"""Executor: Playwright actions + pre/post state hashes. 3s timeout; snapshot fallback."""
import hashlib, time

DEFAULT_TIMEOUT_MS = 3000

def state_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()

def page_state(page) -> str:
    try:
        return page.content()
    except Exception:
        try:
            return page.evaluate("() => document.documentElement.outerHTML") or ""
        except Exception as e:
            return f"<snapshot-failed:{e}>"

def do_action(page, action: str, locator, value: str | None = None, timeout_ms: int = DEFAULT_TIMEOUT_MS):
    t0 = time.time()
    before = state_hash(page_state(page))
    result = "ok"
    try:
        if action == "goto":
            page.goto(value, wait_until="domcontentloaded", timeout=timeout_ms)
        elif action == "click":
            locator.click(timeout=timeout_ms)
        elif action == "fill":
            locator.fill(value or "", timeout=timeout_ms)
        elif action == "press":
            locator.press(value or "Enter", timeout=timeout_ms)
        else:
            raise ValueError(f"unknown action {action}")
    except Exception as e:
        result = f"timeout_or_error: {type(e).__name__}: {e}"
        try:
            snap = page_state(page)
            before = state_hash(snap)
        except Exception:
            pass
    after = state_hash(page_state(page))
    return {"state_before_hash": before, "state_after_hash": after,
            "duration_ms": int((time.time() - t0) * 1000), "result": result}
