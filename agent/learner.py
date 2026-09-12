"""Learner: wraps `webcmd learn`; kill-gate T+0:30 falls back to hand-authored JSON."""
import json, datetime, pathlib

def learn_stub(goal: str, site: str, out: str):
    print("webcmd learn not wired yet (kill-gate: use hand-authored commands/phone_delivery_check.json).")
    print(f"goal={goal} site={site} out={out}")
    return False
