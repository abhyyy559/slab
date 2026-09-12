"""Judge perturbation console (Flask, localhost only). Live-chaos source: mocks poll /status."""
import time, json
from flask import Flask, jsonify, request

app = Flask(__name__)
STATE = {"active": None, "ts": None, "seed": 42,
         "composite": ["shuffle", "rename", "modal", "extra_step", "throttle", "strip_testids"]}

def _log(typ):
    try:
        with open("logs/actions.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"event": "PERTURB_INJECTED", "type": typ, "ts": int(time.time() * 1000)}) + "\n")
    except Exception:
        pass

@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

@app.get("/status")
def status():
    return jsonify(STATE)

def _set(typ):
    STATE.update(active=typ, ts=int(time.time() * 1000))
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
    btns = ["shuffle", "rename", "modal", "extra_step", "throttle", "composite", "reset"]
    bhtml = "".join(
        f'<button data-p="{b}" style="font-size:20px;padding:16px 24px;margin:6px;">{b}</button>' for b in btns)
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>SENTRY perturb console</title></head>
<body style="font-family:sans-serif;max-width:640px;margin:40px auto;">
<h1>SENTRY perturb console</h1>
<p>Press one. The live mock page mutates in &lt;1s. <b>reset</b> restores it.</p>
<div>{bhtml}</div>
<p id="st">state: {STATE}</p>
<script>
document.querySelectorAll('button[data-p]').forEach(b => b.onclick = async () => {{
  const r = await fetch('/perturb/' + b.dataset.p, {{method: 'POST'}});
  document.getElementById('st').textContent = 'state: ' + await r.text();
}});
</script></body></html>"""

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--port", type=int, default=8765)
    a = ap.parse_args()
    app.run(host="127.0.0.1", port=a.port)
