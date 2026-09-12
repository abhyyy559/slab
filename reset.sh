#!/usr/bin/env bash
set -e
# SENTRY reset: kill servers, clear logs, restore commands to v1
pkill -f "mocks/serve.py" 2>/dev/null || true
pkill -f "harness/console/app.py" 2>/dev/null || true
mkdir -p logs commands
: > logs/actions.jsonl
: > logs/recoveries.jsonl
: > logs/replay-hashes.jsonl
cat > logs/metrics.json <<'JSON'
{"replay_success_rate": "0/0", "offline_replay_success_rate": "0/0", "avg_time_to_detect_ms": null, "avg_time_to_heal_ms": null, "avg_extra_steps": null, "citation_precision": null, "transfer": null, "learning_curve": []}
JSON
echo "reset done. commands/ left untouched (v1 is source of truth)."
