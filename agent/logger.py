"""Logger: action log + recovery log + hash chain + metrics."""
import json, time, pathlib

def _append(path: str, obj: dict):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")

def log_action(**kw):
    kw.setdefault("ts", int(time.time() * 1000))
    _append("logs/actions.jsonl", kw)

def log_recovery(**kw):
    kw.setdefault("ts", int(time.time() * 1000))
    _append("logs/recoveries.jsonl", kw)

def log_hash(**kw):
    kw.setdefault("ts", int(time.time() * 1000))
    _append("logs/replay-hashes.jsonl", kw)
