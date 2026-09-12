# SENTRY run — v4/chaos_max

- **started:** 2026-09-12 15:05:53
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 15:05:53 | +1789205753395 | · PERTURB_INJECTED | target=chaos_max · seq=0 |
| 15:05:54 | +1789205754414 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=106 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=chaos_max |
| 15:05:54 | +1789205754417 | • step | ✓ step action: goto:search |
| 15:05:54 | +1789205754419 | ⛓ hash | HASH seq=1 8c8405b93504... (goto:search) |
| 15:05:55 | +1789205755525 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789205754791 · time_to_detect_ms=19 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=712 · verified=False |
| 15:05:55 | +1789205755526 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 15:05:55 | +1789205755527 | ✓ healed | ✓ HEALED in 712ms (verified=False) |
| 15:05:55 | +1789205755577 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 15:05:55 | +1789205755762 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789205755740 · time_to_detect_ms=9 · strategy=re_locate · time_to_heal_ms=11 · verified=False |
| 15:05:55 | +1789205755763 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 15:05:55 | +1789205755764 | ✓ healed | ✓ HEALED in 11ms (verified=False) |
| 15:05:55 | +1789205755824 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:55 | +1789205755863 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=36 · result=ok |
| 15:05:55 | +1789205755869 | • step | ✓ step action: click:filter |
| 15:05:55 | +1789205755872 | ⛓ hash | HASH seq=2 4ecb82041d51... (click:filter) |
| 15:05:55 | +1789205755891 | · STOCK_FILTER | excluded=1 · detail=out of stock, not eligible: ['Lava Blaze 8GB'] |
| 15:05:55 | +1789205755905 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:05:55 | +1789205755963 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=52 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=chaos_max&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:05:55 | +1789205755969 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:05:55 | +1789205755970 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 15:05:56 | +1789205756358 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789205756342 · time_to_detect_ms=5 · strategy=re_locate · time_to_heal_ms=5 · verified=False |
| 15:05:56 | +1789205756358 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 15:05:56 | +1789205756358 | ✓ healed | ✓ HEALED in 5ms (verified=False) |
| 15:05:56 | +1789205756406 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:56 | +1789205756407 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=chaos_max&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:05:56 | +1789205756411 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=chaos_max&product=Redmi%20Note%208GB · mode=cli |
| 15:05:56 | +1789205756446 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=30 · result=ok · candidate=Redmi Note 8GB |
| 15:05:56 | +1789205756453 | • step | ✓ step action: click:check |
| 15:05:56 | +1789205756456 | ⛓ hash | HASH seq=4 988a29cfa1ed... (click:check) |
| 15:05:59 | +1789205759477 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:05:59 | +1789205759503 | 📊 metric | METRIC detect=11ms heal=242ms extra=2 status=pass |

**finished:** 2026-09-12 15:05:59 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 2 · recoveries 3

**finished:** 2026-09-12 15:05:59 — **end**
