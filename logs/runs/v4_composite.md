# SENTRY run — v4/composite

- **started:** 2026-09-12 19:42:47
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 19:42:47 | +1789222367653 | · PERTURB_INJECTED | target=composite · seq=0 |
| 19:42:49 | +1789222369124 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=287 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=composite |
| 19:42:49 | +1789222369126 | • step | ✓ step action: goto:search |
| 19:42:49 | +1789222369132 | ⛓ hash | HASH seq=1 6f565c69f0c3... (goto:search) |
| 19:42:50 | +1789222370585 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789222369729 · time_to_detect_ms=66 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=786 · verified=False |
| 19:42:50 | +1789222370589 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 19:42:50 | +1789222370595 | ✓ healed | ✓ HEALED in 786ms (verified=False) |
| 19:42:50 | +1789222370753 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 19:42:50 | +1789222370812 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:42:50 | +1789222370866 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:42:51 | +1789222371139 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789222371055 · time_to_detect_ms=36 · strategy=re_locate · time_to_heal_ms=44 · verified=False |
| 19:42:51 | +1789222371139 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 19:42:51 | +1789222371145 | ✓ healed | ✓ HEALED in 44ms (verified=False) |
| 19:42:51 | +1789222371297 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:51 | +1789222371411 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=111 · result=ok |
| 19:42:51 | +1789222371411 | • step | ✓ step action: click:filter |
| 19:42:51 | +1789222371417 | ⛓ hash | HASH seq=2 39b4e5c1e7f7... (click:filter) |
| 19:42:51 | +1789222371467 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:42:51 | +1789222371497 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:42:51 | +1789222371505 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:42:51 | +1789222371622 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=113 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:42:51 | +1789222371630 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:42:51 | +1789222371630 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 19:42:52 | +1789222372035 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:42:52 | +1789222372388 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789222372288 · time_to_detect_ms=31 · strategy=re_locate · time_to_heal_ms=49 · verified=False |
| 19:42:52 | +1789222372388 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 19:42:52 | +1789222372410 | ✓ healed | ✓ HEALED in 49ms (verified=False) |
| 19:42:52 | +1789222372702 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:52 | +1789222372711 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:42:52 | +1789222372743 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · mode=cli |
| 19:42:52 | +1789222372965 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=219 · result=ok · candidate=Redmi Note 8GB |
| 19:42:52 | +1789222372990 | • step | ✓ step action: click:check |
| 19:42:52 | +1789222372990 | ⛓ hash | HASH seq=4 988a29cfa1ed... (click:check) |
| 19:42:56 | +1789222376046 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:42:56 | +1789222376066 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:42:56 | +1789222376231 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=165 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 19:42:56 | +1789222376239 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 19:42:56 | +1789222376247 | ⛓ hash | HASH seq=5 dfe15bbf3814... (goto:enquiry:Redmi Note 8GB) |
| 19:42:57 | +1789222377054 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:57 | +1789222377063 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 19:42:57 | +1789222377073 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Redmi%20Note%208GB · mode=cli |
| 19:42:57 | +1789222377192 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=108 · result=ok |
| 19:42:57 | +1789222377192 | • step | ✓ step action: click:enquiry:submit |
| 19:42:57 | +1789222377200 | ⛓ hash | HASH seq=6 dfe15bbf3814... (click:enquiry:submit) |
| 19:42:59 | +1789222379418 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 19:42:59 | +1789222379613 | 📊 metric | METRIC detect=44ms heal=293ms extra=2 status=pass |

**finished:** 2026-09-12 19:42:59 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 2 · recoveries 3

**finished:** 2026-09-12 19:42:59 — **end**
