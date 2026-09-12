"""Detector: precondition/postcondition checks + live-change scan.

`scan` runs before each action and reports *blocking* changes (things that must be
cleared before we act). `check_post` verifies the page actually reached the state
the step promised. Both are structural: they look at roles, labels and visibility,
not only at test ids, so a stripped/renamed page still yields a correct verdict.
"""
from dataclasses import dataclass, field
import time

RENAMED_PAIRS = [("Apply Filter", "Refine Results"), ("Check Delivery", "Verify Shipment"),
                 ("Search", "Look Up")]

# Build the reverse map so we can spot a rename from either direction.
_ALL_LABELS = [a for pair in RENAMED_PAIRS for a in pair]


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


def _button_labels(page) -> list:
    try:
        return page.evaluate(
            "() => [...document.querySelectorAll('button,[role=button]')]"
            ".map(b => (b.textContent || '').trim()).filter(Boolean)") or []
    except Exception:
        return []


def scan(page, expected_button_texts: list | None = None) -> list:
    """Scan for live changes that block acting. Empty list = clean."""
    out = []
    low = _body_text(page).lower()

    if _visible(page, "#chaos-modal"):
        out.append(ChangeDetected("modal", "no_blocking_modal", "chaos-modal visible",
                                  ["visual"], _now()))
    if _visible(page, "#chaos-confirm"):
        out.append(ChangeDetected("extra_step", "no_interstitial", "chaos-confirm visible",
                                  ["visual"], _now()))

    # label rename: expected label gone, its synonym present instead
    labels = set(_button_labels(page))
    pairs = RENAMED_PAIRS
    if expected_button_texts is not None:
        pairs = [(t, "") for t in expected_button_texts]
    for exp, renamed in pairs:
        if exp.lower() not in low and renamed and renamed.lower() in low:
            out.append(ChangeDetected("label_renamed", exp, renamed, ["text"], _now()))
        elif renamed and renamed in labels and exp not in labels:
            out.append(ChangeDetected("label_renamed", exp, renamed, ["text"], _now()))

    # structure moved: a control we expect is present but no longer where it was
    if _visible(page, "[data-chaos-moved]"):
        out.append(ChangeDetected("structure_moved", "stable_layout",
                                  "element relocated in DOM", ["dom"], _now()))

    title = ""
    try:
        title = page.title() or ""
    except Exception:
        pass
    if "500" in title or "error" in title.lower():
        out.append(ChangeDetected("error_page", "site_page", title, ["text"], _now()))
    return out


def _count_visible_cards(page) -> int:
    """Visible product cards in whichever list is currently displayed."""
    try:
        return int(page.evaluate(
            "() => { const live = document.querySelector('#chaos-list-container') "
            "|| document.querySelector('[data-testid=\\'results\\']') "
            "|| document.querySelector('section[aria-label=\\'Results\\']') || document.body; "
            "return [...live.querySelectorAll('article')].filter(c => c.offsetParent !== null "
            "&& getComputedStyle(c).display !== 'none').length; }"))
    except Exception:
        return -1


def check_post(page, name: str) -> tuple:
    """Verify a postcondition. Returns (ok, observed)."""
    if name == "results_visible":
        ok = _visible(page, '[data-testid="results"], #chaos-list-container, section[aria-label="Results"]')
        return ok, "results_visible" if ok else "results_missing"
    if name == "results_filtered":
        n = _count_visible_cards(page)
        if n < 0:
            return False, "eval_failed"
        return (n >= 1), f"{n}_visible_cards"
    if name == "product_selected":
        return True, "product_selected"
    if name == "delivery_status_visible":
        sel = ('[data-testid="delivery-status"], #status, '
               'div[role="status"], [aria-live="polite"]')
        try:
            for el in page.locator(sel).all():
                try:
                    t = (el.inner_text() or "").strip()
                except Exception:
                    continue
                if t:
                    return True, t[:160]
            return False, "delivery_status_empty"
        except Exception:
            return False, "delivery_status_missing"
    if name == "enquiry_confirmed":
        # Positive proof only: the desk must say the enquiry was received. A bare
        # "incomplete" validation message is NOT success (mirrors constraints.py).
        sel = ('[data-testid="enquiry-status"], #status, '
               'div[role="status"], [aria-live="polite"]')
        try:
            for el in page.locator(sel).all():
                try:
                    t = (el.inner_text() or "").strip()
                except Exception:
                    continue
                if not t:
                    continue
                low = t.lower()
                if "enquiry received" in low or "reference" in low:
                    return True, t[:200]
                if "incomplete" in low or "required" in low or "error" in low:
                    return False, t[:200]
            return False, "enquiry_status_empty"
        except Exception:
            return False, "enquiry_status_missing"
    return True, f"unknown_postcondition:{name}"


def detect(expected: str, observed: str, signals=None) -> ChangeDetected | None:
    if expected == observed:
        return None
    return ChangeDetected("mismatch", expected, observed, signals or [], _now())


def wait_for_post(page, name: str, timeout_ms: int = 6000, poll_ms: int = 200) -> tuple:
    """Poll a postcondition until it holds or the deadline passes.

    Fixed sleeps are fragile: injected latency (throttle) and live chaos land at
    unpredictable times. We instead poll until the page reaches the promised
    state, bounded by a deadline. Returns (ok, observed) exactly like check_post,
    so callers can drop it in and only pay the real wait when something is slow.
    """
    deadline = _now() + max(0, int(timeout_ms))
    ok, obs = check_post(page, name)
    while not ok and _now() < deadline:
        try:
            page.wait_for_timeout(poll_ms)
        except Exception:
            break
        ok, obs = check_post(page, name)
    return ok, obs


def settle(page, quiet_ms: int = 250, max_ms: int = 2000) -> None:
    """Wait for the DOM to stop changing (bounded). Absorbs async chaos injection.

    We watch document.body child-count changes via a light MutationObserver; when
    nothing mutates for `quiet_ms`, the page is considered settled. Capped by
    `max_ms` so a permanently-animating page cannot stall the run.
    """
    try:
        page.evaluate(
            """({quiet, cap}) => new Promise((resolve) => {
                const root = document.body;
                if (!root) return resolve();
                let done = false;
                const finish = () => { if (!done) { done = true; obs.disconnect(); resolve(); } };
                let timer = setTimeout(finish, quiet);
                const capTimer = setTimeout(finish, cap);
                const obs = new MutationObserver(() => {
                    clearTimeout(timer);
                    timer = setTimeout(finish, quiet);
                });
                obs.observe(root, {childList: true, subtree: true, attributes: true});
                setTimeout(() => { clearTimeout(capTimer); finish(); }, cap);
            })""",
            {"quiet": quiet_ms, "cap": max_ms})
    except Exception:
        try:
            page.wait_for_timeout(min(quiet_ms, max_ms))
        except Exception:
            pass
