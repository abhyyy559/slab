# FAILURES.md — honest, updated per run

- Open-domain transfer: not supported. Reason: command store is site-specific.
- Learn/version-bump loop: VERIFIED 2026-09-12. `agent/learner.py` explores Site A/B via WebCMD sessions and generates `commands/phone_delivery_check.json`. `agent/reflect.py` passes regression guards (`harness/regression/test_guard.py`) and bumps version (`v1 -> v2`) with backup and rollback support.
- Variant 1 end-to-end: VERIFIED 2026-09-12 (WebCMD v0.8.4 CLI, Cloak daemon, mocks :8000): `status: pass`, Pixel Lite 8GB Rs 18999, delivery available to 500001, 2 extractive evidence rows, APPROVAL_REQUESTED+GRANTED, WebCMD session lifecycle logged, SHA-256 hash chain in logs/. See last_run.json + evidence.html.
- Perturbed recovery (modal/extra-step/rename/shuffle/throttle): VERIFIED 2026-09-12 (WebCMD). Variant 4 composite: `status: pass`, 2 extra steps (both overlay dismissals), rename forces synonym re-ground (0.373 -> 0.80), sitemap memory signal verified, postconditions verified.
- Real-site credibility run (books.toscrape.com): not done. Reason: blocked behind variant 1.

