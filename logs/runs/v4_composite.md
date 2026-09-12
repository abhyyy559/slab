# SENTRY run — v4/composite

- **started:** 2026-09-12 16:01:55
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:55 | +1789209115742 | · PERTURB_INJECTED | target=composite · seq=0 |
| 16:01:56 | +1789209116434 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=103 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=composite |
| 16:01:56 | +1789209116434 | • step | ✓ step action: goto:search |
| 16:01:56 | +1789209116434 | ⛓ hash | HASH seq=1 6f565c69f0c3... (goto:search) |
| 16:01:57 | +1789209117487 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789209116791 · time_to_detect_ms=10 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=685 · verified=False |
| 16:01:57 | +1789209117487 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 16:01:57 | +1789209117488 | ✓ healed | ✓ HEALED in 685ms (verified=False) |
| 16:01:57 | +1789209117518 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 16:01:57 | +1789209117580 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789209117570 · time_to_detect_ms=4 · strategy=re_locate · time_to_heal_ms=5 · verified=False |
| 16:01:57 | +1789209117581 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 16:01:57 | +1789209117582 | ✓ healed | ✓ HEALED in 5ms (verified=False) |
| 16:01:57 | +1789209117607 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:57 | +1789209117627 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=20 · result=ok |
| 16:01:57 | +1789209117628 | • step | ✓ step action: click:filter |
| 16:01:57 | +1789209117628 | ⛓ hash | HASH seq=2 39b4e5c1e7f7... (click:filter) |
| 16:01:57 | +1789209117641 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:57 | +1789209117649 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:57 | +1789209117677 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=27 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:57 | +1789209117680 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:57 | +1789209117681 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 16:01:58 | +1789209118021 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789209118012 · time_to_detect_ms=4 · strategy=re_locate · time_to_heal_ms=4 · verified=False |
| 16:01:58 | +1789209118021 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 16:01:58 | +1789209118021 | ✓ healed | ✓ HEALED in 4ms (verified=False) |
| 16:01:58 | +1789209118044 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:58 | +1789209118045 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 16:01:58 | +1789209118046 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · mode=cli |
| 16:01:58 | +1789209118081 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=33 · result=ok · candidate=Redmi Note 8GB |
| 16:01:58 | +1789209118082 | • step | ✓ step action: click:check |
| 16:01:58 | +1789209118082 | ⛓ hash | HASH seq=4 988a29cfa1ed... (click:check) |
| 16:02:01 | +1789209121104 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:02:01 | +1789209121135 | 📊 metric | METRIC detect=6ms heal=231ms extra=2 status=pass |

**finished:** 2026-09-12 16:02:01 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 2 · recoveries 3

**finished:** 2026-09-12 16:02:01 — **end**
