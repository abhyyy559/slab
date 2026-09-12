"""Reflect: version bump + regression guard + rollback. Emits learning-curve data."""
import json, pathlib, shutil

def bump_version(workflow_path: str) -> int:
    p = pathlib.Path(workflow_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    data["version"] = int(data.get("version", 1)) + 1
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data["version"]

def rollback(workflow: str, to: int):
    print(f"rollback {workflow} to v{to}: restore commands/{workflow}.json from git or backup (TODO Phase 3).")
