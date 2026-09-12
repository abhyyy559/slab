"""Recovery ladder: re-locate / re-plan / backtrack + verify. Never act irreversibly on unverified state."""
import time

def recover(trigger: str, expected: str, observed: str) -> dict:
    t0 = int(time.time() * 1000)
    # v1: re-locate only; re-plan/backtrack wired in Phase 2
    rec = {"trigger": trigger, "expected": expected, "observed": observed,
           "strategy": "re_locate", "steps": 1,
           "time_to_heal_ms": int(time.time() * 1000) - t0,
           "verified": False}
    return rec
