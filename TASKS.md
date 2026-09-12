# TASKS.md — SENTRY build task list (one by one, no new work until checked items pass)

## Legend
- [x] done + verified (log committed) · [ ] open · [~] in progress

## Phase 0 — Environment (done)
- [x] Python 3.11.9 + Playwright chromium on build machine
- [x] `node --check` on `mocks/chaos.js` after every edit (false-negative lesson)

## Phase 1 — Core loop (done)
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

## Next — one by one, in order
- [ ] Infeasible variant (+1): budget 8000 + 12GB → ABSTAIN naming `max_price AND min_ram`
- [ ] Medicine-finder swap: pharmacy + clinic mocks replace phone v0; re-verify v1 + v4
- [ ] Credibility run: same-family real HTML (books.toscrape.com), pass or honest ABSTAIN
- [ ] Reflect: regression-guarded version bump + `rollback` demo (only then un-cut "learning")
- [ ] README architecture diagram + ONE-PAGER metrics from real logs
- [ ] Backup MP4 (≤3 min, real execution) + 5-min demo rehearsal ×2 laptops

## How to run anything here (resources)
```bash
# install (once)
python -m pip install -r requirements.txt
python -m playwright install chromium
# terminals (repo root)
python mocks/serve.py --port 8000        # mocks
python harness/console/app.py --port 8765 # judge console
# runs
python -m agent run --goal "Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days" --variant 1 --base http://127.0.0.1:8000
python -m agent run --goal "..." --variant 4 --perturb composite --base http://127.0.0.1:8000
python build_evidence.py --in last_run.json --out evidence.html
```
