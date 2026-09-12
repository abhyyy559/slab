# SENTRY run — v4/attrs

- **started:** 2026-09-12 19:42:10
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 19:42:10 | +1789222330323 | · PERTURB_INJECTED | target=attrs · seq=0 |
| 19:42:11 | +1789222331695 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=261 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=attrs |
| 19:42:11 | +1789222331703 | • step | ✓ step action: goto:search |
| 19:42:11 | +1789222331711 | ⛓ hash | HASH seq=1 bf597a15bac7... (goto:search) |
| 19:42:12 | +1789222332267 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:42:12 | +1789222332342 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:42:12 | +1789222332387 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:42:12 | +1789222332575 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:12 | +1789222332691 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=107 · result=ok |
| 19:42:12 | +1789222332691 | • step | ✓ step action: click:filter |
| 19:42:12 | +1789222332700 | ⛓ hash | HASH seq=2 34dea5b73b9a... (click:filter) |
| 19:42:12 | +1789222332733 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:42:12 | +1789222332750 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:42:12 | +1789222332757 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:42:12 | +1789222332866 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=96 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:42:12 | +1789222332873 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:42:12 | +1789222332877 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:42:13 | +1789222333223 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:42:13 | +1789222333375 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:13 | +1789222333375 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:42:13 | +1789222333391 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Redmi%20Note%208GB · mode=cli |
| 19:42:13 | +1789222333519 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=128 · result=ok · candidate=Redmi Note 8GB |
| 19:42:13 | +1789222333519 | • step | ✓ step action: click:check |
| 19:42:13 | +1789222333528 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 19:42:16 | +1789222336583 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:42:16 | +1789222336611 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:42:16 | +1789222336766 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=147 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=attrs&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 19:42:16 | +1789222336769 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 19:42:16 | +1789222336775 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 19:42:17 | +1789222337551 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:17 | +1789222337557 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=attrs&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 19:42:17 | +1789222337557 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=attrs&product=Redmi%20Note%208GB · mode=cli |
| 19:42:17 | +1789222337690 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=116 · result=ok |
| 19:42:17 | +1789222337699 | • step | ✓ step action: click:enquiry:submit |
| 19:42:17 | +1789222337707 | ⛓ hash | HASH seq=6 39c33fda756c... (click:enquiry:submit) |
| 19:42:17 | +1789222337749 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 19:42:17 | +1789222337822 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:42:17 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:42:17 — **end**
