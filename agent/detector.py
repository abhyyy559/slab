"""Detector: compare expected precondition vs current page state."""
from dataclasses import dataclass
import time

@dataclass
class ChangeDetected:
    type: str
    expected: str
    observed: str
    signals: list
    timestamp_ms: int

def detect(expected: str, observed: str, signals=None) -> ChangeDetected | None:
    if expected == observed:
        return None
    return ChangeDetected(
        type="mismatch", expected=expected, observed=observed,
        signals=signals or [], timestamp_ms=int(time.time() * 1000),
    )
