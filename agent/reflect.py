"""Reflect: version bump + regression guard + rollback. Implements the learn->replay->heal->version-bump loop."""
import datetime, json, os, pathlib, shutil, subprocess
from .logger import log_action

def run_regression_guard() -> bool:
    """Execute regression test suite to ensure strategy updates do not break invariants."""
    try:
        from harness.regression.test_guard import test_command_schema, test_template_integrity, test_params_present
        test_command_schema()
        test_template_integrity()
        test_params_present()
        return True
    except Exception as e:
        print(f"[Reflect] Regression guard failed: {e}")
        return False

def reflect_on_run(workflow_path: str = "commands/phone_delivery_check.json",
                   recoveries: list | None = None, last_run: dict | None = None) -> dict:
    """Evaluate run recoveries and execute a regression-guarded version bump if healed strategy should persist."""
    p = pathlib.Path(workflow_path)
    if not p.exists():
        return {"action": "skipped", "reason": "workflow_not_found"}
    
    data = json.loads(p.read_text(encoding="utf-8"))
    workflow = data.get("workflow", "phone_delivery_check")
    current_ver = int(data.get("version", 1))

    # Read recoveries from argument or logs/recoveries.jsonl
    if recoveries is None:
        rec_path = pathlib.Path("logs/recoveries.jsonl")
        if rec_path.exists():
            recoveries = [json.loads(line) for line in rec_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        else:
            recoveries = []

    has_meaningful_recovery = any(r.get("strategy") in ("re_plan", "backtrack", "re_locate") for r in (recoveries or []))
    
    if not has_meaningful_recovery:
        return {"action": "no_change_needed", "version": current_ver}

    # Run regression guard before bumping
    if not run_regression_guard():
        log_action(event="VERSION_BUMP_REJECTED", workflow=workflow, version=current_ver, reason="regression_guard_failed")
        return {"action": "bump_rejected", "reason": "regression_guard_failed", "version": current_ver}

    # Backup current version
    backup_path = p.parent / f"{workflow}.v{current_ver}.json"
    shutil.copy2(p, backup_path)

    new_ver = current_ver + 1
    data["version"] = new_ver
    data.setdefault("provenance", {})["last_healed_at"] = datetime.datetime.now().isoformat()
    data["provenance"]["healed_from_version"] = current_ver
    data["provenance"]["recoveries_absorbed"] = len(recoveries)

    p.write_text(json.dumps(data, indent=2), encoding="utf-8")

    bump_record = {
        "workflow": workflow,
        "from_version": current_ver,
        "to_version": new_ver,
        "timestamp": datetime.datetime.now().isoformat(),
        "backup_path": str(backup_path),
        "recoveries_count": len(recoveries)
    }

    # Log bump event
    log_action(event="VERSION_BUMPED", **bump_record)
    
    vb_log = pathlib.Path("logs/version_bumps.jsonl")
    vb_log.parent.mkdir(parents=True, exist_ok=True)
    with vb_log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(bump_record) + "\n")

    print(f"[Reflect] Regression guard passed. Workflow {workflow} bumped from v{current_ver} -> v{new_ver}.", flush=True)
    return {"action": "version_bumped", "workflow": workflow, "old_version": current_ver, "new_version": new_ver}

def rollback(workflow: str = "phone_delivery_check", to: int = 1) -> bool:
    """Restore workflow command JSON to a previous version."""
    target = pathlib.Path(f"commands/{workflow}.json")
    backup = pathlib.Path(f"commands/{workflow}.v{to}.json")
    if not backup.exists():
        print(f"[Reflect] Rollback target backup not found: {backup}")
        return False
    shutil.copy2(backup, target)
    log_action(event="ROLLBACK_EXECUTED", workflow=workflow, restored_version=to)
    print(f"[Reflect] Successfully rolled back {workflow} to v{to}.")
    return True

