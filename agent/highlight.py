"""Live element highlighting for headed runs.

The rubric's stretch goal is "a dashboard that replays the run with the detected
changes highlighted". The trace already *says* what was grounded; this module makes
the browser *show* it, in real time, on the element the agent is about to touch.

Design constraints
------------------
* It must never affect the run. All calls are best-effort and swallow errors.
* It must not change the DOM the agent grounds against (no extra ids/classes on the
  target itself), so grounding and highlighting cannot interfere.
* Overlay nodes are tagged `data-sentry-overlay` and cleaned up on every call, so a
  swap/rerender cannot leave orphans behind.
"""
from __future__ import annotations

import json

# Injected once per page; idempotent.
_INSTALL = r"""
() => {
  if (window.__sentryHighlight) return;
  const layer = document.createElement('div');
  layer.id = '__sentry_layer';
  layer.setAttribute('data-sentry-overlay', '1');
  layer.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:2147483000;';
  document.documentElement.appendChild(layer);
  window.__sentryHighlight = true;
}
"""

# Draw a labelled outline around a bounding box. Colours carry meaning:
#   cyan  = grounding a target (about to act)
#   amber = a detected UI change (before recovery)
#   green = recovered / verified
#   red   = abstained / failed
_COLORS = {"ground": "#22d3ee", "change": "#fbbf24", "heal": "#34d399", "abstain": "#f87171"}


def _box_js(box: dict, kind: str, label: str, ttl_ms: int) -> str:
    color = _COLORS.get(kind, "#22d3ee")
    label_s = json.dumps(label or "")
    return f"""
    () => {{
      const layer = document.getElementById('__sentry_layer');
      if (!layer) return;
      const el = document.createElement('div');
      el.setAttribute('data-sentry-overlay', '1');
      el.style.cssText = 'position:fixed;left:{box['x']}px;top:{box['y']}px;'
        + 'width:{box['width']}px;height:{box['height']}px;border:3px solid {color};'
        + 'border-radius:6px;box-shadow:0 0 0 2px rgba(0,0,0,.35), 0 0 18px {color};'
        + 'transition:opacity .35s ease;';
      if ({label_s}) {{
        const tag = document.createElement('div');
        tag.textContent = {label_s};
        tag.style.cssText = 'position:absolute;top:-22px;left:-3px;background:{color};'
          + 'color:#06121f;font:600 11px/1.6 system-ui,sans-serif;padding:0 7px;border-radius:5px;'
          + 'white-space:nowrap;';
        el.appendChild(tag);
      }}
      layer.appendChild(el);
      setTimeout(() => {{ el.style.opacity = '0'; setTimeout(() => el.remove(), 400); }}, {ttl_ms});
    }}
    """


def install(page) -> bool:
    """Create the overlay layer if it does not exist. Safe to call repeatedly."""
    try:
        page.evaluate(_INSTALL)
        return True
    except Exception:
        return False


def _clear(page) -> None:
    try:
        page.evaluate(
            "() => document.querySelectorAll('[data-sentry-overlay]')"
            ".forEach(e => { if (e.id !== '__sentry_layer') e.remove(); })")
    except Exception:
        pass


def mark(page, locator, kind: str = "ground", label: str = "", ttl_ms: int = 2200) -> bool:
    """Outline a locator's current position. Returns True if drawn.

    `kind` selects the colour: ground | change | heal | abstain. Best-effort.
    """
    try:
        if locator is None:
            return False
        box = locator.bounding_box()
        if not box or box.get("width", 0) < 1 or box.get("height", 0) < 1:
            return False
        install(page)
        _clear(page)
        page.evaluate(_box_js(box, kind, label, ttl_ms))
        return True
    except Exception:
        return False


def banner(page, text: str, kind: str = "change", ttl_ms: int = 2600) -> bool:
    """A small top-centre toast describing a detected change or recovery."""
    if not text:
        return False
    color = _COLORS.get(kind, "#fbbf24")
    try:
        install(page)
        page.evaluate(
            """({txt, col, ttl}) => {
                const layer = document.getElementById('__sentry_layer');
                if (!layer) return;
                const el = document.createElement('div');
                el.setAttribute('data-sentry-overlay', '1');
                el.textContent = txt;
                el.style.cssText = 'position:fixed;top:14px;left:50%;transform:translateX(-50%);'
                  + 'background:' + col + ';color:#06121f;font:700 13px/1.5 system-ui,sans-serif;'
                  + 'padding:8px 16px;border-radius:999px;box-shadow:0 6px 22px rgba(0,0,0,.4);'
                  + 'transition:opacity .4s ease;white-space:nowrap;';
                layer.appendChild(el);
                setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 450); }, ttl);
            }""",
            {"txt": text, "col": color, "ttl": ttl_ms})
        return True
    except Exception:
        return False


def clear(page) -> None:
    _clear(page)
