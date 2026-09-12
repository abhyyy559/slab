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
 goal (NL)
  └─ planner.plan_goal() ── unsupported? ──→ ABSTAIN(unsupported_goal)
  └─ commands/phone_delivery_check.json (v1, learned_by: webcmd)
  └─ replayer ── executor (Playwright, headed slow_mo on stage)
       ├─ grounder: selector .35 + role_name .25 + text .20 + visual .10 + landmark .10 → conf ≥ τ=0.70
       ├─ detector: scan (modal/extra-step/rename/error) + check_post per step
       ├─ recovery: re-plan (dismiss) → re-locate (synonym re-ground) → backtrack → verify
       ├─ step 5 loop: Site B checks candidates cheapest-first (?product=), fallback or ABSTAIN
       ├─ evidence: verbatim snippet + URL + char_offset + sha256 → evidence.html
       ├─ constraints: pass/unsat → ABSTAIN names the failed constraint
       ├─ approval: browser modal (teammate clicks) / CLI fallback
       └─ logger: actions.jsonl · recoveries.jsonl · replay-hashes.jsonl · metrics.json · live.json
            → reflect: guard v1..v6 → ACCEPT (+1) / REJECT / rollback (.history/) → versions.jsonl
 judge console :8765 ── chaos.js (600ms poll) or ?perturb= ──→ page mutates
 webcmd substrate: adapters/voltkart+swiftship (learn once) · skills in .agents/
```
Entry: `python -m agent --help`. Frozen demo copy: `%LOCALAPPDATA%\sentry-demo` (no sync).

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
| Element renamed/moved | re-ground (5-signal, tau=0.70), log Recovery | VERIFIED (v4, jitter 5/5) |
| Unexpected modal / extra step | dismiss / confirm, verify postcondition | VERIFIED (v4, +2 extra) |
| Load timeout | 3s cap, snapshot fallback | VERIFIED (throttle absorbed, v4 green) |
| No eligible result | ABSTAIN naming failed constraint | VERIFIED (v6) |
| Open-domain transfer | not supported (same-family only) | published limitation |
| Baseline uses stable `data-testid`; perturbed run strips them | say so on stage | policy |

## Credibility test
Mocks are the benchmark; one run against real public HTML we did not write (books.toscrape.com or quotes.toscrape.com) is the credibility test. **Done 2026-09-12: v5 PASS** — cheapest in-stock book under £20 on unseen DOM, evidence in `logs/transfer.json`.

## Safety
No CAPTCHA solving, no login bypass, no real credentials/payments. Respects robots/ToS/rate limits. Human approval gate before irreversible actions — **browser modal** ("SENTRY wants to submit. Approve?"), teammate clicks on stage; CLI y/N is fallback only.
