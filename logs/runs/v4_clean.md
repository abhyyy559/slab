# SENTRY run — v4/clean

- **started:** 2026-09-12 15:06:32
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 15:06:33 | +1789205793479 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=104 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 15:06:33 | +1789205793483 | • step | ✓ step action: goto:search |
| 15:06:33 | +1789205793486 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 15:06:34 | +1789205794640 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789205793889 · time_to_detect_ms=27 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=719 · verified=False |
| 15:06:34 | +1789205794642 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 15:06:34 | +1789205794646 | ✓ healed | ✓ HEALED in 719ms (verified=False) |
| 15:06:34 | +1789205794722 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 15:06:34 | +1789205794891 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789205794862 · time_to_detect_ms=16 · strategy=re_locate · time_to_heal_ms=10 · verified=False |
| 15:06:34 | +1789205794892 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 15:06:34 | +1789205794894 | ✓ healed | ✓ HEALED in 10ms (verified=False) |
| 15:06:34 | +1789205794958 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:06:35 | +1789205795030 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=65 · result=ok |
| 15:06:35 | +1789205795039 | • step | ✓ step action: click:filter |
| 15:06:35 | +1789205795042 | ⛓ hash | HASH seq=2 39b4e5c1e7f7... (click:filter) |
| 15:06:35 | +1789205795069 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:06:35 | +1789205795089 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:06:35 | +1789205795160 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=65 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:06:35 | +1789205795166 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:06:35 | +1789205795168 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 15:06:35 | +1789205795580 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789205795561 · time_to_detect_ms=7 · strategy=re_locate · time_to_heal_ms=7 · verified=False |
| 15:06:35 | +1789205795581 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 15:06:35 | +1789205795582 | ✓ healed | ✓ HEALED in 7ms (verified=False) |
| 15:06:35 | +1789205795646 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:06:35 | +1789205795653 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:06:35 | +1789205795662 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 15:06:35 | +1789205795722 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=52 · result=ok · candidate=Redmi Note 8GB |
| 15:06:35 | +1789205795727 | • step | ✓ step action: click:check |
| 15:06:35 | +1789205795730 | ⛓ hash | HASH seq=4 988a29cfa1ed... (click:check) |
| 15:06:37 | +1789205797733 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:06:37 | +1789205797778 | 📊 metric | METRIC detect=16ms heal=245ms extra=2 status=pass |

**finished:** 2026-09-12 15:06:37 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 2 · recoveries 3

**finished:** 2026-09-12 15:06:37 — **end**
