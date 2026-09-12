"""Approval gate: VISIBLE browser modal first, CLI fallback. Logs APPROVAL_REQUESTED/GRANTED/DENIED."""
from .logger import log_action

MODAL_JS = """(opts) => {
  const old = document.getElementById('sentry-approval');
  if (old) old.remove();
  const ov = document.createElement('div');
  ov.id = 'sentry-approval';
  ov.setAttribute('role', 'dialog');
  ov.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:999999;display:flex;align-items:center;justify-content:center;';
  ov.innerHTML = `<div style="background:#fff;color:#000;padding:24px;max-width:480px;font-family:sans-serif;border:3px solid #000;">`
    + `<h2 style="margin-top:0">SENTRY wants approval</h2>`
    + `<p><b>action:</b> ${opts.action}</p>`
    + `<p><b>url:</b> ${opts.url}</p>`
    + `<p><b>payload:</b> ${opts.payload}</p>`
    + `<button id="sentry-ok" style="padding:12px 24px;margin-right:12px;font-size:16px;">Approve</button>`
    + `<button id="sentry-no" style="padding:12px 24px;font-size:16px;">Deny</button></div>`;
  document.body.appendChild(ov);
  return new Promise((resolve) => {
    document.getElementById('sentry-ok').onclick = () => { ov.remove(); resolve(true); };
    document.getElementById('sentry-no').onclick = () => { ov.remove(); resolve(false); };
  });
}"""

def require_approval_browser(page, url: str, action: str, payload: dict, timeout_ms: int = 60000) -> bool:
    """Inject a visible modal; a teammate clicks Approve/Deny. Returns the choice."""
    log_action(event="APPROVAL_REQUESTED", target=action, url=url, payload=str(payload), mode="browser_modal")
    try:
        ok = page.evaluate(MODAL_JS, {"url": url, "action": action, "payload": str(payload)})
        # sync API: evaluate returning a Promise resolves to the value
        ok = bool(ok)
    except Exception as e:
        log_action(event="APPROVAL_MODAL_FAILED", target=action, url=url, error=str(e)[:200])
        return require_approval(url, action, payload)
    log_action(event="APPROVAL_GRANTED" if ok else "APPROVAL_DENIED", target=action, url=url, mode="browser_modal")
    return ok

def require_approval(url: str, action: str, payload: dict, auto: str | None = None) -> bool:
    log_action(event="APPROVAL_REQUESTED", target=action, url=url, payload=str(payload), mode="cli")
    if auto == "deny":
        log_action(event="APPROVAL_DENIED", target=action, url=url, mode="cli")
        return False
    if auto == "grant":
        log_action(event="APPROVAL_GRANTED", target=action, url=url, mode="cli")
        return True
    print(f"APPROVAL REQUIRED\n  url={url}\n  action={action}\n  payload={payload}")
    ans = input("Approve? [y/N]: ").strip().lower()
    ok = ans == "y"
    log_action(event="APPROVAL_GRANTED" if ok else "APPROVAL_DENIED", target=action, url=url, mode="cli")
    return ok
