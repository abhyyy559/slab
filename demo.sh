#!/usr/bin/env bash
# SENTRY demo launcher: starts the mock sites and the judge console + dashboard.
#   ./demo.sh              both servers, then opens the dashboard in a new tab
#   OPEN=0 ./demo.sh       don't open a browser (CI / already have it open)
#   PORT_MOCKS=9000 ./demo.sh
#   PYTHON=/path/to/python ./demo.sh
#   NOAUTO=1 ./demo.sh     start only the mock sites, not the console
set -uo pipefail
cd "$(dirname "$0")" || exit 1

PORT_MOCKS="${PORT_MOCKS:-8000}"
PORT_CONSOLE="${PORT_CONSOLE:-8765}"

# Git Bash does not read the Windows "App Paths" registry, so `python`/`py` are often
# missing from PATH even when Python is installed. Probe for an interpreter that
# actually has this project's dependencies.
find_python() {
  local c
  for c in "${PYTHON:-}" python3 python py; do
    if [ -n "$c" ] && command -v "$c" >/dev/null 2>&1 && "$c" -c "import playwright, flask" >/dev/null 2>&1; then
      printf '%s\n' "$c"; return 0
    fi
  done
  local p
  for p in "$LOCALAPPDATA"/Programs/Python/Python3*/python.exe \
           "$HOME"/AppData/Local/Programs/Python/Python3*/python.exe \
           /c/Python3*/python.exe; do
    if [ -x "$p" ] && "$p" -c "import playwright, flask" >/dev/null 2>&1; then
      printf '%s\n' "$p"; return 0
    fi
  done
  return 1
}

if ! PY="$(find_python)"; then
  echo "No Python with playwright + flask found." >&2
  echo "Install them, then re-run:" >&2
  echo "  <python> -m pip install -r requirements.txt" >&2
  echo "  <python> -m playwright install chromium" >&2
  echo "Or point at one explicitly:  PYTHON=/c/path/to/python.exe ./demo.sh" >&2
  exit 1
fi

echo "python : $PY"
"$PY" -c "import sys, playwright, flask; print('         python ' + sys.version.split()[0] + ', playwright + flask OK')"

# MSYS `kill` cannot reliably terminate native Windows processes (python.exe), which
# leaves a server holding the port after Ctrl-C. Escalate to taskkill when needed.
kill_tree() {
  local pid="$1"
  [ -n "$pid" ] || return 0
  kill "$pid" 2>/dev/null
  sleep 0.3
  if kill -0 "$pid" 2>/dev/null; then kill -9 "$pid" 2>/dev/null; fi
  if kill -0 "$pid" 2>/dev/null && command -v taskkill >/dev/null 2>&1; then
    taskkill //F //T //PID "$pid" >/dev/null 2>&1
  fi
}

MOCK_PID=""
CONSOLE_PID=""
cleanup() {
  echo
  echo "shutting down..."
  kill_tree "$MOCK_PID"
  kill_tree "$CONSOLE_PID"
  wait 2>/dev/null
  exit 0
}
trap cleanup INT TERM

"$PY" mocks/serve.py --port "$PORT_MOCKS" &
MOCK_PID=$!
"$PY" harness/console/app.py --port "$PORT_CONSOLE" &
CONSOLE_PID=$!

deadline=$((SECONDS + 25))
until "$PY" -c "
import sys, urllib.request
for u in ('http://127.0.0.1:$PORT_MOCKS/site_a/search.html', 'http://127.0.0.1:$PORT_CONSOLE/status'):
    urllib.request.urlopen(u, timeout=2).read()
" >/dev/null 2>&1; do
  if [ "$SECONDS" -ge "$deadline" ]; then
    echo "servers did not come up in time; see output above" >&2
    cleanup
  fi
  sleep 0.4
done

echo
echo "  mocks + storefronts : http://127.0.0.1:$PORT_MOCKS/site_a/search.html"
echo "  dashboard           : http://127.0.0.1:$PORT_CONSOLE"
echo
echo "Ctrl-C to stop both."

if [ "${OPEN:-1}" = "1" ]; then
  # Reuse a single named tab so re-running the demo does not pile up dashboard tabs.
  "$PY" -c "
import webbrowser
try:
    webbrowser.open('http://127.0.0.1:$PORT_CONSOLE', new=2)
except Exception:
    pass
" >/dev/null 2>&1 || true
fi

wait
