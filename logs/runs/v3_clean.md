# SENTRY run — v3/clean

- **started:** 2026-09-12 14:38:37
- **goal:** (none)

| t | ts | event | detail |
|---|---|---|---|
| 14:38:38 | +1789204118357 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=134 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 14:38:38 | +1789204118360 | • step | ✓ step action: goto:search |
| 14:38:38 | +1789204118361 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:38:38 | +1789204118765 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:38:38 | +1789204118865 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:38:38 | +1789204118941 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=73 · result=ok |
| 14:38:38 | +1789204118943 | • step | ✓ step action: click:filter |
| 14:38:38 | +1789204118945 | ⛓ hash | HASH seq=2 bff7efd767aa... (click:filter) |
| 14:38:45 | +1789204125014 | · RECOVERY · event | trigger=postcondition_failed · expected=results_filtered · observed=0_visible_cards · detected_at_ms=1789204124954 · time_to_detect_ms=0 · strategy=re_locate · time_to_heal_ms=59 · verified=False · confidence_after=0.88 |
| 14:38:45 | +1789204125014 | ⚠ recovery | ⚠ RECOVERY: postcondition_failed -> re_locate |
| 14:38:45 | +1789204125015 | ✓ healed | ✓ HEALED in 59ms (verified=False) |
| 14:38:45 | +1789204125062 | • step | ✓ step action: click:filter:retry |
| 14:38:45 | +1789204125063 | ⛓ hash | HASH seq=3 bff7efd767aa... (click:filter:retry) |
| 14:38:51 | +1789204131230 | · ABSTAIN | reason=no_results · constraint=max_price AND min_ram |

**finished:** 2026-09-12 14:38:51 — **end**
