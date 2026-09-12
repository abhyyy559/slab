# SENTRY — Recovery engine for browser agents (SLAB Track 01)

**Thesis:** *Replay deterministically. Heal on change. Prove every claim. Abstain when wrong.*
**Frame:** *We didn't build another shopping agent. We built the recovery layer any browser agent needs — benchmarked against a cross-site workflow under live, judge-operated UI chaos.* The benchmark is the test bench; the recovery engine is the product.
**Learn fact (20 seconds, then move on):** every run before burned effort rediscovering the same site. We ran webcmd learn once — `adapters/voltkart/search.js` + `adapters/swiftship/check.js` is what came out. Every replay since has been deterministic (`python -m agent learn` reproduces it).
**Cut from pitch:** "learning" / version-bump loop — stubs only, no logs yet (see FAILURES.md).

## Benchmark workflow (load-bearing handoff: loop, not hop)
Goal: *"Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days, and hold it for approval."* Site B's answer determines Site A's choice — cheapest *deliverable*, not cheapest listed. Current `commands/phone_delivery_check.json` is the v0 phone-shaped placeholder; medicine swap lands once variant 1 verifies on a Python 3.11 machine.

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate  |  Linux/mac: source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
python mocks/serve.py --port 8000
python harness/console/app.py --port 8765   # then open http://127.0.0.1:8765
python -m agent run --goal "Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days" --variant 1
```

## Architecture
```
NL goal -> planner -> commands/*.json -> replayer -> executor (Playwright)
                          |                |-> grounder (5-signal confidence, tau=0.70)
                          |                |-> detector (ChangeDetected) -> recovery (re-locate/re-plan/backtrack)
                          |-> evidence (extractive snippets) -> evidence.html (plain table, generated)
                          |-> constraints (pass/fail/unsat + ABSTAIN) -> approval gate (browser modal; CLI fallback)
                          |-> logger (actions/recoveries/hashes/metrics). learner/reflect: CUT from pitch (stubs).
Judge console + dashboard: `harness/console` (localhost:8765) injects shuffle/rename/modal/extra_step/throttle/composite **and** runs the agent with a live step trace. Open http://127.0.0.1:8765 for scenario presets, parameter overrides, a headed/approval toggle, a step-by-step timeline tailed from `logs/*.jsonl`, and the result card. The agent runs as a subprocess (Playwright's sync API cannot run inside a Flask worker thread). The task box is parsed by `planner.plan_goal()` into budget / RAM / PIN and mapped to a workflow, logged as a `PLAN` event; explicit parameters override it, and unknown domains ABSTAIN with `unsupported_goal` rather than silently running the phone workflow. One workflow only — see FAILURES.md.
Mocks: mocks/site_a (search/filter/results/product), mocks/site_b (PIN delivery check).
```

## Models / APIs used
- Planner/grounding assist: (declare here, e.g. `none/keyless-first` or `model: <name>`). No LLM in hot replay loop.
- Automation: Playwright (sync API) + webcmd site adapters (`voltkart/search`, `swiftship/check` — sources in `adapters/`, kill-gate PASSED 2026-09-12).
- Data: JSON command store, JSONL logs, evidence.html plain table (generated from JSON).
- Server: Flask judge console (localhost only) + static mock server.
- Declared libs: see `requirements.txt`. Declared templates: `commands/*.json` provenance field.

## Layout
See spec §4. Entry: `python -m agent --help`.

## Logs / Traces
`logs/actions.jsonl`, `logs/recoveries.jsonl`, `logs/replay-hashes.jsonl`, `logs/metrics.json` from at least one full run. Hash-chain head is printed to stdout as appended (visible in 3s, not buried in JSONL). `evidence.html` is a **plain table generated from JSON** (`python build_evidence.py`) — the evidence-board/ project is killed, 1h max.

## Headline metric: recovery cost
Extra steps + heal time per perturbation, averaged across the run. Nobody else owns this number.
Definitions (say verbatim if probed): detect_ms = DOM mutation → next scan (polling cadence, not reasoning); heal_ms = first detection → verified recovery (reasoning + acting).

## Failure table (honest, updated per run — full list in FAILURES.md)
| Failure | Handling | Status |
|---|---|---|
| Element renamed/moved | re-ground (5-signal, tau=0.70), log Recovery | built, unverified (no Python here) |
| Unexpected modal / extra step | dismiss / confirm, verify postcondition | planned Phase 2 |
| Load timeout | 3s cap, snapshot fallback | built, unverified |
| No eligible result | ABSTAIN naming failed constraint | built, unverified |
| Open-domain transfer | not supported (same-family only) | published limitation |
| Baseline uses stable `data-testid`; perturbed run strips them | say so on stage | policy |

## Credibility test
Mocks are the benchmark; one run against real public HTML we did not write (books.toscrape.com or quotes.toscrape.com) is the credibility test. **Done 2026-09-12: v5 PASS** — cheapest in-stock book under £20 on unseen DOM, evidence in `logs/transfer.json`.

## Safety
No CAPTCHA solving, no login bypass, no real credentials/payments. Respects robots/ToS/rate limits. Human approval gate before irreversible actions — **browser modal** ("SENTRY wants to submit. Approve?"), teammate clicks on stage; CLI y/N is fallback only.
