# SENTRY run — v4/move

- **started:** 2026-09-12 15:06:54
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 15:06:54 | +1789205814077 | · PERTURB_INJECTED | target=move · seq=0 |
| 15:06:55 | +1789205815245 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=137 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=move |
| 15:06:55 | +1789205815249 | • step | ✓ step action: goto:search |
| 15:06:55 | +1789205815251 | ⛓ hash | HASH seq=1 b0f62bd5ec8d... (goto:search) |
| 15:06:55 | +1789205815649 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789205815629 · time_to_detect_ms=7 · strategy=re_locate · time_to_heal_ms=8 · verified=False |
| 15:06:55 | +1789205815651 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 15:06:55 | +1789205815655 | ✓ healed | ✓ HEALED in 8ms (verified=False) |
| 15:06:55 | +1789205815760 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:06:55 | +1789205815884 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789205815870 · time_to_detect_ms=4 · strategy=re_locate · time_to_heal_ms=8 · verified=False |
| 15:06:55 | +1789205815885 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 15:06:55 | +1789205815885 | ✓ healed | ✓ HEALED in 8ms (verified=False) |
| 15:06:55 | +1789205815948 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:06:56 | +1789205816028 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=77 · result=ok |
| 15:06:56 | +1789205816034 | • step | ✓ step action: click:filter |
| 15:06:56 | +1789205816037 | ⛓ hash | HASH seq=2 598c25f75653... (click:filter) |
| 15:06:56 | +1789205816061 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:06:56 | +1789205816073 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:06:56 | +1789205816139 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=61 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:06:56 | +1789205816147 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:06:56 | +1789205816151 | ⛓ hash | HASH seq=3 246060fc45d4... (goto:delivery:Redmi Note 8GB) |
| 15:06:56 | +1789205816539 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789205816528 · time_to_detect_ms=2 · strategy=re_locate · time_to_heal_ms=9 · verified=False |
| 15:06:56 | +1789205816539 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 15:06:56 | +1789205816539 | ✓ healed | ✓ HEALED in 9ms (verified=False) |
| 15:06:56 | +1789205816580 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:06:56 | +1789205816590 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:06:56 | +1789205816594 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · mode=cli |
| 15:06:56 | +1789205816646 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=49 · result=ok · candidate=Redmi Note 8GB |
| 15:06:56 | +1789205816652 | • step | ✓ step action: click:check |
| 15:06:56 | +1789205816654 | ⛓ hash | HASH seq=4 2f8e6266ceb0... (click:check) |
| 15:06:59 | +1789205819679 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:06:59 | +1789205819737 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=49 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=move&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 15:06:59 | +1789205819740 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 15:06:59 | +1789205819743 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 15:07:00 | +1789205820161 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:00 | +1789205820164 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=move&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 15:07:00 | +1789205820166 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=move&product=Redmi%20Note%208GB · mode=cli |
| 15:07:00 | +1789205820214 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=41 · result=ok |
| 15:07:00 | +1789205820221 | • step | ✓ step action: click:enquiry:submit |
| 15:07:00 | +1789205820223 | ⛓ hash | HASH seq=6 39c33fda756c... (click:enquiry:submit) |
| 15:07:00 | +1789205820242 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 15:07:00 | +1789205820268 | 📊 metric | METRIC detect=4ms heal=8ms extra=0 status=pass |

**finished:** 2026-09-12 15:07:00 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 3

**finished:** 2026-09-12 15:07:00 — **end**
