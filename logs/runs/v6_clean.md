# SENTRY run — v6/clean

- **started:** 2026-09-12 14:38:53
- **goal:** (none)

| t | ts | event | detail |
|---|---|---|---|
| 14:38:54 | +1789204134190 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=82 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 14:38:54 | +1789204134191 | • step | ✓ step action: goto:search |
| 14:38:54 | +1789204134191 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:38:54 | +1789204134574 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:38:54 | +1789204134653 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:38:54 | +1789204134704 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=49 · result=ok |
| 14:38:54 | +1789204134705 | • step | ✓ step action: click:filter |
| 14:38:54 | +1789204134706 | ⛓ hash | HASH seq=2 1da7e0021f67... (click:filter) |
| 14:39:00 | +1789204140950 | · RECOVERY · event | trigger=postcondition_failed · expected=results_filtered · observed=0_visible_cards · detected_at_ms=1789204140902 · time_to_detect_ms=0 · strategy=re_locate · time_to_heal_ms=47 · verified=False · confidence_after=0.88 |
| 14:39:00 | +1789204140951 | ⚠ recovery | ⚠ RECOVERY: postcondition_failed -> re_locate |
| 14:39:00 | +1789204140952 | ✓ healed | ✓ HEALED in 47ms (verified=False) |
| 14:39:01 | +1789204141006 | • step | ✓ step action: click:filter:retry |
| 14:39:01 | +1789204141007 | ⛓ hash | HASH seq=3 1da7e0021f67... (click:filter:retry) |
| 14:39:07 | +1789204147165 | · ABSTAIN | reason=no_results · constraint=max_price AND min_ram |

**finished:** 2026-09-12 14:39:07 — **end**
