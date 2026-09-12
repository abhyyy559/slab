# SENTRY — Recovery engine for browser agents (SLAB Track 01)

**Thesis:** *Replay deterministically. Heal on change. Prove every claim. Abstain when wrong.*
**Frame:** *We didn't build another shopping agent. We built the recovery layer any browser agent needs — benchmarked against a cross-site workflow under live, judge-operated UI chaos.* The benchmark is the test bench; the recovery engine is the product.

## Benchmark workflow (load-bearing handoff: loop, not hop)
Goal: *"Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days, and hold it for approval."* Site B's answer determines Site A's choice — cheapest *deliverable*, not cheapest listed. Current `commands/phone_delivery_check.json` is the v0 phone-shaped placeholder; medicine swap lands once variant 1 verifies.

## Setup
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate  |  Linux/mac: source .venv/bin/activate
pip install -r requirements.txt
# Ensure WebCMD CLI is installed and running
webcmd doctor
python mocks/serve.py --port 8000
python -m agent run --goal "Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days" --variant 1
```

## How we use WebCMD (Mandatory Browser & Memory Layer)

WebCMD is the exclusive browser control and knowledge persistence engine across SENTRY. No raw Playwright or Selenium processes run directly in the agent loop.

1. **Session & Profile Hygiene**:
   - Each run dynamically creates an isolated WebCMD session (`webcmd session create <name> -f json` with `--profile` scoping).
   - All subsequent browser navigation, fills, clicks, and evaluations pass the immutable session ID (`webcmd --session <id> browser run ...`).
   - Every session creation and teardown is guarded by `try / finally` and logged to `logs/actions.jsonl` as `SESSION_CREATED` and `SESSION_CLOSED` events for full auditability.

2. **Browser Action Execution**:
   - Browser actions (`goto`, `click`, `fill`, `press`, `evaluate`) execute via `webcmd browser run --stdin --no-snapshot-diff -f json`.
   - JavaScript programs execute in WebCMD's QuickJS sandbox driving the Cloak browser daemon.
   - Every action computes SHA-256 pre- and post-state hashes (`state_before_hash`, `state_after_hash`) to maintain a tamper-evident audit trail.

3. **Layer-1 Sitemap Memory Integration**:
   - WebCMD's durable sitemap memory (`webcmd site memory context`, `webcmd site note`) stores verified page routes, stable landmarks, and interaction contracts.
   - SENTRY's `agent/grounder.py` queries WebCMD's sitemap memory as a 6th signal in its multi-signal fusion algorithm (`selector`, `role_name`, `text`, `visual`, `landmark`, `sitemap_memory`), boosting locator confidence when live DOM matches verified knowledge.
   - SENTRY's `agent/detector.py` cross-checks live mutations against stored sitemap memory to detect broken interfaces early.

4. **Self-Learning Loop (Learn → Replay → Recover → Reflect)**:
   - **Learn**: `agent/learner.py` commands WebCMD to explore Site A/B, analyze actionable DOM structures, and synthesize initial workflow command templates.
   - **Replay & Recover**: `agent/replayer.py` replays the workflow with 3-tier recovery (overlay dismissal, synonym re-grounding, backtrack).
   - **Reflect**: `agent/reflect.py` absorbs verified recoveries, runs the regression guard (`harness/regression/test_guard.py`), and bumps strategy versions (`v1 -> v2`) with automatic backups and rollback support.

## Architecture
```
NL goal -> planner -> commands/*.json -> replayer -> executor (WebCMD CLI)
                          |                |-> grounder (6-signal fusion incl. WebCMD sitemap memory)
                          |                |-> detector (ChangeDetected) -> recovery (re-locate/re-plan/backtrack)
                          |-> evidence (extractive snippets) -> evidence.html (plain table, generated)
                          |-> constraints (pass/fail/unsat + ABSTAIN) -> approval gate (browser modal; CLI fallback)
                          |-> logger (actions/recoveries/hashes/metrics) -> reflect (regression-guarded version bumps)
Judge console: harness/console (localhost:8765) injects shuffle/rename/modal/extra_step/throttle/composite.
Mocks: mocks/site_a (search/filter/results/product), mocks/site_b (PIN delivery check).
```

## Models / APIs used
- Planner/grounding assist: Deterministic keyless-first rule engine (no LLM in hot replay loop).
- Automation: WebCMD CLI (`webcmd browser run/snapshot/session/memory`) exclusively driving Cloak browser daemon.
- Data: JSON command store, JSONL logs, evidence.html plain table (generated from JSON).
- Server: Flask judge console (localhost only) + static mock server.
- Declared libs: see `requirements.txt`. Declared templates: `commands/*.json` provenance field.

## Layout
See spec §4. Entry: `python -m agent --help`.

## Logs / Traces
`logs/actions.jsonl`, `logs/recoveries.jsonl`, `logs/replay-hashes.jsonl`, `logs/metrics.json` from at least one full run. Hash-chain head is printed to stdout as appended (visible in 3s, not buried in JSONL). `evidence.html` is a **plain table generated from JSON** (`python build_evidence.py`).

## Headline metric: recovery cost
Extra steps + heal time per perturbation, averaged across the run. Nobody else owns this number.
Definitions (say verbatim if probed): detect_ms = DOM mutation → next scan (polling cadence, not reasoning); heal_ms = first detection → verified recovery (reasoning + acting).

## Failure table (honest, updated per run — full list in FAILURES.md)
| Failure | Handling | Status |
|---|---|---|
| Element renamed/moved | re-ground (6-signal, tau=0.70), log Recovery | VERIFIED (WebCMD) |
| Unexpected modal / extra step | dismiss / confirm, verify postcondition | VERIFIED (WebCMD) |
| Load timeout | 3s cap, snapshot fallback | VERIFIED (WebCMD) |
| No eligible result | ABSTAIN naming failed constraint | VERIFIED (WebCMD) |
| Open-domain transfer | not supported (same-family only) | published limitation |
| Baseline uses stable `data-testid`; perturbed run strips them | say so on stage | policy |

## Credibility test
Mocks are the benchmark; one run against real public HTML we did not write (books.toscrape.com or quotes.toscrape.com) is the credibility test.

## Safety
No CAPTCHA solving, no login bypass, no real credentials/payments. Respects robots/ToS/rate limits. Human approval gate before irreversible actions — **browser modal** ("SENTRY wants to submit. Approve?"), teammate clicks on stage; CLI y/N is fallback only.

