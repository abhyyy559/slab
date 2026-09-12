# SENTRY run — v1/move

- **started:** 2026-09-12 14:32:09
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:32:09 | +1789203729693 | · PERTURB_INJECTED | target=move · seq=0 |
| 14:32:10 | +1789203730591 | · BROWSER_WINDOW | mode=headed · raised=True · slow_mo=800 · keep_open_ms=6000 · stage={'screen_w': 1536, 'screen_h': 960} |
| 14:32:11 | +1789203731504 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=910 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=move |
| 14:32:11 | +1789203731506 | • step | ✓ step action: goto:search |
| 14:32:11 | +1789203731522 | ⛓ hash | HASH seq=1 f5e3e80e25a7... (goto:search) |
| 14:32:11 | +1789203731961 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789203731912 · time_to_detect_ms=23 · strategy=re_locate · time_to_heal_ms=22 · verified=False |
| 14:32:11 | +1789203731961 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 14:32:11 | +1789203731963 | ✓ healed | ✓ HEALED in 22ms (verified=False) |
| 14:32:12 | +1789203732011 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:32:13 | +1789203733806 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789203733760 · time_to_detect_ms=30 · strategy=re_locate · time_to_heal_ms=13 · verified=False |
| 14:32:13 | +1789203733807 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 14:32:13 | +1789203733808 | ✓ healed | ✓ HEALED in 13ms (verified=False) |
| 14:32:13 | +1789203733850 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:32:14 | +1789203734775 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=900 · result=ok |
| 14:32:14 | +1789203734780 | • step | ✓ step action: click:filter |
| 14:32:14 | +1789203734785 | ⛓ hash | HASH seq=2 ac3cba021152... (click:filter) |
| 14:32:20 | +1789203740951 | · RECOVERY · event | trigger=postcondition_failed · expected=results_filtered · observed=0_visible_cards · detected_at_ms=1789203740876 · time_to_detect_ms=0 · strategy=re_locate · time_to_heal_ms=72 · verified=False · confidence_after=0.88 |
| 14:32:20 | +1789203740952 | ⚠ recovery | ⚠ RECOVERY: postcondition_failed -> re_locate |
| 14:32:20 | +1789203740954 | ✓ healed | ✓ HEALED in 72ms (verified=False) |
| 14:32:21 | +1789203741806 | • step | ✓ step action: click:filter:retry |
| 14:32:21 | +1789203741811 | ⛓ hash | HASH seq=3 f7728756c152... (click:filter:retry) |
| 14:32:28 | +1789203748030 | · ABSTAIN | reason=no_results · constraint=max_price AND min_ram |

**finished:** 2026-09-12 14:32:34 — **end**
