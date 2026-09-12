# SENTRY run — v4/composite

- **started:** 2026-09-12 15:07:28
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 15:07:28 | +1789205848191 | · PERTURB_INJECTED | target=composite · seq=0 |
| 15:07:29 | +1789205849198 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=113 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=composite |
| 15:07:29 | +1789205849205 | • step | ✓ step action: goto:search |
| 15:07:29 | +1789205849207 | ⛓ hash | HASH seq=1 6f565c69f0c3... (goto:search) |
| 15:07:30 | +1789205850371 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789205849588 · time_to_detect_ms=17 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=763 · verified=False |
| 15:07:30 | +1789205850373 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 15:07:30 | +1789205850377 | ✓ healed | ✓ HEALED in 763ms (verified=False) |
| 15:07:30 | +1789205850448 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 15:07:30 | +1789205850613 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789205850586 · time_to_detect_ms=16 · strategy=re_locate · time_to_heal_ms=11 · verified=False |
| 15:07:30 | +1789205850616 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 15:07:30 | +1789205850618 | ✓ healed | ✓ HEALED in 11ms (verified=False) |
| 15:07:30 | +1789205850671 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:30 | +1789205850732 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=55 · result=ok |
| 15:07:30 | +1789205850737 | • step | ✓ step action: click:filter |
| 15:07:30 | +1789205850738 | ⛓ hash | HASH seq=2 39b4e5c1e7f7... (click:filter) |
| 15:07:30 | +1789205850756 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:07:30 | +1789205850767 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:07:30 | +1789205850814 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=44 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:07:30 | +1789205850820 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:07:30 | +1789205850821 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 15:07:31 | +1789205851212 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789205851186 · time_to_detect_ms=12 · strategy=re_locate · time_to_heal_ms=12 · verified=False |
| 15:07:31 | +1789205851213 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 15:07:31 | +1789205851215 | ✓ healed | ✓ HEALED in 12ms (verified=False) |
| 15:07:31 | +1789205851257 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:31 | +1789205851261 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:07:31 | +1789205851264 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · mode=cli |
| 15:07:31 | +1789205851309 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=39 · result=ok · candidate=Redmi Note 8GB |
| 15:07:31 | +1789205851314 | • step | ✓ step action: click:check |
| 15:07:31 | +1789205851316 | ⛓ hash | HASH seq=4 988a29cfa1ed... (click:check) |
| 15:07:34 | +1789205854333 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:07:34 | +1789205854395 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=52 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 15:07:34 | +1789205854400 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 15:07:34 | +1789205854402 | ⛓ hash | HASH seq=5 dfe15bbf3814... (goto:enquiry:Redmi Note 8GB) |
| 15:07:34 | +1789205854837 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:34 | +1789205854842 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 15:07:34 | +1789205854847 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=composite&product=Redmi%20Note%208GB · mode=cli |
| 15:07:34 | +1789205854891 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=40 · result=ok |
| 15:07:34 | +1789205854898 | • step | ✓ step action: click:enquiry:submit |
| 15:07:34 | +1789205854900 | ⛓ hash | HASH seq=6 dfe15bbf3814... (click:enquiry:submit) |
| 15:07:36 | +1789205856903 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 15:07:36 | +1789205856962 | 📊 metric | METRIC detect=15ms heal=262ms extra=2 status=pass |

**finished:** 2026-09-12 15:07:36 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 2 · recoveries 3

**finished:** 2026-09-12 15:07:36 — **end**
