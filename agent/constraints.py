"""Constraints: per-constraint pass/fail/unsat + ABSTAIN with named failed constraint."""
ABSTAIN = "ABSTAIN"

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
