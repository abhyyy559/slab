"""Reflect: regression-guarded version bumps + rollback. Learning loop with logs.

Every decision lands in logs/versions.jsonl (PROPOSED/ACCEPTED/REJECTED/ROLLED_BACK).
v1 baseline carries learned_by: webcmd; bumps carry reflected_from: <heal event>.
"""
import copy
import json
import pathlib
import shutil
import time

COMMANDS = pathlib.Path("commands")
HISTORY = COMMANDS / ".history"
VERSIONS_LOG = pathlib.Path("logs/versions.jsonl")

# variant -> (run kwargs, expectation). v5 transfer pending (SKIP, needs real site).
GUARD = {
    1: ({"variant": 1}, lambda o: o.get("status") == "pass" and o.get("extra_steps", 99) == 0),
    2: ({"variant": 2, "budget": 25000}, lambda o: o.get("status") == "pass"),
    3: ({"variant": 3, "pin": "500002"}, lambda o: o.get("status") == "ABSTAIN"),
    4: ({"variant": 4, "perturb": "composite"},
        lambda o: o.get("status") == "pass" and o.get("extra_steps", 99) <= 2),
    6: ({"variant": 6, "budget": 8000, "ram": 12},
        lambda o: o.get("status") == "ABSTAIN" and o.get("failed_constraint") == "max_price AND min_ram"),
}

def _cmd_path(workflow: str) -> pathlib.Path:
    return COMMANDS / f"{workflow}.json"

def _load(workflow: str) -> dict:
    return json.loads(_cmd_path(workflow).read_text(encoding="utf-8"))

def _log(event: dict):
    VERSIONS_LOG.parent.mkdir(parents=True, exist_ok=True)
    event.setdefault("ts", int(time.time() * 1000))
    with VERSIONS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

def run_guard(workflow: str = "phone_delivery_check", base: str = "http://127.0.0.1:8000",
              command_path: str | None = None) -> dict:
    """Run all guard variants against a command file. Returns {variant: {ok, detail}} + overall."""
    from .replayer import run_variant
    if command_path is None:
        command_path = str(_cmd_path(workflow))
    results, ok_all = {}, True
    for variant, (kw, expect) in GUARD.items():
        try:
            out = run_variant(base=base, command_path=command_path, auto_approve=True,
                              headless=True, goal="", **kw)
            ok = bool(expect(out))
            detail = f"status={out.get('status')} extra={out.get('extra_steps')}"
        except Exception as e:
            ok, detail = False, f"error:{type(e).__name__}:{str(e)[:120]}"
        results[variant] = {"ok": ok, "detail": detail}
        ok_all = ok_all and ok
    results["transfer_v5"] = {"ok": None, "detail": "SKIP: real-site credibility run pending"}
    results["overall"] = ok_all
    return results

def _mutate(data: dict, mode: str, reflected_from: str) -> dict:
    data = copy.deepcopy(data)
    lessons = data.setdefault("lessons", [])
    if mode == "good":
        lessons.append({"reflected_from": reflected_from,
                        "note": "filter_button synonyms observed under rename perturb",
                        "synonyms": {"Apply Filter": ["Refine Results"]}})
    elif mode == "bad":
        data["params"]["budget"] = "100"  # absurd: breaks every eligibility check
        lessons.append({"reflected_from": reflected_from, "note": "DEMO bad lesson (budget=100)"})
    else:
        raise ValueError(f"unknown mode {mode}")
    data["version"] = int(data.get("version", 1)) + 1
    return data

def propose_bump(workflow: str = "phone_delivery_check", reflected_from: str = "variant_4_heal",
                 mode: str = "good", base: str = "http://127.0.0.1:8000") -> dict:
    """Propose a lesson bump; ACCEPT only if the full guard passes. Returns the verdict."""
    data = _load(workflow)
    from_v = int(data.get("version", 1))
    mutated = _mutate(data, mode, reflected_from)
    to_v = mutated["version"]
    _log({"event": "PROPOSED", "workflow": workflow, "from_version": from_v,
          "to_version": to_v, "mode": mode, "reflected_from": reflected_from})
    tmp = COMMANDS / f".{workflow}.v{to_v}.tmp.json"
    tmp.write_text(json.dumps(mutated, indent=2), encoding="utf-8")
    try:
        guard = run_guard(workflow, base, command_path=str(tmp))
    finally:
        if tmp.exists():
            tmp.unlink()
    first_bad = next((str(v) for v, r in guard.items() if isinstance(v, int) and not r["ok"]), None)
    if guard["overall"]:
        HISTORY.mkdir(parents=True, exist_ok=True)
        shutil.copy(_cmd_path(workflow), HISTORY / f"{workflow}.v{from_v}.json")
        _cmd_path(workflow).write_text(json.dumps(mutated, indent=2), encoding="utf-8")
        _log({"event": "ACCEPTED", "workflow": workflow, "from_version": from_v,
              "to_version": to_v, "mode": mode, "reflected_from": reflected_from,
              "learned_by": "webcmd", "guard": {str(k): v for k, v in guard.items() if isinstance(k, int)}})
        return {"verdict": "ACCEPTED", "from_version": from_v, "to_version": to_v, "guard": guard}
    _log({"event": "REJECTED", "workflow": workflow, "from_version": from_v,
          "to_version": to_v, "mode": mode, "reflected_from": reflected_from,
          "reason": f"variant {first_bad} failed", "guard": {str(k): v for k, v in guard.items() if isinstance(k, int)}})
    return {"verdict": "REJECTED", "reason": f"variant {first_bad} failed",
            "from_version": from_v, "to_version": to_v, "guard": guard}

def rollback(workflow: str = "phone_delivery_check", to: int = 1,
             base: str = "http://127.0.0.1:8000", verify: bool = True) -> dict:
    """Restore commands/<workflow>.json from .history backup. Optionally re-run guard."""
    src = HISTORY / f"{workflow}.v{to}.json"
    if not src.exists():
        return {"verdict": "FAILED", "reason": f"no backup {src}"}
    shutil.copy(src, _cmd_path(workflow))
    rec = {"event": "ROLLED_BACK", "workflow": workflow, "to_version": to,
           "current_version": json.loads(_cmd_path(workflow).read_text()) .get("version")}
    if verify:
        rec["guard"] = {str(k): v for k, v in run_guard(workflow, base).items() if isinstance(k, int)}
        rec["guard_overall"] = all(v["ok"] for v in rec["guard"].values())
    _log(rec)
    return {"verdict": "ROLLED_BACK", **rec}
