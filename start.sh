#!/usr/bin/env bash
# SENTRY locked runtime: start both servers detached (survive terminal close),
# verify health, print URLs. One command: ./start.sh
# Env: PYTHON=/path/to/python ./start.sh | PORT_MOCKS=8000 PORT_CONSOLE=8765 ./start.sh
set -u
cd "$(dirname "$0")" || exit 1
PORT_MOCKS="${PORT_MOCKS:-8000}"
PORT_CONSOLE="${PORT_CONSOLE:-8765}"

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
  echo "  <python> -m pip install -r requirements.txt" >&2
  exit 1
fi
echo "python: $PY"
mkdir -p logs

already_up() { "$PY" -c "
import sys, urllib.request
try:
    urllib.request.urlopen('$1', timeout=3).read()
except Exception:
    sys.exit(1)
" >/dev/null 2>&1; }

for spec in "mocks:$PORT_MOCKS:mocks/serve.py --port $PORT_MOCKS" "console:$PORT_CONSOLE:harness/console/app.py --port $PORT_CONSOLE"; do
  name="${spec%%:*}"; rest="${spec#*:}"; port="${rest%%:*}"; cmd="${rest#*:}"
  if already_up "http://127.0.0.1:$port/$([ "$name" = mocks ] && echo site_a/search.html || echo status)"; then
    echo "$name : already up on :$port, reusing"
    continue
  fi
  # shellcheck disable=SC2086
  nohup $PY $cmd > "logs/start-$name.log" 2>&1 < /dev/null &
  # no disown: trailing `wait` keeps this script (and the container) alive.
  echo "$name : starting (logs/start-$name.log)"
done

deadline=$((SECONDS + 30))
ok=1
until already_up "http://127.0.0.1:$PORT_MOCKS/site_a/search.html" && already_up "http://127.0.0.1:$PORT_CONSOLE/status"; do
  if [ "$SECONDS" -ge "$deadline" ]; then ok=0; break; fi
  sleep 1
done
if [ "$ok" = 1 ]; then
  echo "DEMO READY  mocks http://127.0.0.1:$PORT_MOCKS/site_a/search.html  console http://127.0.0.1:$PORT_CONSOLE"
else
  echo "FAILED to bring up servers; see logs/start-*.log" >&2
  exit 1
fi
# Hold the foreground so containers (and `wait`-based supervisors) stay alive.
wait
