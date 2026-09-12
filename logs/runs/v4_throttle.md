# SENTRY run — v4/throttle

- **started:** 2026-09-12 19:42:36
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 19:42:36 | +1789222356838 | · PERTURB_INJECTED | target=throttle · seq=0 |
| 19:42:38 | +1789222358433 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=323 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=throttle |
| 19:42:38 | +1789222358449 | • step | ✓ step action: goto:search |
| 19:42:38 | +1789222358466 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 19:42:39 | +1789222359037 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:42:39 | +1789222359078 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:42:39 | +1789222359112 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:42:39 | +1789222359263 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:39 | +1789222359379 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=115 · result=ok |
| 19:42:39 | +1789222359387 | • step | ✓ step action: click:filter |
| 19:42:39 | +1789222359387 | ⛓ hash | HASH seq=2 7d2e46e86368... (click:filter) |
| 19:42:39 | +1789222359414 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:42:39 | +1789222359434 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:42:39 | +1789222359434 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:42:39 | +1789222359606 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=143 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:42:39 | +1789222359626 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:42:39 | +1789222359626 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:42:39 | +1789222359982 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:42:40 | +1789222360156 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:40 | +1789222360168 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:42:40 | +1789222360168 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · mode=cli |
| 19:42:40 | +1789222360311 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=126 · result=ok · candidate=Redmi Note 8GB |
| 19:42:40 | +1789222360330 | • step | ✓ step action: click:check |
| 19:42:40 | +1789222360343 | ⛓ hash | HASH seq=4 217cda3bde74... (click:check) |
| 19:42:43 | +1789222363400 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:42:43 | +1789222363412 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:42:43 | +1789222363581 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=161 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=throttle&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 19:42:43 | +1789222363581 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 19:42:43 | +1789222363593 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 19:42:44 | +1789222364381 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:44 | +1789222364391 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=throttle&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 19:42:44 | +1789222364407 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=throttle&product=Redmi%20Note%208GB · mode=cli |
| 19:42:44 | +1789222364566 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=143 · result=ok |
| 19:42:44 | +1789222364574 | • step | ✓ step action: click:enquiry:submit |
| 19:42:44 | +1789222364582 | ⛓ hash | HASH seq=6 dccfb6e26d60... (click:enquiry:submit) |
| 19:42:47 | +1789222367126 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 19:42:47 | +1789222367210 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:42:47 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:42:47 — **end**
