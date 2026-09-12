# SENTRY run — v4/rename

- **started:** 2026-09-12 19:42:59
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 19:42:59 | +1789222379977 | · PERTURB_INJECTED | target=rename · seq=0 |
| 19:43:01 | +1789222381723 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=400 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename |
| 19:43:01 | +1789222381732 | • step | ✓ step action: goto:search |
| 19:43:01 | +1789222381740 | ⛓ hash | HASH seq=1 e3d8d082eea9... (goto:search) |
| 19:43:02 | +1789222382467 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789222382361 · time_to_detect_ms=35 · strategy=re_locate · time_to_heal_ms=65 · verified=False |
| 19:43:02 | +1789222382471 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 19:43:02 | +1789222382486 | ✓ healed | ✓ HEALED in 65ms (verified=False) |
| 19:43:02 | +1789222382641 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:43:02 | +1789222382684 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:43:02 | +1789222382740 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:43:02 | +1789222382984 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789222382926 · time_to_detect_ms=17 · strategy=re_locate · time_to_heal_ms=34 · verified=False |
| 19:43:02 | +1789222382984 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 19:43:02 | +1789222382984 | ✓ healed | ✓ HEALED in 34ms (verified=False) |
| 19:43:03 | +1789222383164 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:43:03 | +1789222383303 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=131 · result=ok |
| 19:43:03 | +1789222383309 | • step | ✓ step action: click:filter |
| 19:43:03 | +1789222383314 | ⛓ hash | HASH seq=2 8abc8136a040... (click:filter) |
| 19:43:03 | +1789222383353 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:43:03 | +1789222383374 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:43:03 | +1789222383379 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:43:03 | +1789222383490 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=107 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:43:03 | +1789222383499 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:43:03 | +1789222383499 | ⛓ hash | HASH seq=3 8693c8664bfa... (goto:delivery:Redmi Note 8GB) |
| 19:43:03 | +1789222383850 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:43:04 | +1789222384076 | · RECOVERY · event | trigger=label_renamed · expected=clean_page · observed=Verify Shipment · detected_at_ms=1789222384035 · time_to_detect_ms=16 · strategy=re_locate · time_to_heal_ms=9 · verified=False |
| 19:43:04 | +1789222384076 | ⚠ recovery | ⚠ RECOVERY: label_renamed -> re_locate |
| 19:43:04 | +1789222384076 | ✓ healed | ✓ HEALED in 9ms (verified=False) |
| 19:43:04 | +1789222384189 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:43:04 | +1789222384194 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:43:04 | +1789222384198 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · mode=cli |
| 19:43:04 | +1789222384293 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=94 · result=ok · candidate=Redmi Note 8GB |
| 19:43:04 | +1789222384309 | • step | ✓ step action: click:check |
| 19:43:04 | +1789222384309 | ⛓ hash | HASH seq=4 5b840b9e89d4... (click:check) |
| 19:43:07 | +1789222387345 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:43:07 | +1789222387354 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:43:07 | +1789222387408 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=51 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=rename&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 19:43:07 | +1789222387410 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 19:43:07 | +1789222387410 | ⛓ hash | HASH seq=5 9bad21c4079e... (goto:enquiry:Redmi Note 8GB) |
| 19:43:07 | +1789222387938 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:43:07 | +1789222387941 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=rename&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 19:43:07 | +1789222387943 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=rename&product=Redmi%20Note%208GB · mode=cli |
| 19:43:08 | +1789222388010 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=63 · result=ok |
| 19:43:08 | +1789222388012 | • step | ✓ step action: click:enquiry:submit |
| 19:43:08 | +1789222388014 | ⛓ hash | HASH seq=6 c1777af67038... (click:enquiry:submit) |
| 19:43:08 | +1789222388028 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 19:43:08 | +1789222388070 | 📊 metric | METRIC detect=22ms heal=36ms extra=0 status=pass |

**finished:** 2026-09-12 19:43:08 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 3

**finished:** 2026-09-12 19:43:08 — **end**
