"""Approval gate: blocks irreversible actions, logs APPROVAL_REQUESTED/GRANTED/DENIED."""
import sys
from .logger import log_action

def require_approval(url: str, action: str, payload: dict, auto: str | None = None) -> bool:
    log_action(event="APPROVAL_REQUESTED", target=action, url=url, payload=str(payload))
    if auto == "deny":
        log_action(event="APPROVAL_DENIED", target=action, url=url)
        return False
    if auto == "grant":
        log_action(event="APPROVAL_GRANTED", target=action, url=url)
        return True
    print(f"APPROVAL REQUIRED\n  url={url}\n  action={action}\n  payload={payload}")
    ans = input("Approve? [y/N]: ").strip().lower()
    ok = ans == "y"
    log_action(event="APPROVAL_GRANTED" if ok else "APPROVAL_DENIED", target=action, url=url)
    return ok
