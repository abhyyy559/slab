# SENTRY run — v4/extra_step

- **started:** 2026-09-12 15:07:13
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 15:07:13 | +1789205833202 | · PERTURB_INJECTED | target=extra_step · seq=0 |
| 15:07:14 | +1789205834270 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=107 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=extra_step |
| 15:07:14 | +1789205834274 | • step | ✓ step action: goto:search |
| 15:07:14 | +1789205834275 | ⛓ hash | HASH seq=1 695f69c6cb1a... (goto:search) |
| 15:07:15 | +1789205835014 | · RECOVERY · event | trigger=extra_step · expected=clean_page · observed=chaos-confirm visible · detected_at_ms=1789205834641 · time_to_detect_ms=12 · strategy=re_plan · steps=['dismissed:#chaos-confirm'] · time_to_heal_ms=357 · verified=False |
| 15:07:15 | +1789205835015 | ⚠ recovery | ⚠ RECOVERY: extra_step -> re_plan |
| 15:07:15 | +1789205835019 | ✓ healed | ✓ HEALED in 357ms (verified=False) |
| 15:07:15 | +1789205835070 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:07:15 | +1789205835167 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:15 | +1789205835213 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=39 · result=ok |
| 15:07:15 | +1789205835220 | • step | ✓ step action: click:filter |
| 15:07:15 | +1789205835223 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 15:07:15 | +1789205835239 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:07:15 | +1789205835251 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:07:15 | +1789205835313 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=56 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:07:15 | +1789205835316 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:07:15 | +1789205835318 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:07:15 | +1789205835674 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:15 | +1789205835677 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:07:15 | +1789205835681 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · mode=cli |
| 15:07:15 | +1789205835709 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=24 · result=ok · candidate=Redmi Note 8GB |
| 15:07:15 | +1789205835714 | • step | ✓ step action: click:check |
| 15:07:15 | +1789205835717 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 15:07:18 | +1789205838746 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:07:18 | +1789205838809 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=50 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=extra_step&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 15:07:18 | +1789205838814 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 15:07:18 | +1789205838817 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 15:07:19 | +1789205839229 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:19 | +1789205839236 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=extra_step&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 15:07:19 | +1789205839246 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=extra_step&product=Redmi%20Note%208GB · mode=cli |
| 15:07:19 | +1789205839306 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=54 · result=ok |
| 15:07:19 | +1789205839310 | • step | ✓ step action: click:enquiry:submit |
| 15:07:19 | +1789205839312 | ⛓ hash | HASH seq=6 39c33fda756c... (click:enquiry:submit) |
| 15:07:19 | +1789205839333 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 15:07:19 | +1789205839360 | 📊 metric | METRIC detect=12ms heal=357ms extra=1 status=pass |

**finished:** 2026-09-12 15:07:19 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 1 · recoveries 1

**finished:** 2026-09-12 15:07:19 — **end**
