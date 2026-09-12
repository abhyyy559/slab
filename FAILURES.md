# FAILURES.md — honest, updated per run

- Open-domain transfer: not supported. Reason: command store is site-specific.
- Learn/version-bump loop: not demonstrated. Reason: no learn→replay→heal→version-bump logs exist yet; `learner.py`/`reflect.py` are stubs. Pitch cut until 3+ logged trials.
- Variant 1 end-to-end: VERIFIED 2026-09-12 (Python 3.11.9, Playwright chromium, mocks :8000): `status: pass`, Pixel Lite 8GB Rs 18999, delivery available to 500001, 2 extractive evidence rows, APPROVAL_REQUESTED+GRANTED, hash chain in logs/. See last_run.json + evidence.html.
- Perturbed recovery (modal/extra-step/throttle): unbuilt. Reason: detector/recovery ladder + console wiring land only after variant 1 passes (Phase 2).
- Real-site credibility run (books.toscrape.com): not done. Reason: blocked behind variant 1.
