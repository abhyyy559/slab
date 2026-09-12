# SENTRY — Recovery engine for browser agents (SLAB Track 01)

**Thesis:** *Replay deterministically. Heal on change. Prove every claim. Abstain when wrong.*
**Frame:** *We didn't build another shopping agent. We built the recovery layer any browser agent needs — benchmarked against a cross-site workflow under live, judge-operated UI chaos.* The benchmark is the test bench; the recovery engine is the product.
**Learn fact (20 seconds, then move on):** every run before burned effort rediscovering the same site. We ran webcmd learn once — `adapters/voltkart/search.js` + `adapters/swiftship/check.js` is what came out. Every replay since has been deterministic (`python -m agent learn` reproduces it).
**Cut from pitch:** "learning" / version-bump loop — stubs only, no logs yet (see FAILURES.md).

## Benchmark workflow (load-bearing handoff: loop, not hop)
Goal: *"Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days, and hold it for approval."* Site B's answer determines Site A's choice — cheapest *deliverable*, not cheapest listed — so the handoff is a loop, not a one-way hop.

Two workflows are selectable **by the goal text** (`planner.plan_goal`):
| Workflow | Steps | When |
|---|---|---|
| `phone_delivery_check` | 4 | default goal |
| `phone_fulfilment_enquiry` | 5 | goal mentions enquiry / contact / quote — appends an irreversible **cross-site write** on Site B |

The 5-step run is the rubric's own example ("submit an enquiry for it on Site B"): the product
chosen on Site A becomes the enquiry subject on Site B, the form is filled structurally, and the
submission goes through the same approval gate as any irreversible action. It is skipped entirely
unless delivery was positively confirmed, so we never enquire about an unverifiable product.

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
  └─ routes by goal text → phone_delivery_check.json (4 steps)
  │                      → phone_fulfilment_enquiry.json (5 steps, + cross-site write)
  └─ replayer ── browser.launch_browser() (headed = maximized, foreground, held open)
       ├─ grounder: selector .35 + role_name .25 + text .20 + visual .10 + landmark .10 → conf ≥ τ=0.70
       │            fallback when ids are stripped/renamed: ARIA role + <label for>/aria-label + SYNONYMS
       │            discover(): structure-first control lookup (no test ids required)
       ├─ detector: scan (modal/extra-step/rename/move/error) + check_post per step
       │            settle() DOM-quiet wait + wait_for_post() poll-to-deadline (absorbs async chaos)
       ├─ recovery: re-plan (dismiss) → re-locate (structural + synonym) → backtrack → verify
       │            low confidence + --pause-on-low → confidence pause, ask the human
       ├─ highlight: overlay marks ground/change/heal/abstain live in the headed window
       ├─ step 5 loop: Site B checks candidates cheapest-first (?product=), fallback or ABSTAIN
       ├─ step 5 write: enquiry.html?product=<choice> filled structurally → approval → submit → verify
       ├─ evidence: verbatim snippet + URL + char_offset + sha256 → evidence.html
       ├─ constraints: pass/unsat → ABSTAIN names the failed constraint
       ├─ approval: browser modal (teammate clicks) / CLI fallback
       ├─ transcript: logs/runs/<run_id>.md — readable step-by-step log (rubric requirement)
       └─ logger: actions.jsonl · recoveries.jsonl · replay-hashes.jsonl · metrics.json · live.json
            → reflect: guard v1..v6 → ACCEPT (+1) / REJECT / rollback (.history/) → versions.jsonl
 judge console :8765 ── chaos.js (600ms poll) or ?perturb= ──→ page mutates
 webcmd substrate: adapters/voltkart+swiftship (learn once) · skills in .agents/
```
Entry: `python -m agent --help`. Frozen demo copy: `%LOCALAPPDATA%\sentry-demo` (no sync).

## Browser window (headed / demo mode)
Headed runs are *demonstrations*, so they must be watchable:
```bash
python -m agent run --headed                                    # real, maximized, foreground window
python -m agent run --headed --slowmo 400 --keep-open 12000     # slower, holds result 12s
python -m agent run --headed --no-raise                         # don't steal focus
```
`agent/browser.py` raises the Chromium window to the top of the z-order (Win32 `SetForegroundWindow`, matched by
window class so nothing else is disturbed), lands it on the current screen, and holds the final frame open for
`--keep-open` ms (default 6000) after the run. `--slowmo` defaults to 250ms when headed. Failures degrade
gracefully instead of crashing the demo.

**Live highlighting** (on by default when headed, `--no-highlight` to disable): an injected
`#__sentry_layer` overlay draws a labelled outline around the grounded element and colour-codes the run —
cyan `ground`, amber `change`, green `heal`, red `abstain` — plus a top-centre banner when chaos is injected.
It is pointer-events-free and never touches the DOM the agent grounds against.

**Confidence pause** (`--pause-on-low`): when a step's grounding confidence falls below τ=0.70 and recovery
cannot lift it, the agent stops and asks a human (browser modal, CLI fallback) instead of guessing. Each pause
is logged as `LOW_CONFIDENCE_PAUSE` and counted in `stats.pauses`.

## Chaos / adaptive-browsing matrix
`harness/perturbations.py` is the catalogue (single source of truth, pinned by tests). Deterministic via
`--perturb <type>`, or live via the dashboard. New types: `move`, `attrs`, `strip`, `ab`, `swap`, `rename_strip`,
`chaos_max` (on top of `rename`/`modal`/`extra_step`/`throttle`/`composite`).

| Type | What changes | Agent's fallback signal |
|---|---|---|
| `rename` | labels swapped for synonyms | role + synonym table |
| `strip` | `data-testid` removed from controls | ARIA role + `<label for>` / `aria-label` |
| `move` | controls relocated/reordered in the DOM | label association, not position |
| `attrs` | `data-*` attributes + classes mutated | text/structure, not attribute selectors |
| `modal` | blocking overlay injected | detector.scan → dismiss |
| `extra_step` | inserted confirmation interstitial | detector.scan → clear + verify |
| `throttle` | 2–2.5s response latency | `wait_for_post` polls to deadline |
| `ab` | every other result card hidden | pick from the *visible* set |
| `swap` | list re-rendered into a new container | re-discover the live list |
| `composite` | rename+strip+move+attrs+modal+extra_step+throttle | full ladder |
| `chaos_max` | everything incl. ab + swap | full ladder (may ABSTAIN honestly) |

`ab`/`chaos_max` can remove every eligible candidate; the agent then ABSTAINs naming the failed constraint — the
correct answer, not a failure. See DECISIONS.md.

## Tests
```bash
python -m pytest harness/regression -q                  # fast unit + live battery (skips if mocks down)
python -m pytest harness/regression -q -k "not live"    # unit only, no browser
```
Unit: `test_mock_contracts.py` (id + structure contracts for both sites incl. `enquiry.html`),
`test_enquiry_workflow.py` (planner routing + command-file contracts for both workflows),
`test_chaos_engine.py` (catalogue ↔ chaos.js parity, rename ↔ synonym parity), `test_grounding.py`
(grounder/detector/constraints), `test_constraints.py` (negative-match). Live: `test_adaptive_live.py`
runs the real agent against every perturbation for **both** workflows and asserts pass-or-honest-ABSTAIN
— never a false pass. **87 tests, all green 2026-09-12** (53 fast unit + 34 live, 216s).

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

**Readable action log (rubric requirement):** every run also writes `logs/runs/<run_id>.md` — a human-readable
transcript with timestamps listing every step, each detected change (`CHANGE`), each recovery (`RECOVERY`) and
any confidence pause (`PAUSE`). Path overridable with `SENTRY_TRANSCRIPT`. This is the artifact to hand a judge
who wants to read what happened without parsing JSONL.

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
