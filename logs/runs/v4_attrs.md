# SENTRY run — v4/attrs

- **started:** 2026-09-12 15:07:00
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 15:07:00 | +1789205820499 | · PERTURB_INJECTED | target=attrs · seq=0 |
| 15:07:01 | +1789205821627 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=138 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=attrs |
| 15:07:01 | +1789205821633 | • step | ✓ step action: goto:search |
| 15:07:01 | +1789205821636 | ⛓ hash | HASH seq=1 bf597a15bac7... (goto:search) |
| 15:07:02 | +1789205822083 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:07:02 | +1789205822219 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:02 | +1789205822296 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=70 · result=ok |
| 15:07:02 | +1789205822302 | • step | ✓ step action: click:filter |
| 15:07:02 | +1789205822304 | ⛓ hash | HASH seq=2 34dea5b73b9a... (click:filter) |
| 15:07:02 | +1789205822322 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:07:02 | +1789205822338 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:07:02 | +1789205822406 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=58 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:07:02 | +1789205822412 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:07:02 | +1789205822415 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:07:02 | +1789205822824 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:02 | +1789205822832 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:07:02 | +1789205822842 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Redmi%20Note%208GB · mode=cli |
| 15:07:02 | +1789205822905 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=57 · result=ok · candidate=Redmi Note 8GB |
| 15:07:02 | +1789205822913 | • step | ✓ step action: click:check |
| 15:07:02 | +1789205822916 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 15:07:05 | +1789205825946 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:07:06 | +1789205826035 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=77 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=attrs&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 15:07:06 | +1789205826043 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 15:07:06 | +1789205826046 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 15:07:06 | +1789205826437 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:07:06 | +1789205826442 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=attrs&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 15:07:06 | +1789205826446 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=attrs&product=Redmi%20Note%208GB · mode=cli |
| 15:07:06 | +1789205826507 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=56 · result=ok |
| 15:07:06 | +1789205826512 | • step | ✓ step action: click:enquiry:submit |
| 15:07:06 | +1789205826514 | ⛓ hash | HASH seq=6 39c33fda756c... (click:enquiry:submit) |
| 15:07:06 | +1789205826530 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 15:07:06 | +1789205826555 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 15:07:06 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 0

**finished:** 2026-09-12 15:07:06 — **end**
