# SENTRY run — v4/ab

- **started:** 2026-09-12 14:35:52
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:35:52 | +1789203952789 | · PERTURB_INJECTED | target=ab · seq=0 |
| 14:35:54 | +1789203954397 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=114 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=ab |
| 14:35:54 | +1789203954400 | • step | ✓ step action: goto:search |
| 14:35:54 | +1789203954402 | ⛓ hash | HASH seq=1 0e8832183f4c... (goto:search) |
| 14:35:54 | +1789203954839 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:35:54 | +1789203954992 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:35:55 | +1789203955060 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=67 · result=ok |
| 14:35:55 | +1789203955067 | • step | ✓ step action: click:filter |
| 14:35:55 | +1789203955069 | ⛓ hash | HASH seq=2 bebfb364ce4b... (click:filter) |
| 14:36:01 | +1789203961149 | · RECOVERY · event | trigger=postcondition_failed · expected=results_filtered · observed=0_visible_cards · detected_at_ms=1789203961079 · time_to_detect_ms=0 · strategy=re_locate · time_to_heal_ms=55 · verified=False · confidence_after=0.88 |
| 14:36:01 | +1789203961151 | ⚠ recovery | ⚠ RECOVERY: postcondition_failed -> re_locate |
| 14:36:01 | +1789203961154 | ✓ healed | ✓ HEALED in 55ms (verified=False) |
| 14:36:01 | +1789203961203 | • step | ✓ step action: click:filter:retry |
| 14:36:01 | +1789203961206 | ⛓ hash | HASH seq=3 bebfb364ce4b... (click:filter:retry) |
| 14:36:07 | +1789203967224 | · ABSTAIN | reason=no_results · constraint=max_price AND min_ram |

**finished:** 2026-09-12 14:36:07 — **end**
