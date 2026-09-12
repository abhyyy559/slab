# SENTRY run — v4/strip

- **started:** 2026-09-12 19:41:52
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 19:41:52 | +1789222312961 | · PERTURB_INJECTED | target=strip · seq=0 |
| 19:41:54 | +1789222314478 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=303 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=strip |
| 19:41:54 | +1789222314486 | • step | ✓ step action: goto:search |
| 19:41:54 | +1789222314496 | ⛓ hash | HASH seq=1 35408ad28619... (goto:search) |
| 19:41:55 | +1789222315099 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 19:41:55 | +1789222315148 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:41:55 | +1789222315202 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:41:55 | +1789222315388 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.88 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:41:55 | +1789222315492 | · click | seq=2 · step=2 · target=filter_button · confidence=0.88 · signals=['role_name', 'text', 'visual'] · duration_ms=91 · result=ok |
| 19:41:55 | +1789222315501 | • step | ✓ step action: click:filter |
| 19:41:55 | +1789222315509 | ⛓ hash | HASH seq=2 bad85bf688ed... (click:filter) |
| 19:41:55 | +1789222315554 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:41:55 | +1789222315566 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:41:55 | +1789222315582 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:41:55 | +1789222315678 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=87 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:41:55 | +1789222315678 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:41:55 | +1789222315687 | ⛓ hash | HASH seq=3 a42c14bbab0e... (goto:delivery:Redmi Note 8GB) |
| 19:41:56 | +1789222316029 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:41:56 | +1789222316216 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:41:56 | +1789222316220 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:41:56 | +1789222316224 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Redmi%20Note%208GB · mode=cli |
| 19:41:56 | +1789222316293 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=63 · result=ok · candidate=Redmi Note 8GB |
| 19:41:56 | +1789222316297 | • step | ✓ step action: click:check |
| 19:41:56 | +1789222316303 | ⛓ hash | HASH seq=4 46b32eba74d5... (click:check) |
| 19:41:59 | +1789222319387 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:41:59 | +1789222319410 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:41:59 | +1789222319543 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=124 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=strip&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 19:41:59 | +1789222319552 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 19:41:59 | +1789222319556 | ⛓ hash | HASH seq=5 58a014d28576... (goto:enquiry:Redmi Note 8GB) |
| 19:42:00 | +1789222320337 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:00 | +1789222320343 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=strip&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 19:42:00 | +1789222320355 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=strip&product=Redmi%20Note%208GB · mode=cli |
| 19:42:00 | +1789222320477 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=120 · result=ok |
| 19:42:00 | +1789222320485 | • step | ✓ step action: click:enquiry:submit |
| 19:42:00 | +1789222320493 | ⛓ hash | HASH seq=6 7df479e03eda... (click:enquiry:submit) |
| 19:42:00 | +1789222320526 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 19:42:00 | +1789222320635 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:42:00 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:42:00 — **end**
