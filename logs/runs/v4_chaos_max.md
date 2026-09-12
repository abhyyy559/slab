# SENTRY run — v4/chaos_max

- **started:** 2026-09-12 19:40:32
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:40:32 | +1789222232111 | · PERTURB_INJECTED | target=chaos_max · seq=0 |
| 19:40:33 | +1789222233621 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=275 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=chaos_max |
| 19:40:33 | +1789222233629 | • step | ✓ step action: goto:search |
| 19:40:33 | +1789222233629 | ⛓ hash | HASH seq=1 8c8405b93504... (goto:search) |
| 19:40:35 | +1789222235031 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789222234163 · time_to_detect_ms=55 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=809 · verified=False |
| 19:40:35 | +1789222235034 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 19:40:35 | +1789222235035 | ✓ healed | ✓ HEALED in 809ms (verified=False) |
| 19:40:35 | +1789222235170 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 19:40:35 | +1789222235219 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:40:35 | +1789222235265 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:40:35 | +1789222235544 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789222235462 · time_to_detect_ms=37 · strategy=re_locate · time_to_heal_ms=37 · verified=False |
| 19:40:35 | +1789222235544 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 19:40:35 | +1789222235551 | ✓ healed | ✓ HEALED in 37ms (verified=False) |
| 19:40:35 | +1789222235702 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:40:35 | +1789222235817 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=107 · result=ok |
| 19:40:35 | +1789222235825 | • step | ✓ step action: click:filter |
| 19:40:35 | +1789222235825 | ⛓ hash | HASH seq=2 4ecb82041d51... (click:filter) |
| 19:40:35 | +1789222235861 | · STOCK_FILTER | excluded=1 · detail=out of stock, not eligible: ['Lava Blaze 8GB'] |
| 19:40:35 | +1789222235884 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:40:35 | +1789222235892 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Oppo A 8GB@16499,iQoo Z 8GB@18999 |
| 19:40:35 | +1789222235987 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=82 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=chaos_max&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:40:35 | +1789222235996 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:40:35 | +1789222235996 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 19:40:36 | +1789222236403 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:40:36 | +1789222236703 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789222236626 · time_to_detect_ms=24 · strategy=re_locate · time_to_heal_ms=50 · verified=False |
| 19:40:36 | +1789222236707 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 19:40:36 | +1789222236722 | ✓ healed | ✓ HEALED in 50ms (verified=False) |
| 19:40:36 | +1789222236873 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:40:36 | +1789222236890 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=chaos_max&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:40:36 | +1789222236898 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=chaos_max&product=Redmi%20Note%208GB · mode=cli |
| 19:40:36 | +1789222236996 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=89 · result=ok · candidate=Redmi Note 8GB |
| 19:40:37 | +1789222237004 | • step | ✓ step action: click:check |
| 19:40:37 | +1789222237012 | ⛓ hash | HASH seq=4 988a29cfa1ed... (click:check) |
| 19:40:40 | +1789222240063 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:40:40 | +1789222240094 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:40:40 | +1789222240169 | 📊 metric | METRIC detect=38ms heal=298ms extra=2 status=pass |

**finished:** 2026-09-12 19:40:40 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 2 · recoveries 3

**finished:** 2026-09-12 19:40:40 — **end**
