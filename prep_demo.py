"""SENTRY one-file demo prep. Run:  python prep_demo.py
Checks interpreter, installs deps + chromium, starts mocks (:8000) and judge
console (:8765), waits for health, runs a variant-1 sanity check, prints URLs.
Reuses servers already running on those ports. Stdlib only.
"""
import json
import shutil
import subprocess
import sys
import time
import urllib.request

ROOT = __import__("pathlib").Path(__file__).resolve().parent
MOCKS = "http://127.0.0.1:8000/site_a/search.html"
CONSOLE = "http://127.0.0.1:8765/status"
GOAL = "Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days"


def step(name):
    print(f"\n[..] {name}", flush=True)


def ok(msg="ok"):
    print(f"[ok] {msg}", flush=True)


def fail(msg):
    print(f"[FAIL] {msg}", flush=True)
    raise SystemExit(1)


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=ROOT, **kw)


def healthy(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    step("1/6 python >= 3.11")
    if sys.version_info < (3, 11):
        fail(f"need Python 3.11+, have {sys.version.split()[0]}")
    ok(f"Python {sys.version.split()[0]}")

    step("2/6 pip install -r requirements.txt")
    p = run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    if p.returncode != 0:
        fail("pip install failed:\n" + (p.stderr or p.stdout)[-1500:])
    ok("deps installed")

    step("3/6 playwright chromium")
    has_browser = False
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            exe = pw.chromium.executable_path
            import os
            has_browser = os.path.exists(exe)
    except Exception:
        pass
    if not has_browser:
        print("     installing chromium (one time, ~170MB)...", flush=True)
        p = run([sys.executable, "-m", "playwright", "install", "chromium"])
        if p.returncode != 0:
            fail("playwright install failed:\n" + (p.stderr or p.stdout)[-1500:])
    ok("chromium ready")

    step("4/6 chaos.js syntax check")
    if shutil.which("node"):
        p = run(["node", "--check", "mocks/chaos.js"])
        if p.returncode != 0:
            fail("chaos.js has a syntax error — fix before demo:\n" + (p.stderr or p.stdout)[-800:])
        ok("chaos.js parses")
    else:
        print("     node not found — skipping (playwright runs don't need it)", flush=True)

    step("5/6 servers (:8000 mocks, :8765 console)")
    import os
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    detached = 0
    if sys.platform == "win32":
        detached = getattr(subprocess, "DETACHED_PROCESS", 0) | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    jobs = [("mocks", [sys.executable, "mocks/serve.py", "--port", "8000"], MOCKS),
            ("console", [sys.executable, "harness/console/app.py", "--port", "8765"], CONSOLE)]
    for name, cmd, url in jobs:
        if healthy(url):
            print(f"     {name}: already up, reusing", flush=True)
            continue
        log = open(logs / f"prep-{name}.log", "a")
        subprocess.Popen(cmd, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                         creationflags=detached)
        deadline = time.time() + 30
        while time.time() < deadline and not healthy(url):
            time.sleep(1)
        if not healthy(url):
            fail(f"{name} did not come up — see logs/prep-{name}.log")
        print(f"     {name}: started", flush=True)
    ok("both servers healthy")

    step("6/6 sanity run (variant 1)")
    p = run([sys.executable, "-m", "agent", "run", "--goal", GOAL,
             "--variant", "1", "--base", "http://127.0.0.1:8000"])
    try:
        out = json.loads(p.stdout[p.stdout.index("{"):p.stdout.rindex("}") + 1])
    except Exception:
        fail("agent output not JSON:\n" + (p.stdout + p.stderr)[-1500:])
    if out.get("status") != "pass" or out.get("extra_steps") != 0:
        fail(f"sanity run not green: {json.dumps(out)[:400]}")
    ok(f"variant 1 PASS, 0 extra steps ({out.get('elapsed_ms')}ms)")

    print("\n================ DEMO READY ================")
    print("Storefront : http://127.0.0.1:8000/site_a/search.html")
    print("Console    : http://127.0.0.1:8765   <- press a chaos button here")
    print("Then run   : python -m agent run --goal \"" + GOAL + "\" --variant 1")
    print("Perturbed  : add  --variant 4 --perturb composite  (expect pass, +2 steps)")
    print("ABSTAIN    : --variant 6 --budget 8000 --ram 12")
    print("Stop servers with Ctrl-C in their windows (or close them).")
    print("============================================")


if __name__ == "__main__":
    main()
