# SENTRY run — v4/rename_strip

- **started:** 2026-09-12 15:05:03
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 15:05:03 | +1789205703825 | · PERTURB_INJECTED | target=rename_strip · seq=0 |
| 15:05:04 | +1789205704867 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=105 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename_strip |
| 15:05:04 | +1789205704872 | • step | ✓ step action: goto:search |
| 15:05:04 | +1789205704874 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 15:05:05 | +1789205705263 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:05:05 | +1789205705403 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:05 | +1789205705465 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=56 · result=ok |
| 15:05:05 | +1789205705472 | • step | ✓ step action: click:filter |
| 15:05:05 | +1789205705475 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 15:05:05 | +1789205705501 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:05:05 | +1789205705517 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:05:05 | +1789205705575 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=55 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:05:05 | +1789205705581 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:05:05 | +1789205705582 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:05:05 | +1789205705967 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:05 | +1789205705971 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:05:05 | +1789205705976 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Redmi%20Note%208GB · mode=cli |
| 15:05:06 | +1789205706015 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=37 · result=ok · candidate=Redmi Note 8GB |
| 15:05:06 | +1789205706021 | • step | ✓ step action: click:check |
| 15:05:06 | +1789205706023 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 15:05:09 | +1789205709045 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:05:09 | +1789205709074 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 15:05:09 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 15:05:09 — **end**
