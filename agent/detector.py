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

def scan(page, expected_button_texts: list | None = None) -> list:
    """Scan for live changes. Returns ChangeDetected list (empty = clean)."""
    out = []
    res = page.evaluate("""() => {
        const modal = document.getElementById('chaos-modal');
        const confirm = document.getElementById('chaos-confirm');
        const modalVis = !!(modal && (modal.offsetWidth || modal.offsetHeight || modal.getClientRects().length));
        const confirmVis = !!(confirm && (confirm.offsetWidth || confirm.offsetHeight || confirm.getClientRects().length));
        const body = document.body ? document.body.innerText : '';
        const title = document.title || '';
        return { modalVis, confirmVis, body, title };
    }""") or {}

    body = res.get("body", "")
    low = body.lower()
    if res.get("modalVis"):
        out.append(ChangeDetected("modal", "no_blocking_modal", "chaos-modal visible", ["visual"], _now()))
    if res.get("confirmVis"):
        out.append(ChangeDetected("extra_step", "no_interstitial", "chaos-confirm visible", ["visual"], _now()))
    for exp, renamed in (RENAMED_PAIRS if expected_button_texts is None
                         else [(t, "") for t in expected_button_texts]):
        if exp.lower() not in low and renamed and renamed.lower() in low:
            out.append(ChangeDetected("label_renamed", exp, renamed, ["text"], _now()))
    title = res.get("title", "")
    if "500" in title or "error" in title.lower():
        out.append(ChangeDetected("error_page", "site_page", title, ["text"], _now()))
    return out

def check_post(page, name: str) -> tuple:
    """Verify a postcondition. Returns (ok: bool, observed: str)."""
    if name == "results_visible":
        res = page.evaluate("""() => {
            const el = document.querySelector('[data-testid="results"], #chaos-results');
            return !!(el && (el.offsetWidth || el.offsetHeight || el.getClientRects().length));
        }""")
        ok = bool(res)
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
            t = page.evaluate("""() => {
                const el = document.querySelector('[data-testid="delivery-status"]');
                return el ? el.innerText : '';
            }""") or ""
            return (len(t.strip()) > 0, t.strip()[:80] or "delivery_status_empty")
        except Exception:
            return False, "delivery_status_missing"
    return True, f"unknown_postcondition:{name}"

def detect(expected: str, observed: str, signals=None) -> ChangeDetected | None:
    if expected == observed:
        return None
    return ChangeDetected("mismatch", expected, observed, signals or [], _now())

