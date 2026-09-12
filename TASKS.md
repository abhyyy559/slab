# TASKS.md — SENTRY build task list (one by one, no new work until checked items pass)

## Legend
- [x] done + verified (log committed) · [ ] open · [~] in progress

## Phase 0 — Environment (done)
- [x] Python 3.11.9 + Playwright chromium on build machine
- [x] `node --check` on `mocks/chaos.js` after every edit (false-negative lesson)

## Phase 1 — Core loop (done)
- [x] webcmd kill-gate PASSED (mandatory): adapters `voltkart/search` + `swiftship/check` verified live; `python -m agent learn` works; sources in `adapters/`
- [x] Repo skeleton (§4) + reset/docs/competition.yaml
- [x] Mocks served (`/site_a/search.html`, `/site_b/check.html`)
- [x] Executor (hash chain) + grounder (5-signal, tau=0.70)
- [x] Replayer vs hand-authored `commands/phone_delivery_check.json`
- [x] Variant 1 verified: pass, 0 extra steps

## Jury cuts (done)
- [x] CHAOS agent killed; adversary = judge + console
- [x] Reframe: recovery engine, benchmarked on medicine-finder (phone JSON = v0 placeholder)
- [x] evidence-board/ killed → `evidence.html` plain table + `build_evidence.py`
- [x] "Learning" cut from pitch (stubs, no logs) → FAILURES.md owns the honesty
- [x] FAILURES.md created + growing
- [x] Load-bearing goal: B confirms deliverable-within-3-days determines A's choice
- [x] Approval = browser modal (CLI fallback)

## Phase 2 — Recovery (done)
- [x] chaos.js transport (console poll 600ms + `?perturb=` deterministic)
- [x] Detector (scan + postcondition) + recovery ladder (confirm-first, synonym re-ground, backtrack)
- [x] Replayer integration: HASH on stdout, recovery-cost counting, metrics trials
- [x] Variant 4 composite verified: pass, 2 extra, detect ~3ms, heal ~157ms

## Now — Demo polish (in progress)
- [x] Polish Site A / Site B UI (VoltKart + SwiftShip; DOM contracts kept)
- [x] Re-verify v1 + composite on polished mocks (v1: 0 extra; v4: 2 extra)
- [x] Demo run for review: screenshots + log walkthrough (this session)
- [x] Storefront restyle v2 (VoltKart + SwiftShip): contracts frozen, sticky chrome below chaos overlays, empty-state on zero matches; evidence snippet no longer the thumbnail emoji
- [x] Re-verify after v2: full guard green (v1 pass/0, v2 pass/0, v3 ABSTAIN, v4 pass/2 extra, v6 ABSTAIN); last_run.json + evidence.html regenerated
- [x] Judge console → **dashboard** (`harness/console`): task box, 5 scenario presets, param overrides, headed/approval toggles, live SSE trace tailed from `logs/*.jsonl`, result card with evidence, chaos injector. Runs the agent as a subprocess (Playwright sync API is not usable in a Flask thread). `/status` shape frozen; 22 endpoint checks + 7 chaos-click checks green.
- [x] `demo.sh` one-command launcher: finds a Python with playwright+flask (Git Bash misses the Windows App Paths registry), starts both servers, Ctrl-C stops both. Shutdown escalates to `taskkill` because MSYS `kill` cannot reliably terminate native `python.exe` (leaked a server holding :8000 in testing).
- [x] Goal now drives the plan: `planner.plan_goal()` extracts budget / RAM / PIN and routes to a workflow, logged as a `PLAN` event. Precedence: explicit flags > goal params > command defaults. Unknown domains (medicine / travel / groceries) return `ABSTAIN / unsupported_goal` instead of silently running the phone workflow. Guard re-verified green.

## Next — one by one, in order
- [x] Infeasible variant (+1): budget 8000 + 12GB → ABSTAIN naming `max_price AND min_ram` (verified)
- [x] Regression-guard + rollback: guard v1/v2/v3/v4/v6, good ACCEPTED v1→v2, bad REJECTED, rollback→v1 green; `logs/versions.jsonl` (verified). Re-run green after storefront restyle v2. Un-cutting "learning" from the pitch is still an owner call.
- [x] Run history: summaries persisted to `logs/dashboard-runs.jsonl` (goal, outcome, extra steps, detect/heal, recoveries), `/api/history` + `/api/history/<id>`, dashboard panel with cross-run recovery-cost comparison; click a row to reload its result card.

## Production hardening pass (2026-09-12)
- [x] **Visible window fix** (`agent/browser.py`): headed runs now open a real, maximized, foreground window on the current screen, hold it open after the run (`--keep-open`, default 6s), and slow to a legible pace (`--slowmo`, default 250ms). New flags: `--headed/--slowmo/--keep-open/--no-raise/--channel`.
- [x] **Chaos engine expanded** (`mocks/chaos.js`): rename, strip, move, attrs, modal, extra_step, throttle, ab, swap, composite, chaos_max. Deterministic (`?perturb=`) + judge-operated (600ms poll, now racing-safe).
- [x] **Structural grounding** (`agent/grounder.py`): 5-signal fusion now falls back to ARIA role + accessible name + label association + synonym table when test ids are stripped/renamed. `discover()` for structure-first control lookup.
- [x] **Adaptive waits** (`agent/detector.py`): `settle()` (DOM-quiet) + `wait_for_post()` (poll to deadline) replace fixed sleeps — this fixed the judge-operated live-injection ABSTAIN (chaos lands ~600ms after load, a fixed 300ms sleep raced it).
- [x] **Mock sites hardened**: controls carry `aria-label`/`role`/landmark structure; page-side JS reads structurally (`#fmax`/`#fmin`, `pinEl()`, `statusEl()`) so a testid strip no longer breaks the site's own logic.
- [x] **Test suite**: 40 fast unit tests (`test_chaos_engine.py`, `test_grounding.py`, upgraded `test_mock_contracts.py`) + 21 live adaptive-battery tests (`test_adaptive_live.py`) covering every perturbation end-to-end. All green.
- [x] Console: generic `/perturb/<type>` injector, `/api/perturbations` catalogue, 12 chaos buttons, new presets (chaos_max, strip), slow-mo/keep-open inputs.

## Track 01 rubric compliance (2026-09-12, "it should follow all this rule strictly")
Audit of the codebase against every bullet of the official brief, then gap-closing.

- [x] **Accept a plain-language goal** — `planner.plan_goal()` parses budget/RAM/PIN/brand from free text; unsupported domains ABSTAIN with `unsupported_goal` rather than silently running the wrong workflow.
- [x] **Cross-site workflow that hands data from one site to another** — Site A's chosen product becomes Site B's enquiry subject (`?product=`), and Site B's delivery answer determines Site A's choice (loop, not hop).
- [x] **Rubric's literal example goal** ("submit an enquiry for it on Site B") — was NOT implemented; the old workflow stopped at a delivery check. Built `mocks/site_b/enquiry.html` + `commands/phone_fulfilment_enquiry.json` (5 steps) + `_submit_enquiry()` in the replayer + planner routing + grounder synonyms. Verified end-to-end.
- [x] **Detect unexpected state** — moved, renamed, new modal, extra step, slow load, error page: all six in `harness/perturbations.py`, all detected by `detector.scan()`.
- [x] **Recover automatically** — re-locate (ARIA role + label + synonyms) / re-plan (dismiss) / backtrack, then verify. Never proceeds on an unverified postcondition.
- [x] **Keep a readable action log** — per-run `logs/runs/<run_id>.md` transcript: every step, change, recovery and pause with timestamps (17 runs generated).
- [x] *Stretch:* **Visual + DOM grounding** — 5-signal fusion survives testid strip + rename + move via structure, not ids.
- [x] *Stretch:* **Confidence score + pause when low** — τ=0.70 gate; `--pause-on-low` calls the human instead of guessing. `LOW_CONFIDENCE_PAUSE` logged, counted in `stats.pauses`.
- [x] *Stretch:* **Dashboard replaying the run with changes highlighted** — console + live in-page overlay (`agent/highlight.py`): cyan ground / amber change / green heal / red abstain, plus chaos banner.
- [x] **Responsible design** — approval gate (browser modal, CLI fallback) before every irreversible action; enquiry write gated; no CAPTCHA/login/payments; extractive evidence only.
- [x] Tests: **87 green** (53 unit + 34 live), incl. 12 new enquiry tests across 8 answer-preserving perturbations. Verified live: pass, extra 2, detect 25ms, heal 242ms, 3 evidence rows, `SS-734303`.

## Backlog
- [ ] Medicine-finder swap: pharmacy + clinic mocks replace phone v0; re-verify v1 + v4 (the planner now refuses `medicine` goals with `unsupported_goal`, so lifting that refusal goes with this task)
- [ ] README architecture diagram + ONE-PAGER metrics from real logs
- [x] Backup MP4 (≤3 min, real execution) + 5-min demo rehearsal ×2 laptops

## How to run anything here (resources)
```bash
# install (once)
python -m pip install -r requirements.txt
python -m playwright install chromium
# terminals (repo root)
python mocks/serve.py --port 8000        # mocks
python harness/console/app.py --port 8765 # judge console + dashboard (open 127.0.0.1:8765)
./demo.sh                                 # or: both servers, then opens the dashboard (Ctrl-C stops both)
# runs
python -m agent run --goal "Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days" --variant 1 --base http://127.0.0.1:8000
python -m agent run --goal "..." --variant 4 --perturb composite --base http://127.0.0.1:8000
python build_evidence.py --in last_run.json --out evidence.html
```
