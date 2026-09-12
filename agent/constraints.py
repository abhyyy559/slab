"""Constraints: per-constraint pass/fail/unsat + ABSTAIN with named failed constraint."""
ABSTAIN = "ABSTAIN"

# Positive proof required for deliverability. Never substring-match bare words like
# "available" — "not available" contains it (caught by guard 2026-09-12, 3rd verification catch).
DELIVERABLE_PROOF = "2-3 days"

NEGATIVE_MARKERS = ("not available", "unavailable", "out of stock", "no delivery",
                    "currently unavailable", "cannot deliver")

def deliverable_within_days(status_text: str) -> bool:
    """True only with positive proof AND no negative marker. Infrastructure, not a patch."""
    t = (status_text or "").lower()
    if any(m in t for m in NEGATIVE_MARKERS):
        return False
    return DELIVERABLE_PROOF in (status_text or "")

def check(constraints: dict) -> dict:
    results = {}
    for k, v in constraints.items():
        results[k] = "pass" if v else "unsat"
    failed = [k for k, v in results.items() if v != "pass"]
    out = {"results": results}
    if failed:
        out["decision"] = ABSTAIN
        out["failed_constraint"] = failed[0]
    else:
        out["decision"] = "proceed"
    return out
