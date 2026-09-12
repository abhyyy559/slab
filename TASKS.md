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
- [ ] Medicine-finder swap: pharmacy + clinic mocks replace phone v0; re-verify v1 + v4 (the planner now refuses `medicine` goals with `unsupported_goal`, so lifting that refusal goes with this task)
- [x] Credibility run: same-family real HTML (books.toscrape.com), pass or honest ABSTAIN
- [ ] README architecture diagram + ONE-PAGER metrics from real logs
- [ ] Backup MP4 (≤3 min, real execution) + 5-min demo rehearsal ×2 laptops

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
