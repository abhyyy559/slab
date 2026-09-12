# SENTRY run — v6/clean

- **started:** 2026-09-12 19:23:40
- **goal:** (none)

| t | ts | event | detail |
|---|---|---|---|
| 19:23:40 | +1789221220978 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=138 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 19:23:40 | +1789221220980 | • step | ✓ step action: goto:search |
| 19:23:40 | +1789221220983 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 19:23:41 | +1789221221398 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:23:41 | +1789221221508 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:23:41 | +1789221221605 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=94 · result=ok |
| 19:23:41 | +1789221221608 | • step | ✓ step action: click:filter |
| 19:23:41 | +1789221221608 | ⛓ hash | HASH seq=2 1f2cdeb9f1d9... (click:filter) |
| 19:23:47 | +1789221227877 | · RECOVERY · event | trigger=postcondition_failed · expected=results_filtered · observed=0_visible_cards · detected_at_ms=1789221227813 · time_to_detect_ms=0 · strategy=re_locate · time_to_heal_ms=64 · verified=False · confidence_after=0.88 |
| 19:23:47 | +1789221227877 | ⚠ recovery | ⚠ RECOVERY: postcondition_failed -> re_locate |
| 19:23:47 | +1789221227882 | ✓ healed | ✓ HEALED in 64ms (verified=False) |
| 19:23:47 | +1789221227949 | • step | ✓ step action: click:filter:retry |
| 19:23:47 | +1789221227955 | ⛓ hash | HASH seq=3 1f2cdeb9f1d9... (click:filter:retry) |
| 19:23:54 | +1789221234180 | · ABSTAIN | reason=no_results · constraint=max_price AND min_ram |

**finished:** 2026-09-12 19:23:54 — **end**
