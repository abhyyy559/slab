"""Judge perturbation console (Flask, localhost only). Phase 2: wired to real DOM via query param; v1 logs + seeded stub."""
import time
from flask import Flask, jsonify, request

app = Flask(__name__)
STATE = {"active": None, "ts": None, "seed": 42}

def _log(typ):
    try:
        with open("logs/actions.jsonl", "a", encoding="utf-8") as f:
            import json
            f.write(json.dumps({"event": "PERTURB_INJECTED", "type": typ, "ts": int(time.time()*1000)}) + "\n")
    except Exception:
        pass

@app.get("/status")
def status():
    return jsonify(STATE)

def _set(typ):
    STATE.update(active=typ, ts=int(time.time()*1000))
    _log(typ)
    return jsonify(STATE)

@app.post("/perturb/shuffle")
def p_shuffle(): return _set("shuffle")
@app.post("/perturb/rename")
def p_rename(): return _set("rename")
@app.post("/perturb/modal")
def p_modal(): return _set("modal")
@app.post("/perturb/extra_step")
def p_extra(): return _set("extra_step")
@app.post("/perturb/throttle")
def p_throttle(): return _set("throttle")
@app.post("/perturb/composite")
def p_comp(): return _set("composite")
@app.post("/perturb/reset")
def p_reset(): return _set(None)

@app.get("/")
def idx():
    btns = ["shuffle","rename","modal","extra_step","throttle","composite","reset"]
    html = "<h1>SENTRY perturb console</h1>" + "".join(
        f'<form method="post" action="/perturb/{b}"><button>{b}</button></form>' for b in btns)
    return html + f"<p>{STATE}</p>"

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    app.run(host="127.0.0.1", port=a.port)
