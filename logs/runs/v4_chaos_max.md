# SENTRY run — v4/chaos_max

- **started:** 2026-09-12 14:36:07
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:36:07 | +1789203967406 | · PERTURB_INJECTED | target=chaos_max · seq=0 |
| 14:36:08 | +1789203968932 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=118 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=chaos_max |
| 14:36:08 | +1789203968936 | • step | ✓ step action: goto:search |
| 14:36:08 | +1789203968938 | ⛓ hash | HASH seq=1 9b9152b2d684... (goto:search) |
| 14:36:10 | +1789203970197 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789203969340 · time_to_detect_ms=46 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=805 · verified=False |
| 14:36:10 | +1789203970199 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 14:36:10 | +1789203970201 | ✓ healed | ✓ HEALED in 805ms (verified=False) |
| 14:36:10 | +1789203970294 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 14:36:10 | +1789203970427 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789203970385 · time_to_detect_ms=16 · strategy=re_locate · time_to_heal_ms=22 · verified=False |
| 14:36:10 | +1789203970429 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 14:36:10 | +1789203970433 | ✓ healed | ✓ HEALED in 22ms (verified=False) |
| 14:36:10 | +1789203970501 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:36:10 | +1789203970558 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=53 · result=ok |
| 14:36:10 | +1789203970565 | • step | ✓ step action: click:filter |
| 14:36:10 | +1789203970567 | ⛓ hash | HASH seq=2 97ec2c2f8fbc... (click:filter) |
| 14:36:10 | +1789203970581 | · ABSTAIN | reason=no_results · constraint=max_price AND min_ram |

**finished:** 2026-09-12 14:36:10 — **end**
