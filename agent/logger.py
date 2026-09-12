"""Logger: action log + recovery log + hash chain + metrics + colored stage output."""
import json, sys, time, pathlib

try:
    from rich.console import Console
    # A legacy console (Git Bash/mintty, cmd.exe) reports isatty()=True but encodes as
    # cp1252, so rich's step glyphs (\u2713) raise UnicodeEncodeError and kill the run
    # mid-step. Degrade the glyph instead of the run (caught 2026-09-12: guard died
    # with charmap_encode on 'step action').
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:
        pass
    _console = Console()
except Exception:
    _console = None

def stage(kind: str, msg: str):
    """Colored one-liners for the demo terminal. Plain print fallback (no rich = no color, same text)."""
    styles = {"step": "green", "ok": "green", "recovery": "red",
              "healed": "yellow", "metric": "cyan", "hash": "dim", "warn": "red"}
    if _console is not None:
        try:
            _console.print(msg, style=styles.get(kind, ""), highlight=False)
            return
        except Exception:
            pass
    try:
        print(msg, flush=True)
    except Exception:
        print(msg.encode("ascii", "replace").decode(), flush=True)

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
