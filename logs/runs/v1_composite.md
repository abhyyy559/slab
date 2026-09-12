# SENTRY run — v1/composite

- **started:** 2026-09-12 14:40:06
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days, then submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 14:40:06 | +1789204206446 | · PERTURB_INJECTED | target=composite · seq=0 |
| 14:40:07 | +1789204207302 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=69 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=composite |
| 14:40:07 | +1789204207310 | • step | ✓ step action: goto:search |
| 14:40:07 | +1789204207338 | ⛓ hash | HASH seq=1 92844c7cdd9d... (goto:search) |
| 14:40:08 | +1789204208416 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789204207670 · time_to_detect_ms=22 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=718 · verified=False |
| 14:40:08 | +1789204208438 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 14:40:08 | +1789204208443 | ✓ healed | ✓ HEALED in 718ms (verified=False) |
| 14:40:08 | +1789204208514 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 14:40:08 | +1789204208651 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789204208613 · time_to_detect_ms=33 · strategy=re_locate · time_to_heal_ms=4 · verified=False |
| 14:40:08 | +1789204208652 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 14:40:08 | +1789204208654 | ✓ healed | ✓ HEALED in 4ms (verified=False) |
| 14:40:08 | +1789204208678 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:40:08 | +1789204208746 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=51 · result=ok |
| 14:40:08 | +1789204208750 | • step | ✓ step action: click:filter |
| 14:40:08 | +1789204208751 | ⛓ hash | HASH seq=2 debe56ff275a... (click:filter) |
| 14:40:08 | +1789204208774 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:40:08 | +1789204208810 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=31 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:40:08 | +1789204208818 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:40:08 | +1789204208821 | ⛓ hash | HASH seq=3 2267c5022de7... (goto:delivery:Pixel Lite 8GB) |
| 14:40:09 | +1789204209200 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789204209170 · time_to_detect_ms=21 · strategy=re_locate · time_to_heal_ms=6 · verified=False |
| 14:40:09 | +1789204209201 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 14:40:09 | +1789204209203 | ✓ healed | ✓ HEALED in 6ms (verified=False) |
| 14:40:09 | +1789204209235 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:40:09 | +1789204209254 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:40:09 | +1789204209261 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Pixel%20Lite%208GB · mode=cli |
| 14:40:09 | +1789204209302 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=36 · result=ok · candidate=Pixel Lite 8GB |
| 14:40:09 | +1789204209308 | • step | ✓ step action: click:check |
| 14:40:09 | +1789204209311 | ⛓ hash | HASH seq=4 325dfbd74510... (click:check) |
| 14:40:12 | +1789204212348 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:40:12 | +1789204212409 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=49 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB |
| 14:40:12 | +1789204212413 | • step | ✓ step action: goto:enquiry:Pixel Lite 8GB |
| 14:40:12 | +1789204212415 | ⛓ hash | HASH seq=5 dfe15bbf3814... (goto:enquiry:Pixel Lite 8GB) |
| 14:40:12 | +1789204212776 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:40:12 | +1789204212794 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Pixel%20Lite%208GB · payload={'product': 'Pixel Lite 8GB', 'pin': '500001'} · mode=cli |
| 14:40:12 | +1789204212798 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Pixel%20Lite%208GB · mode=cli |
| 14:40:12 | +1789204212844 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=43 · result=ok |
| 14:40:12 | +1789204212850 | • step | ✓ step action: click:enquiry:submit |
| 14:40:12 | +1789204212852 | ⛓ hash | HASH seq=6 fe3c04c1f7f8... (click:enquiry:submit) |
| 14:40:14 | +1789204214874 | · enquiry_verdict | seq=6 · step=5 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 14:40:14 | +1789204214920 | 📊 metric | METRIC detect=25ms heal=242ms extra=2 status=pass |

**finished:** 2026-09-12 14:40:14 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Pixel Lite 8GB. Reference SS-734303. We will reply to agent+pin500001@example.com within 1 business · extra steps 2 · recoveries 3

**finished:** 2026-09-12 14:40:14 — **end**
