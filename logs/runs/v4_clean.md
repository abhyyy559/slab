# SENTRY run — v4/clean

- **started:** 2026-09-12 19:41:30
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:41:32 | +1789222292579 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=254 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 19:41:32 | +1789222292596 | • step | ✓ step action: goto:search |
| 19:41:32 | +1789222292596 | ⛓ hash | HASH seq=1 001b85ac14fe... (goto:search) |
| 19:41:34 | +1789222294123 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789222293172 · time_to_detect_ms=61 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=890 · verified=False |
| 19:41:34 | +1789222294123 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 19:41:34 | +1789222294138 | ✓ healed | ✓ HEALED in 890ms (verified=False) |
| 19:41:34 | +1789222294341 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 19:41:34 | +1789222294393 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:41:34 | +1789222294428 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:41:34 | +1789222294560 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789222294522 · time_to_detect_ms=20 · strategy=re_locate · time_to_heal_ms=16 · verified=False |
| 19:41:34 | +1789222294560 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 19:41:34 | +1789222294560 | ✓ healed | ✓ HEALED in 16ms (verified=False) |
| 19:41:34 | +1789222294621 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:41:34 | +1789222294694 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=67 · result=ok |
| 19:41:34 | +1789222294695 | • step | ✓ step action: click:filter |
| 19:41:34 | +1789222294695 | ⛓ hash | HASH seq=2 39b4e5c1e7f7... (click:filter) |
| 19:41:34 | +1789222294714 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:41:34 | +1789222294724 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:41:34 | +1789222294731 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:41:34 | +1789222294814 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=80 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:41:34 | +1789222294816 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:41:34 | +1789222294818 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 19:41:35 | +1789222295145 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:41:35 | +1789222295307 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789222295273 · time_to_detect_ms=18 · strategy=re_locate · time_to_heal_ms=16 · verified=False |
| 19:41:35 | +1789222295310 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 19:41:35 | +1789222295310 | ✓ healed | ✓ HEALED in 16ms (verified=False) |
| 19:41:35 | +1789222295367 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:41:35 | +1789222295369 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:41:35 | +1789222295371 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 19:41:35 | +1789222295432 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=59 · result=ok · candidate=Redmi Note 8GB |
| 19:41:35 | +1789222295439 | • step | ✓ step action: click:check |
| 19:41:35 | +1789222295440 | ⛓ hash | HASH seq=4 988a29cfa1ed... (click:check) |
| 19:41:37 | +1789222297471 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:41:37 | +1789222297479 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:41:37 | +1789222297522 | 📊 metric | METRIC detect=33ms heal=307ms extra=2 status=pass |

**finished:** 2026-09-12 19:41:37 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 2 · recoveries 3

**finished:** 2026-09-12 19:41:37 — **end**
