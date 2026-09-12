# DECISIONS

- 2026-09-12: Repo skeleton created. webcmd kill-gate pending (T+0:30). Default: hand-authored command JSON v1.
- 2026-09-12: tau=0.70 initial, calibrate on practiced variants.
- 2026-09-12: CHAOS adversary agent KILLED (jury call): doubles 6-8h scope, "red vs blue" is a trope, dilutes Task/Adaptation/Recovery (60 pts). Adversary = judge with console. Only.
- 2026-09-12: Reframe adopted: recovery engine benchmarked on medicine-finder, not a shopper. Phone command JSON = v0 placeholder; medicine swap after variant 1 verifies.
- 2026-09-12: ENV GATE first: no Python on build machine (node 22 only). No claims until variant 1 runs on Python 3.11 + `playwright install chromium`. webcmd gate runs after env gate.
- 2026-09-12: Evidence board cut to plain HTML table (90-min cap). Approval gate = browser modal (CLI fallback). Headline metric = recovery cost. Failure table started in README. Credibility test = 1 run on real public HTML (books/quotes.toscrape.com).
- 2026-09-12: ENV GATE passed: Python 3.11.9 installed locally + playwright chromium. Variant 1 VERIFIED (pass, 0 extra).
- 2026-09-12: Phase 2 done: mocks poll console /status (600ms, CORS) + ?perturb= deterministic mode; detector.scan + check_post; recovery ladder (confirm-first dismiss, synonym re-ground, backtrack) with verify; replayer integrates detect->recover, prints HASH/streaming, counts recovery cost (dismiss/backtrack/retry only). V4 composite VERIFIED: pass, 2 extra, detect 3ms, heal 157ms. False-negative caught: chaos.js syntax error made one "0-extra" pass meaningless — node --check added to workflow.
- 2026-09-12: Verification layer (read on stage): "Symptom: agent reported pass on perturbed run. Root cause: chaos.js syntax error → no injection. Fix: syntax check before every run; evidence-offset cross-check as independent verification. This is the third independent check we've added that catches the agent lying to us."
- 2026-09-12: Metric honesty: detect_ms = DOM mutation → next scan (polling cadence, not reasoning). Heal_ms = first detection → verified recovery (reasoning + acting). Say exactly this when probed.
- Venue rubric/sandbox: TODO fill in first 15 min.
