# SENTRY — Self-healing Evidence-backed Browser Agent (SLAB Track 01)

**Thesis:** *Learn once. Replay forever. Heal on change. Prove every claim. Abstain when wrong.*

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate  |  Linux/mac: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python mocks/serve.py --port 8000
python -m agent run --goal "Find cheapest phone >=8GB RAM under Rs 20000, confirm delivery to PIN 500001" --variant 1
```

## Architecture
```
NL goal -> planner -> commands/*.json -> replayer -> executor (Playwright)
                          |                |-> grounder (5-signal confidence, tau=0.70)
                          |                |-> detector (ChangeDetected) -> recovery (re-locate/re-plan/backtrack)
                          |-> evidence (extractive snippets) -> evidence-board/
                          |-> constraints (pass/fail/unsat + ABSTAIN) -> approval gate (HITL)
                          |-> logger (actions/recoveries/hashes/metrics) -> reflect (version bump + regression + rollback)
Judge console: harness/console (localhost:8765) injects shuffle/rename/modal/extra_step/throttle/composite.
Mocks: mocks/site_a (search/filter/results/product), mocks/site_b (PIN delivery check).
```

## Models / APIs used
- Planner/grounding assist: (declare here, e.g. `none/keyless-first` or `model: <name>`). No LLM in hot replay loop.
- Automation: Playwright (sync API) + webcmd (or hand-authored command JSON fallback per kill-gate).
- Data: JSON command store, JSONL logs, static HTML evidence board.
- Server: Flask judge console (localhost only) + static mock server.
- Declared libs: see `requirements.txt`. Declared templates: `commands/*.json` provenance field.

## Layout
See spec §4. Entry: `python -m agent --help`.

## Logs / Traces
`logs/actions.jsonl`, `logs/recoveries.jsonl`, `logs/replay-hashes.jsonl`, `logs/metrics.json` from at least one full run.

## Safety
No CAPTCHA solving, no login bypass, no real credentials/payments. Respects robots/ToS/rate limits. Human approval gate before irreversible actions.
