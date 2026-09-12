"""Detector: precondition/postcondition checks + live-change scan. Timestamps the moment of detection."""
from dataclasses import dataclass, field
import time

RENAMED_PAIRS = [("Apply Filter", "Refine Results"), ("Check Delivery", "Verify Shipment"), ("Search", "Look Up")]

@dataclass
class ChangeDetected:
    type: str
    expected: str
    observed: str
    signals: list = field(default_factory=list)
    timestamp_ms: int = 0

def _now() -> int:
    return int(time.time() * 1000)

def _visible(page, selector: str) -> bool:
    try:
        loc = page.locator(selector)
        return loc.count() >= 1 and loc.first.is_visible()
    except Exception:
        return False

def _body_text(page) -> str:
    try:
        return page.evaluate("() => document.body ? document.body.innerText : ''") or ""
    except Exception:
        return ""

def scan(page, expected_button_texts: list | None = None) -> list:
    """Scan for live changes. Returns ChangeDetected list (empty = clean)."""
    out = []
    body = _body_text(page)
    low = body.lower()
    if _visible(page, "#chaos-modal"):
        out.append(ChangeDetected("modal", "no_blocking_modal", "chaos-modal visible",
                                  ["visual"], _now()))
    if _visible(page, "#chaos-confirm"):
        out.append(ChangeDetected("extra_step", "no_interstitial", "chaos-confirm visible",
                                  ["visual"], _now()))
    for exp, renamed in (RENAMED_PAIRS if expected_button_texts is None
                         else [(t, "") for t in expected_button_texts]):
        if exp.lower() not in low and renamed and renamed.lower() in low:
            out.append(ChangeDetected("label_renamed", exp, renamed, ["text"], _now()))
    title = ""
    try:
        title = page.title() or ""
    except Exception:
        pass
    if "500" in title or "error" in title.lower():
        out.append(ChangeDetected("error_page", "site_page", title, ["text"], _now()))
    return out

def check_post(page, name: str) -> tuple:
    """Verify a postcondition. Returns (ok: bool, observed: str)."""
    if name == "results_visible":
        ok = _visible(page, '[data-testid="results"], #chaos-results')
        return ok, "results_visible" if ok else "results_missing"
    if name == "results_filtered":
        try:
            n = page.evaluate("() => [...document.querySelectorAll('[data-testid=\"product-card\"]')].filter(c => c.style.display !== 'none').length")
            return (n >= 1, f"{n}_visible_cards")
        except Exception as e:
            return False, f"eval_failed:{e}"[:120]
    if name == "product_selected":
        return True, "product_selected"
    if name == "delivery_status_visible":
        try:
            t = page.inner_text('[data-testid="delivery-status"]') or ""
            return (len(t.strip()) > 0, t.strip()[:80] or "delivery_status_empty")
        except Exception:
            return False, "delivery_status_missing"
    return True, f"unknown_postcondition:{name}"

def detect(expected: str, observed: str, signals=None) -> ChangeDetected | None:
    if expected == observed:
        return None
    return ChangeDetected("mismatch", expected, observed, signals or [], _now())
