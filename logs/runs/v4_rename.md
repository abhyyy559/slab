# SENTRY run — v4/rename

- **started:** 2026-09-12 15:07:37
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 15:07:37 | +1789205857220 | · PERTURB_INJECTED | target=rename · seq=0 |
| 15:07:38 | +1789205858435 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=127 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename |
| 15:07:38 | +1789205858440 | • step | ✓ step action: goto:search |
| 15:07:38 | +1789205858443 | ⛓ hash | HASH seq=1 e3d8d082eea9... (goto:search) |
| 15:07:38 | +1789205858877 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789205858840 · time_to_detect_ms=14 · strategy=re_locate · time_to_heal_ms=20 · verified=False |
| 15:07:38 | +1789205858881 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 15:07:38 | +1789205858884 | ✓ healed | ✓ HEALED in 20ms (verified=False) |
| 15:07:38 | +1789205858976 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:07:39 | +1789205859111 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789205859089 · time_to_detect_ms=8 · strategy=re_locate · time_to_heal_ms=11 · verified=False |
| 15:07:39 | +1789205859113 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 15:07:39 | +1789205859116 | ✓ healed | ✓ HEALED in 11ms (verified=False) |
| 15:07:39 | +1789205859178 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:39 | +1789205859243 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=61 · result=ok |
| 15:07:39 | +1789205859249 | • step | ✓ step action: click:filter |
| 15:07:39 | +1789205859252 | ⛓ hash | HASH seq=2 8abc8136a040... (click:filter) |
| 15:07:39 | +1789205859282 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:07:39 | +1789205859302 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:07:39 | +1789205859375 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=66 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:07:39 | +1789205859382 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:07:39 | +1789205859385 | ⛓ hash | HASH seq=3 8693c8664bfa... (goto:delivery:Redmi Note 8GB) |
| 15:07:39 | +1789205859747 | · RECOVERY · event | trigger=label_renamed · expected=clean_page · observed=Verify Shipment · detected_at_ms=1789205859733 · time_to_detect_ms=4 · strategy=re_locate · time_to_heal_ms=7 · verified=False |
| 15:07:39 | +1789205859748 | ⚠ recovery | ⚠ RECOVERY: label_renamed -> re_locate |
| 15:07:39 | +1789205859751 | ✓ healed | ✓ HEALED in 7ms (verified=False) |
| 15:07:39 | +1789205859788 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:39 | +1789205859816 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:07:39 | +1789205859825 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · mode=cli |
| 15:07:39 | +1789205859891 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=59 · result=ok · candidate=Redmi Note 8GB |
| 15:07:39 | +1789205859897 | • step | ✓ step action: click:check |
| 15:07:39 | +1789205859899 | ⛓ hash | HASH seq=4 5b840b9e89d4... (click:check) |
| 15:07:42 | +1789205862922 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:07:42 | +1789205862976 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=42 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=rename&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 15:07:42 | +1789205862981 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 15:07:42 | +1789205862983 | ⛓ hash | HASH seq=5 9bad21c4079e... (goto:enquiry:Redmi Note 8GB) |
| 15:07:43 | +1789205863373 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:43 | +1789205863373 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=rename&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 15:07:43 | +1789205863380 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=rename&product=Redmi%20Note%208GB · mode=cli |
| 15:07:43 | +1789205863433 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=50 · result=ok |
| 15:07:43 | +1789205863436 | • step | ✓ step action: click:enquiry:submit |
| 15:07:43 | +1789205863439 | ⛓ hash | HASH seq=6 c1777af67038... (click:enquiry:submit) |
| 15:07:43 | +1789205863460 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 15:07:43 | +1789205863486 | 📊 metric | METRIC detect=8ms heal=12ms extra=0 status=pass |

**finished:** 2026-09-12 15:07:43 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 3

**finished:** 2026-09-12 15:07:43 — **end**
