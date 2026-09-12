"""SENTRY judge console: live perturbation injector + agent run dashboard.

Endpoints
  GET  /status               mock pages poll this; chaos.js reads .active -> SHAPE IS FROZEN
  POST /perturb/<type>       set / clear the active perturbation (shuffle|rename|modal|...)
  GET  /                     the dashboard (static/index.html)
  POST /api/run              start a job: run | guard | bump | rollback
  GET  /api/run/<id>/stream  SSE stream: meta, stdout, trace, result, done
  GET  /api/state            server + latest job status

Why subprocesses: the agent drives Playwright's *sync* API, which cannot be used from a
thread that has a running asyncio loop, and log tailing gives a far richer trace than
scraping stdout. Each job is `python -u -m agent ...` with its stdout piped and the
logs/*.jsonl files tailed from a byte offset captured at job start.
"""
import json
import pathlib
import queue
import subprocess
import sys
import threading
import time

from flask import Flask, Response, jsonify, request, send_from_directory

ROOT = pathlib.Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "logs"
TRACE_FILES = ("actions.jsonl", "recoveries.jsonl", "replay-hashes.jsonl", "versions.jsonl")
MOCK_BASE = "http://127.0.0.1:8000"
JOB_TIMEOUT_MS = 600_000
MAX_JOBS = 25
HISTORY = LOG_DIR / "dashboard-runs.jsonl"
HISTORY_MAX = 200
HOLD_MS = 150          # trace settle window before an event is released to the browser

# Import the plan layer directly: the rail must not depend on tailing shared log files, which
# is racy for jobs that finish between polls (a refused goal never launches a browser at all).
# Same function the agent uses, so the two cannot disagree.
sys.path.insert(0, str(ROOT))
try:
    from agent.planner import plan_goal as _plan_goal
    _PLANNER_ERROR = None
except Exception as e:          # never let the dashboard die because of an import
    _plan_goal, _PLANNER_ERROR = None, f"{type(e).__name__}: {e}"

app = Flask(__name__, static_folder="static", static_url_path="/static")

STATE = {"active": None, "ts": None, "seed": 42,
         "composite": ["rename", "strip", "move", "attrs", "modal", "extra_step", "throttle"]}

JOBS: dict = {}
_lock = threading.Lock()


# --------------------------------------------------------------------------- utils
def _now_ms() -> int:
    return int(time.time() * 1000)


def _append_json(path: pathlib.Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")


def _parse_json_blob(text: str):
    """Pull the first complete JSON object out of mixed stdout (agent prints JSON + a table)."""
    dec = json.JSONDecoder()
    i = text.find("{")
    while i != -1:
        try:
            obj, _ = dec.raw_decode(text[i:])
            return obj
        except ValueError:
            i = text.find("{", i + 1)
    return None


# ----------------------------------------------------------------- frozen endpoints
@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.get("/status")
def status():
    return jsonify(STATE)


@app.get("/api/perturbations")
def perturbations():
    """The full catalogue, so the dashboard builds its injector from one source."""
    try:
        from harness.perturbations import PERTURBATIONS, CHAOS_TYPES
        return jsonify({"types": CHAOS_TYPES, "catalogue": PERTURBATIONS})
    except Exception as e:
        return jsonify({"types": [], "error": f"{type(e).__name__}: {e}"})


@app.post("/perturb/<string:typ>")
def p_generic(typ):
    """Generic injector: any catalogue type, so the UI never drifts from chaos.js."""
    try:
        from harness.perturbations import CHAOS_TYPES
        if typ != "reset" and typ not in CHAOS_TYPES:
            return jsonify({"error": f"unknown perturbation {typ!r}"}), 400
    except Exception:
        pass
    return _set(None if typ == "reset" else typ)


def _set(typ):
    STATE.update(active=typ, ts=_now_ms())
    try:
        _append_json(LOG_DIR / "actions.jsonl",
                     {"event": "PERTURB_INJECTED", "type": typ, "ts": _now_ms(), "source": "console"})
    except Exception:
        pass
    return jsonify(STATE)


@app.post("/perturb/shuffle")
def p_shuffle(): return _set("move")
@app.post("/perturb/rename")
def p_rename(): return _set("rename")
@app.post("/perturb/strip")
def p_strip(): return _set("strip")
@app.post("/perturb/move")
def p_move(): return _set("move")
@app.post("/perturb/attrs")
def p_attrs(): return _set("attrs")
@app.post("/perturb/modal")
def p_modal(): return _set("modal")
@app.post("/perturb/extra_step")
def p_extra(): return _set("extra_step")
@app.post("/perturb/throttle")
def p_throttle(): return _set("throttle")
@app.post("/perturb/ab")
def p_ab(): return _set("ab")
@app.post("/perturb/swap")
def p_swap(): return _set("swap")
@app.post("/perturb/composite")
def p_comp(): return _set("composite")
@app.post("/perturb/chaos_max")
def p_max(): return _set("chaos_max")
@app.post("/perturb/reset")
def p_reset(): return _set(None)


# ------------------------------------------------------------------------ job runner
def _argv(action: str, p: dict) -> list:
    py = sys.executable
    base = str(p.get("base") or MOCK_BASE)
    if action == "run":
        a = [py, "-u", "-m", "agent", "run", "--variant", str(p.get("variant", 1)),
             "--base", base, "--goal", str(p.get("goal") or "")]
        if p.get("perturb"):
            a += ["--perturb", str(p["perturb"])]
        for key in ("budget", "ram"):
            if p.get(key) not in (None, ""):
                a += [f"--{key}", str(p[key])]
        if p.get("pin"):
            a += ["--pin", str(p["pin"])]
        if p.get("brand"):
            a += ["--brand", str(p["brand"])]
        if p.get("headed"):
            a += ["--headed"]
            if p.get("slowmo") not in (None, ""):
                a += ["--slowmo", str(p["slowmo"])]
            # Headed runs from the dashboard hold the final frame for a few seconds
            # so the operator can read the result before the window closes itself.
            # Pass keep_open explicitly to override; 0 means close immediately.
            keep = p.get("keep_open")
            a += ["--keep-open", str(keep if keep not in (None, "") else 4000)]
            if p.get("no_raise"):
                a += ["--no-raise"]
        if p.get("channel"):
            a += ["--channel", str(p["channel"])]
        if p.get("pause_on_low"):
            a += ["--pause-on-low"]
        if p.get("no_highlight"):
            a += ["--no-highlight"]
        if p.get("approval_modal"):
            a += ["--no-yes"]
        return a
    if action == "guard":
        code = ("import json;from agent.reflect import run_guard;"
                f"print(json.dumps(run_guard(base={base!r}),indent=2))")
        return [py, "-u", "-c", code]
    if action == "learn":
        code = ("import json;from agent.learner import learn_workflow;"
                f"print(json.dumps(learn_workflow({str(p.get('goal') or '')!r},{base!r}),indent=2))")
        return [py, "-u", "-c", code]
    if action == "probe":
        code = ("import json;from harness.variants.transfer_probe import main as probe;"
                f"print(json.dumps(probe({str(p.get('site_url') or 'https://books.toscrape.com/')!r}),indent=2))")
        return [py, "-u", "-c", code]
    if action == "gauntlet":        # One button: clean + all six perturbation types, headless, auto-approved.
        # Pass bar: every row pass AND extra <= 2.
        code = ("import json;from agent.replayer import run_variant;"
                "GOAL='Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days';"
                f"BASE={base!r};"
                "PERTS=[None,'shuffle','rename','modal','extra_step','throttle','composite'];"
                "rows=[];"
                "import time;"
                "t0=time.time();"
                "[rows.append((lambda p,r:{'perturb':p or 'clean','status':r.get('status'),'extra':r.get('extra_steps'),'heal':r.get('avg_time_to_heal_ms'),'detect':r.get('avg_time_to_detect_ms'),'ms':r.get('elapsed_ms')})(p,run_variant(variant=4,perturb=p,base=BASE,goal=GOAL,auto_approve=True,headless=True))) for p in PERTS];"
                "ok=all(r['status']=='pass' and (r['extra'] if isinstance(r['extra'], int) else 99)<=2 for r in rows);"
                "print(json.dumps({'status':'pass' if ok else 'fail','verdict':'gauntlet %d/7'%sum(1 for r in rows if r['status']=='pass'),'extra_steps':sum(r['extra'] or 0 for r in rows),'matrix':rows,'elapsed_ms':int((time.time()-t0)*1000)},indent=2))")
        return [py, "-u", "-c", code]
    if action == "bump":
        return [py, "-u", "-m", "agent", "propose-bump",
                "--mode", str(p.get("mode") or "good"), "--base", base]
    if action == "rollback":
        return [py, "-u", "-m", "agent", "rollback", "--to", str(p.get("to") or 1), "--base", base]
    raise ValueError(f"unknown action {action!r}")


def _drain(job: dict, offsets: dict, q: queue.Queue, force: bool = False) -> None:
    """Tail the jsonl logs, merging across files by timestamp.

    Reading file-by-file and emitting immediately would reorder the trace: within one poll
    cycle every actions.jsonl line would precede every recoveries.jsonl line regardless of
    real time, so a recovery written *before* a step's own action would arrive after it and
    be attributed to the wrong step. We buffer, sort by `ts`, and only emit events that have
    had HOLD_MS to settle so a late-written earlier event can still merge ahead of them.
    """
    counts = job.setdefault("counts", {})
    buf = job.setdefault("buf", [])
    for name in TRACE_FILES:
        path = LOG_DIR / name
        try:
            size = path.stat().st_size if path.exists() else 0
        except OSError:
            continue
        off = offsets.get(name, 0)
        if size < off:          # log truncated/rotated -> restart from 0
            off = 0
        if size == off:
            continue
        try:
            with path.open("rb") as f:
                f.seek(off)
                data = f.read()
        except OSError:
            continue
        nl = data.rfind(b"\n")
        if nl == -1:            # partial line still being written, wait for next poll
            continue
        offsets[name] = off + nl + 1
        for raw in data[:nl + 1].decode("utf-8", "replace").splitlines():
            raw = raw.strip()
            if not raw:
                continue
            try:
                ev = json.loads(raw)
            except ValueError:
                continue
            buf.append((ev.get("ts") or _now_ms(), name, ev))

    if force:
        # End of job: release everything still inside the settle window. Dropping these would
        # lose the tail of short runs (a refused goal finishes before its events age out).
        ready, job["buf"] = sorted(buf, key=lambda t: t[0]), []
    else:
        cutoff = _now_ms() - HOLD_MS
        ready = sorted([e for e in buf if e[0] < cutoff], key=lambda t: t[0])
        job["buf"] = [e for e in buf if e[0] >= cutoff]
    for ts, name, ev in ready:
        counts[name] = counts.get(name, 0) + 1
        q.put({"kind": "trace", "file": name, "event": ev, "ts": ts})


def _run_job(job: dict) -> None:
    q: queue.Queue = job["q"]
    offsets = {}
    for name in TRACE_FILES:
        p = LOG_DIR / name
        try:
            offsets[name] = p.stat().st_size if p.exists() else 0
        except OSError:
            offsets[name] = 0

    goal = job.get("goal") or ""
    if job["action"] == "run" and goal:
        try:
            _append_json(LOG_DIR / "actions.jsonl",
                         {"event": "GOAL_INTENT", "job": job["id"], "goal": goal,
                          "note": "raw goal text as submitted; parsed by plan_goal into the PLAN event",
                          "ts": _now_ms()})
        except Exception:
            pass

    q.put({"kind": "meta", "job": job["id"], "action": job["action"], "goal": goal,
           "argv": job["argv"], "ts": _now_ms()})

    if job["action"] == "run" and _plan_goal is not None:
        workflow = pathlib.Path("commands/phone_delivery_check.json").stem
        cmd_path = ROOT / "commands" / f"{workflow}.json"
        try:
            if cmd_path.exists():
                workflow = json.loads(cmd_path.read_text(encoding="utf-8")).get("workflow") or workflow
        except Exception:
            pass
        try:
            plan = _plan_goal(goal, workflow)
            q.put({"kind": "plan", "plan": plan.to_dict(), "ts": _now_ms()})
        except Exception as e:
            q.put({"kind": "plan_error", "text": f"{type(e).__name__}: {e}"})

    try:
        proc = subprocess.Popen(job["argv"], cwd=str(ROOT), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True, bufsize=1,
                                encoding="utf-8", errors="replace")
    except Exception as e:
        job.update(status="failed", ended=_now_ms())
        q.put({"kind": "error", "text": f"{type(e).__name__}: {e}"})
        q.put({"kind": "done"})
        return

    job["proc"] = proc
    reader_done = threading.Event()

    def reader():
        try:
            for line in proc.stdout:
                line = line.rstrip("\r\n")
                job["stdout"].append(line)
                q.put({"kind": "stdout", "text": line, "ts": _now_ms()})
        finally:
            reader_done.set()

    threading.Thread(target=reader, daemon=True).start()

    while not (reader_done.is_set() and proc.poll() is not None):
        _drain(job, offsets, q)
        if _now_ms() - job["started"] > JOB_TIMEOUT_MS:
            proc.kill()
            q.put({"kind": "error", "text": f"job exceeded {JOB_TIMEOUT_MS // 1000}s; killed"})
            break
        time.sleep(0.15)

    _drain(job, offsets, q, force=True)   # settle is over: emit everything, in ts order
    reader_done.wait(timeout=5)

    text = "\n".join(job["stdout"])
    job["result"] = _parse_json_blob(text)
    job["returncode"] = proc.returncode
    job["status"] = "done" if job["result"] is not None else "failed"
    job["ended"] = _now_ms()
    job["summary"] = _summarize(job)
    _append_history({**job["summary"], "result": job["result"]})
    q.put({"kind": "result", "result": job["result"], "returncode": proc.returncode,
           "status": job["status"], "ts": job["ended"]})
    q.put({"kind": "done"})


def _append_history(summary: dict) -> None:
    """Persist a run summary so recovery cost can be compared across runs."""
    try:
        _append_json(HISTORY, summary)
        lines = HISTORY.read_text(encoding="utf-8").splitlines()
        if len(lines) > HISTORY_MAX:
            HISTORY.write_text("\n".join(lines[-HISTORY_MAX:]) + "\n", encoding="utf-8")
    except Exception:
        pass


def _summarize(job: dict) -> dict:
    res = job.get("result") if isinstance(job.get("result"), dict) else {}
    counts = job.get("counts", {})
    chose = None
    c = res.get("cheapest") or {}
    if c.get("name"):
        chose = f"{c['name']} @ Rs {c['price']}"
    verdict = res.get("verdict")
    if res.get("overall") is not None:
        verdict = "guard " + ("PASS" if res["overall"] else "FAIL")
    return {
        "id": job["id"], "action": job["action"], "goal": job["goal"],
        "status": job["status"], "started": job["started"], "ended": job["ended"],
        "elapsed_ms": (job["ended"] or job["started"]) - job["started"],
        "returncode": job.get("returncode"),
        "recoveries": counts.get("recoveries.jsonl", 0),
        "result_status": res.get("status"),
        "failed_constraint": res.get("failed_constraint"),
        "extra_steps": res.get("extra_steps"),
        "detect_ms": res.get("avg_time_to_detect_ms"),
        "heal_ms": res.get("avg_time_to_heal_ms"),
        "verdict": verdict,
        "reason": res.get("reason") or res.get("failed_constraint"),
        "chose": chose,
    }


def _latest_job():
    with _lock:
        if not JOBS:
            return None
        return max(JOBS.values(), key=lambda j: j["started"])


def _start_job(action: str, params: dict, goal: str) -> dict:
    params = {**params, "goal": goal}      # so _argv can never disagree with job["goal"]
    job = {"id": f"{action}-{_now_ms()}", "action": action, "params": params, "goal": goal,
           "argv": _argv(action, params), "q": queue.Queue(), "status": "running",
           "started": _now_ms(), "ended": None, "result": None, "stdout": [], "proc": None}
    with _lock:
        JOBS[job["id"]] = job
        for stale in sorted(JOBS.values(), key=lambda j: j["started"])[:-MAX_JOBS]:
            JOBS.pop(stale["id"], None)
    threading.Thread(target=_run_job, args=(job,), daemon=True).start()
    return job


# ------------------------------------------------------------------------- api
@app.get("/")
def idx():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/live")
def live_page():
    return send_from_directory(app.static_folder, "live.html")


@app.get("/api/live")
def api_live():
    try:
        return jsonify(json.loads((LOG_DIR / "live.json").read_text(encoding="utf-8")))
    except Exception:
        return jsonify({"run_id": "-", "step": "-", "status": "idle",
                        "detect_ms": 0, "heal_ms": 0, "extra_steps": 0, "elapsed_ms": 0})


@app.get("/api/state")
def api_state():
    job = _latest_job()
    return jsonify({
        "perturbation": STATE["active"],
        "mock_base": MOCK_BASE,
        "logs_dir": str(LOG_DIR),
        "job": None if job is None else {
            "id": job["id"], "action": job["action"], "status": job["status"],
            "goal": job["goal"], "started": job["started"], "ended": job["ended"],
        },
    })


@app.post("/api/plan")
def api_plan():
    """Dry-run the goal through the real planner: which workflow does it select?

    The dashboard shows this *before* a run so the operator can see the routing
    decision up front instead of inferring it from the trace afterwards. It calls
    the same planner.plan_goal() the agent calls, so the two cannot disagree.
    """
    p = request.get_json(silent=True) or {}
    goal = str(p.get("goal") or "")
    try:
        from agent.planner import plan_goal  # imported here: ROOT is on sys.path
    except Exception as e:                                    # pragma: no cover
        return jsonify({"error": f"planner unavailable: {e}"}), 500
    try:
        plan = plan_goal(goal)
    except Exception as e:                                    # pragma: no cover
        return jsonify({"error": str(e)}), 500
    d = plan.to_dict()
    supported = bool(d.get("supported", True))
    return jsonify({
        "goal": goal,
        # A refused goal keeps the *default* workflow on the Plan object, which would
        # read as "it will run the phone workflow". Report None so the UI cannot
        # imply a run that will not happen.
        "workflow": d.get("workflow") if supported else None,
        "supported": supported,
        "unsupported": d.get("unsupported", []),
        "steps": ([s.get("intent") if isinstance(s, dict) else s for s in (d.get("steps") or [])]
                  if supported else []),
        "params": d.get("params", {}) if supported else {},
        "notes": d.get("notes", []),
    })


DOC_FILES = {
    "README.md": "Overview & setup",
    "TASKS.md": "Build task list + rubric compliance",
    "DECISIONS.md": "Decision log",
    "FAILURES.md": "Honest limitations",
    "ONE-PAGER.md": "Pitch one-pager",
    "REHEARSAL.md": "Demo run-sheet",
}
_ALLOWED_DOCS = set(DOC_FILES)


@app.get("/api/docs")
def api_docs():
    """List the repo docs the dashboard can render."""
    out = []
    for name, desc in DOC_FILES.items():
        p = ROOT / name
        if p.exists():
            st = p.stat()
            out.append({"name": name, "desc": desc, "bytes": st.st_size,
                        "mtime": int(st.st_mtime * 1000)})
    return jsonify({"docs": out})


@app.get("/api/docs/<path:name>")
def api_doc(name: str):
    """Return one doc verbatim. Read-only, and restricted to the allow-list so a
    crafted path can never escape the repo root."""
    if name not in _ALLOWED_DOCS:
        return jsonify({"error": "not found"}), 404
    p = ROOT / name
    if not p.exists():
        return jsonify({"error": "not found"}), 404
    try:
        text = p.read_text(encoding="utf-8")
    except Exception as e:                                    # pragma: no cover
        return jsonify({"error": str(e)}), 500
    return jsonify({"name": name, "desc": DOC_FILES.get(name, ""),
                    "text": text, "mtime": int(p.stat().st_mtime * 1000)})


@app.get("/api/rubric")
def api_rubric():
    """Rubric coverage, read from competition.yaml so it cannot drift from the repo."""
    path = ROOT / "competition.yaml"
    if not path.exists():
        return jsonify({"error": "competition.yaml not found"}), 404
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:                                    # pragma: no cover
        return jsonify({"error": str(e)}), 500
    return jsonify({"text": text, "mtime": int(path.stat().st_mtime * 1000)})


@app.post("/api/run")
def api_run():
    p = request.get_json(silent=True) or {}
    action = str(p.get("action") or "run")
    if action not in ("run", "guard", "gauntlet", "probe", "learn", "bump", "rollback"):
        return jsonify({"error": f"unknown action {action!r}"}), 400
    active = _latest_job()
    if active and active["status"] == "running":
        return jsonify({"error": f"job {active['id']} is still running; wait for it to finish"}), 409
    try:
        job = _start_job(action, p, str(p.get("goal") or ""))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"id": job["id"], "action": job["action"], "argv": job["argv"]})


@app.get("/api/history")
@app.get("/api/history/<job_id>")
def api_history(job_id: str | None = None):
    """Run history for cross-run recovery-cost comparison. The list omits the full result."""
    if not HISTORY.exists():
        if job_id:
            return jsonify({"error": "unknown run"}), 404
        return jsonify({"runs": []})
    records = []
    for line in HISTORY.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except ValueError:
            continue
    if job_id:
        for rec in reversed(records):
            if rec.get("id") == job_id:
                return jsonify(rec)
        return jsonify({"error": "unknown run"}), 404
    recent = records[-50:][::-1]
    return jsonify({"runs": [{k: v for k, v in r.items() if k != "result"} for r in recent]})


@app.get("/api/run/<job_id>/stream")
def api_stream(job_id: str):
    job = JOBS.get(job_id)
    if job is None:
        return jsonify({"error": "unknown job"}), 404

    def gen():
        q: queue.Queue = job["q"]
        while True:
            try:
                ev = q.get(timeout=15)
            except queue.Empty:
                yield ": keepalive\n\n"      # keeps proxies/browsers from timing out
                continue
            yield f"data: {json.dumps(ev)}\n\n"
            if ev.get("kind") == "done":
                break

    return Response(gen(), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "Connection": "keep-alive",
                             "X-Accel-Buffering": "no"})


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    print(f"SENTRY console + dashboard on http://127.0.0.1:{a.port}  (repo root {ROOT})")
    app.run(host="127.0.0.1", port=a.port, threaded=True, debug=False)
