# SENTRY run — v4/composite

- **started:** 2026-09-12 19:27:49
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:27:49 | +1789221469412 | · PERTURB_INJECTED | target=composite · seq=0 |
| 19:27:50 | +1789221470492 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=232 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=composite |
| 19:27:50 | +1789221470496 | • step | ✓ step action: goto:search |
| 19:27:50 | +1789221470506 | ⛓ hash | HASH seq=1 6f565c69f0c3... (goto:search) |
| 19:27:51 | +1789221471830 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789221470962 · time_to_detect_ms=90 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=778 · verified=False |
| 19:27:51 | +1789221471835 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 19:27:51 | +1789221471836 | ✓ healed | ✓ HEALED in 778ms (verified=False) |
| 19:27:51 | +1789221471892 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 19:27:51 | +1789221471940 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:27:51 | +1789221471958 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:27:52 | +1789221472098 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789221472034 · time_to_detect_ms=48 · strategy=re_locate · time_to_heal_ms=16 · verified=False |
| 19:27:52 | +1789221472100 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 19:27:52 | +1789221472103 | ✓ healed | ✓ HEALED in 16ms (verified=False) |
| 19:27:52 | +1789221472151 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:27:52 | +1789221472257 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=71 · result=ok |
| 19:27:52 | +1789221472258 | • step | ✓ step action: click:filter |
| 19:27:52 | +1789221472258 | ⛓ hash | HASH seq=2 b375c4911b7b... (click:filter) |
| 19:27:52 | +1789221472283 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:27:52 | +1789221472298 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:27:52 | +1789221472300 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:27:52 | +1789221472376 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=70 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:27:52 | +1789221472381 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:27:52 | +1789221472382 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 19:27:52 | +1789221472699 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:27:52 | +1789221472919 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789221472803 · time_to_detect_ms=94 · strategy=re_locate · time_to_heal_ms=20 · verified=False |
| 19:27:52 | +1789221472921 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 19:27:52 | +1789221472921 | ✓ healed | ✓ HEALED in 20ms (verified=False) |
| 19:27:52 | +1789221472969 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:27:52 | +1789221472999 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:27:52 | +1789221472999 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · mode=cli |
| 19:27:53 | +1789221473056 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=49 · result=ok · candidate=Redmi Note 8GB |
| 19:27:53 | +1789221473059 | • step | ✓ step action: click:check |
| 19:27:53 | +1789221473059 | ⛓ hash | HASH seq=4 2d6210d8d992... (click:check) |
| 19:27:56 | +1789221476085 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:27:56 | +1789221476085 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:27:56 | +1789221476126 | 📊 metric | METRIC detect=77ms heal=271ms extra=2 status=pass |

**finished:** 2026-09-12 19:27:56 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 2 · recoveries 3

**finished:** 2026-09-12 19:27:56 — **end**
