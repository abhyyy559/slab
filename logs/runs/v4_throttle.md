# SENTRY run — v4/throttle

- **started:** 2026-09-12 15:07:19
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 15:07:19 | +1789205839549 | · PERTURB_INJECTED | target=throttle · seq=0 |
| 15:07:20 | +1789205840683 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=141 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=throttle |
| 15:07:20 | +1789205840689 | • step | ✓ step action: goto:search |
| 15:07:20 | +1789205840691 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 15:07:21 | +1789205841076 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:07:21 | +1789205841180 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:21 | +1789205841254 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=70 · result=ok |
| 15:07:21 | +1789205841259 | • step | ✓ step action: click:filter |
| 15:07:21 | +1789205841261 | ⛓ hash | HASH seq=2 7d2e46e86368... (click:filter) |
| 15:07:21 | +1789205841287 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:07:21 | +1789205841300 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:07:21 | +1789205841361 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=56 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:07:21 | +1789205841364 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:07:21 | +1789205841367 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:07:21 | +1789205841709 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:21 | +1789205841711 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:07:21 | +1789205841716 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · mode=cli |
| 15:07:21 | +1789205841758 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=38 · result=ok · candidate=Redmi Note 8GB |
| 15:07:21 | +1789205841760 | • step | ✓ step action: click:check |
| 15:07:21 | +1789205841763 | ⛓ hash | HASH seq=4 217cda3bde74... (click:check) |
| 15:07:24 | +1789205844784 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:07:24 | +1789205844839 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=44 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=throttle&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 15:07:24 | +1789205844844 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 15:07:24 | +1789205844846 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 15:07:25 | +1789205845257 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:25 | +1789205845261 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=throttle&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 15:07:25 | +1789205845265 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=throttle&product=Redmi%20Note%208GB · mode=cli |
| 15:07:25 | +1789205845310 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=38 · result=ok |
| 15:07:25 | +1789205845318 | • step | ✓ step action: click:enquiry:submit |
| 15:07:25 | +1789205845321 | ⛓ hash | HASH seq=6 dccfb6e26d60... (click:enquiry:submit) |
| 15:07:27 | +1789205847935 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 15:07:27 | +1789205847972 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 15:07:27 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 0

**finished:** 2026-09-12 15:07:27 — **end**
