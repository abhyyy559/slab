# SENTRY run — v4/modal

- **started:** 2026-09-12 15:07:06
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 15:07:06 | +1789205826754 | · PERTURB_INJECTED | target=modal · seq=0 |
| 15:07:07 | +1789205827812 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=108 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=modal |
| 15:07:07 | +1789205827815 | • step | ✓ step action: goto:search |
| 15:07:07 | +1789205827817 | ⛓ hash | HASH seq=1 a723c4ad2b51... (goto:search) |
| 15:07:08 | +1789205828580 | · RECOVERY · event | trigger=modal · expected=clean_page · observed=chaos-modal visible · detected_at_ms=1789205828183 · time_to_detect_ms=12 · strategy=re_plan · steps=['dismissed:#chaos-modal'] · time_to_heal_ms=380 · verified=False |
| 15:07:08 | +1789205828584 | ⚠ recovery | ⚠ RECOVERY: modal -> re_plan |
| 15:07:08 | +1789205828587 | ✓ healed | ✓ HEALED in 380ms (verified=False) |
| 15:07:08 | +1789205828659 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:07:08 | +1789205828783 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:08 | +1789205828884 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=90 · result=ok |
| 15:07:08 | +1789205828891 | • step | ✓ step action: click:filter |
| 15:07:08 | +1789205828894 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 15:07:08 | +1789205828920 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:07:08 | +1789205828933 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:07:08 | +1789205828975 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=36 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:07:08 | +1789205828980 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:07:08 | +1789205828982 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:07:09 | +1789205829389 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:09 | +1789205829392 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:07:09 | +1789205829397 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Redmi%20Note%208GB · mode=cli |
| 15:07:09 | +1789205829452 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=52 · result=ok · candidate=Redmi Note 8GB |
| 15:07:09 | +1789205829458 | • step | ✓ step action: click:check |
| 15:07:09 | +1789205829463 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 15:07:12 | +1789205832480 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:07:12 | +1789205832534 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=44 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=modal&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 15:07:12 | +1789205832539 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 15:07:12 | +1789205832540 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 15:07:12 | +1789205832911 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:12 | +1789205832917 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=modal&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 15:07:12 | +1789205832921 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=modal&product=Redmi%20Note%208GB · mode=cli |
| 15:07:12 | +1789205832964 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=38 · result=ok |
| 15:07:12 | +1789205832970 | • step | ✓ step action: click:enquiry:submit |
| 15:07:12 | +1789205832972 | ⛓ hash | HASH seq=6 39c33fda756c... (click:enquiry:submit) |
| 15:07:12 | +1789205832992 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 15:07:13 | +1789205833016 | 📊 metric | METRIC detect=12ms heal=380ms extra=1 status=pass |

**finished:** 2026-09-12 15:07:13 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 1 · recoveries 1

**finished:** 2026-09-12 15:07:13 — **end**
