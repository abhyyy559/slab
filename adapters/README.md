# adapters/ — webcmd site adapters (learn layer, kill-gate PASSED 2026-09-12)

Authored via `webcmd browser init <site>/<command>`, verified live against mocks.
Adapter sandbox page API = `goto` + `evaluate` + `screenshot` only (no locators) —
all DOM work happens inside `page.evaluate`. Probed 2026-09-12; don't "fix" by adding locators.

## Install (teammates)

```bash
npm install -g @agentrhq/webcmd
mkdir -p ~/.webcmd/clis/voltkart ~/.webcmd/clis/swiftship
cp adapters/voltkart/search.js ~/.webcmd/clis/voltkart/search.js
cp adapters/swiftship/check.js ~/.webcmd/clis/swiftship/check.js
webcmd voltkart search --base http://127.0.0.1:8000 -f json
webcmd swiftship check --base http://127.0.0.1:8000 -f json
```

## What each does

- `voltkart/search --base --max-price --min-ram` → in-stock product rows `[{name, price, ram}]`
- `swiftship/check --base --pin` → delivery rows `[{pin, status}]`

`agent/learner.py` wraps both; `commands/phone_delivery_check.json` provenance points here.
