# SENTRY run — v4/extra_step

- **started:** 2026-09-12 19:42:27
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 19:42:27 | +1789222347765 | · PERTURB_INJECTED | target=extra_step · seq=0 |
| 19:42:29 | +1789222349428 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=280 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=extra_step |
| 19:42:29 | +1789222349431 | • step | ✓ step action: goto:search |
| 19:42:29 | +1789222349435 | ⛓ hash | HASH seq=1 695f69c6cb1a... (goto:search) |
| 19:42:30 | +1789222350590 | · RECOVERY · event | trigger=extra_step · expected=clean_page · observed=chaos-confirm visible · detected_at_ms=1789222350055 · time_to_detect_ms=51 · strategy=re_plan · steps=['dismissed:#chaos-confirm'] · time_to_heal_ms=484 · verified=False |
| 19:42:30 | +1789222350598 | ⚠ recovery | ⚠ RECOVERY: extra_step -> re_plan |
| 19:42:30 | +1789222350598 | ✓ healed | ✓ HEALED in 484ms (verified=False) |
| 19:42:30 | +1789222350706 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:42:30 | +1789222350756 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:42:30 | +1789222350798 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:42:30 | +1789222350985 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:31 | +1789222351137 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=147 · result=ok |
| 19:42:31 | +1789222351145 | • step | ✓ step action: click:filter |
| 19:42:31 | +1789222351154 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 19:42:31 | +1789222351214 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:42:31 | +1789222351241 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:42:31 | +1789222351248 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:42:31 | +1789222351389 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=135 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:42:31 | +1789222351406 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:42:31 | +1789222351414 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:42:31 | +1789222351789 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:42:32 | +1789222352034 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:32 | +1789222352038 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:42:32 | +1789222352049 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · mode=cli |
| 19:42:32 | +1789222352188 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=128 · result=ok · candidate=Redmi Note 8GB |
| 19:42:32 | +1789222352199 | • step | ✓ step action: click:check |
| 19:42:32 | +1789222352199 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 19:42:35 | +1789222355262 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:42:35 | +1789222355287 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:42:35 | +1789222355430 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=139 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=extra_step&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 19:42:35 | +1789222355430 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 19:42:35 | +1789222355438 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 19:42:36 | +1789222356140 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:36 | +1789222356152 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=extra_step&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 19:42:36 | +1789222356152 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=extra_step&product=Redmi%20Note%208GB · mode=cli |
| 19:42:36 | +1789222356265 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=107 · result=ok |
| 19:42:36 | +1789222356273 | • step | ✓ step action: click:enquiry:submit |
| 19:42:36 | +1789222356282 | ⛓ hash | HASH seq=6 39c33fda756c... (click:enquiry:submit) |
| 19:42:36 | +1789222356347 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 19:42:36 | +1789222356431 | 📊 metric | METRIC detect=51ms heal=484ms extra=1 status=pass |

**finished:** 2026-09-12 19:42:36 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 1 · recoveries 1

**finished:** 2026-09-12 19:42:36 — **end**
