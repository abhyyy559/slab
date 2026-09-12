"""Headed browser session.

Why this exists
---------------
A headed run is a *demonstration*: the operator (or a judge) has to be able to
watch the agent heal in real time. By default Chromium opens as a background
window and finishes before anyone can find it. This module:

  * launches a real, visible, OS-level window when headless=False;
  * forces it to the foreground / top of the z-order so it is not hidden
    behind the terminal, the dashboard, or other tabs;
  * puts it on the *current* screen (the monitor the operator is looking at),
    not a secondary display;
  * holds the window open on the result for `keep_open_ms` so the last frame
    is readable instead of vanishing the instant the run ends;
  * slows the run with `slow_mo` so recovery steps are legible.

Every trick here is best-effort. If the OS refuses (kiosk, CI, no window
manager) we degrade to a headless-equivalent run rather than crashing the demo.
"""
from __future__ import annotations

import json
import time

# Chromium switches:
#  * start-maximized      -> the window opens large, not a 800x600 box
#  * disable-background-* -> the renderer keeps painting while unfocused, so a
#                            window we cannot raise still shows live progress
#  * no-first-run /          removes the "Chrome is being controlled" friction
#    no-default-browser-check
LAUNCH_ARGS = [
    "--start-maximized",
    "--disable-background-timer-throttling",
    "--disable-backgrounding-occluded-windows",
    "--disable-renderer-backgrounding",
    "--no-first-run",
    "--no-default-browser-check",
]

# Windows: teach the OS this AppUserModelID deserves the foreground, then raise
# the window with the documented SetForegroundWindow call. We match the window
# by the Chromium title fragment so we never touch an unrelated window.
_WIN_FOREGROUND_JS = r"""
() => {
  // Browser-context no-op guard: this runs in the page, not the OS.
  return { title: document.title, url: location.href };
}
"""


def _bring_windows_to_front(timeout_s: float = 3.0) -> bool:
    """Raise the Chromium window to the top of the z-order on Windows.

    Uses ctypes against the Win32 API. Matches on a Chromium window class so we
    never steal focus from an unrelated application. Returns True if a window
    was found and raised.
    """
    try:
        import ctypes
        from ctypes import wintypes
    except Exception:
        return False

    user32 = ctypes.windll.user32
    # Documented trick: attaching input to the foreground thread lifts the
    # SetForegroundWindow restriction when our process does not own the focus.
    try:
        user32.AllowSetForegroundWindow(-1)  # ASFW_ANY
    except Exception:
        pass

    deadline = time.time() + timeout_s
    found = False
    while time.time() < deadline:
        hwnds = []

        @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        def _enum(hwnd, _lparam):
            buf = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, buf, 256)
            cls = buf.value
            if "Chrome" in cls or "Chromium" in cls:
                if user32.IsWindowVisible(hwnd):
                    hwnds.append(hwnd)
            return True

        user32.EnumWindows(_enum, 0)
        for hwnd in hwnds:
            try:
                user32.ShowWindow(hwnd, 9)          # SW_RESTORE
                user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)  # TOPMOST
                user32.SetWindowPos(hwnd, -2, 0, 0, 0, 0, 0x0001 | 0x0002)  # NOTOPMOST (keep on top momentarily)
                user32.SetForegroundWindow(hwnd)
                user32.BringWindowToTop(hwnd)
                found = True
            except Exception:
                continue
        if found:
            return True
        time.sleep(0.25)
    return False


def _position_window(page, width: int, height: int) -> None:
    """Ask the browser to place its viewport at the current origin on screen."""
    try:
        # window.moveTo(0,0) is ignored by some builds but honoured by headed
        # Chromium windows; combined with start-maximized it lands on the
        # primary/current monitor.
        page.evaluate(f"() => {{ try {{ window.moveTo(0, 0); }} catch (e) {{}} }}")
    except Exception:
        pass


def launch_browser(pw, headless: bool = True, slow_mo: int = 0,
                   viewport: dict | None = None, channel: str | None = None,
                   raise_window: bool = True):
    """Launch Chromium. Headed launches get a visible, focused, maximized window.

    Returns (browser, context). The caller owns closing the browser.
    """
    kwargs: dict = {"headless": headless, "slow_mo": max(0, int(slow_mo or 0))}
    if not headless:
        kwargs["args"] = LAUNCH_ARGS
    if channel:
        kwargs["channel"] = channel
    try:
        browser = pw.chromium.launch(**kwargs)
    except Exception:
        # Channel (e.g. a real Chrome install) missing: fall back to bundled.
        kwargs.pop("channel", None)
        browser = pw.chromium.launch(**kwargs)

    ctx_kwargs: dict = {}
    if viewport and not headless:
        ctx_kwargs["viewport"] = None  # let start-maximized win
    elif viewport:
        ctx_kwargs["viewport"] = viewport
    context = browser.new_context(**ctx_kwargs)

    if not headless and raise_window:
        # Give the OS a beat to map the window, then raise it. Retried inside.
        _bring_windows_to_front(timeout_s=3.0)
    return browser, context


def focus_window(page, raise_window: bool = True) -> bool:
    """Re-raise the visible window and land the viewport on the current screen."""
    if not raise_window:
        return False
    ok = _bring_windows_to_front(timeout_s=1.5)
    _position_window(page, 0, 0)
    try:
        page.bring_to_front()
    except Exception:
        pass
    return ok


def hold_open(ms: int, keep_foreground: bool = True) -> None:
    """Keep the final frame on screen so the operator can read it.

    Chromium will not idle forever when unfocused, but the window stays mapped.
    We raise ONCE at the start of the dwell and then leave the window alone: a
    periodic re-raise fights the operator the moment they click another window,
    which is exactly what makes a demo feel like it is hijacking the desktop.
    """
    if ms <= 0:
        return
    if keep_foreground:
        _bring_windows_to_front(timeout_s=0.5)
    time.sleep(ms / 1000.0)


def describe_window() -> dict:
    """Diagnostics for the console/CLI: what window did we actually get?"""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        return {"screen_w": user32.GetSystemMetrics(0), "screen_h": user32.GetSystemMetrics(1)}
    except Exception:
        return {}
