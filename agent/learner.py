"""Learner: wraps webcmd site adapters (voltkart/search, swiftship/check).

Kill-gate PASSED 2026-09-12: adapters authored via `webcmd browser init`,
verified live against mocks. Sources live in adapters/ (copy to ~/.webcmd/clis/).
"""
import json
import shutil
import subprocess

ADAPTERS = {"site_a": "voltkart/search", "site_b": "swiftship/check"}

def _run(*args: str) -> object:
    exe = shutil.which("webcmd")
    if not exe:
        raise RuntimeError("webcmd CLI not on PATH (npm install -g @agentrhq/webcmd)")
    p = subprocess.run([exe, *args], capture_output=True, text=True, timeout=180)
    if p.returncode != 0:
        raise RuntimeError(f"webcmd failed: {(p.stderr or p.stdout)[:300]}")
    return json.loads(p.stdout)

def learn_site_a(base: str, budget: int = 20000, ram: int = 8) -> object:
    """Learn Site A action space: returns in-stock products within budget/RAM."""
    return _run("voltkart", "search", "--base", base,
                "--max-price", str(budget), "--min-ram", str(ram), "-f", "json")

def learn_site_b(base: str, pin: str = "500001") -> object:
    """Learn Site B action space: returns delivery status rows for a PIN."""
    return _run("swiftship", "check", "--base", base, "--pin", str(pin), "-f", "json")

def learn_workflow(goal: str, base: str, budget: int = 20000,
                   ram: int = 8, pin: str = "500001") -> dict:
    """Full learn pass for the cross-site workflow. Returns adapter rows for both sites."""
    a = learn_site_a(base, budget, ram)
    b = learn_site_b(base, pin)
    return {"status": "learned", "goal": goal, "site_a_rows": a, "site_b_rows": b,
            "provenance": {"learned_by": "webcmd", "adapters": [ADAPTERS["site_a"], ADAPTERS["site_b"]]},
            "command_ref": "commands/phone_delivery_check.json"}
