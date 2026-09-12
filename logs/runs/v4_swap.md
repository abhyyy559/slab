# SENTRY run — v4/swap

- **started:** 2026-09-12 15:05:36
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 15:05:36 | +1789205736771 | · PERTURB_INJECTED | target=swap · seq=0 |
| 15:05:37 | +1789205737846 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=96 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=swap |
| 15:05:37 | +1789205737852 | • step | ✓ step action: goto:search |
| 15:05:37 | +1789205737852 | ⛓ hash | HASH seq=1 a59cbaafd60f... (goto:search) |
| 15:05:38 | +1789205738244 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:05:38 | +1789205738366 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:38 | +1789205738429 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=55 · result=ok |
| 15:05:38 | +1789205738435 | • step | ✓ step action: click:filter |
| 15:05:38 | +1789205738437 | ⛓ hash | HASH seq=2 c56a2318d73b... (click:filter) |
| 15:05:38 | +1789205738448 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:05:38 | +1789205738461 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:05:38 | +1789205738519 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=53 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:05:38 | +1789205738524 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:05:38 | +1789205738526 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:05:38 | +1789205738878 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:38 | +1789205738881 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:05:38 | +1789205738882 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Redmi%20Note%208GB · mode=cli |
| 15:05:38 | +1789205738928 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=43 · result=ok · candidate=Redmi Note 8GB |
| 15:05:38 | +1789205738932 | • step | ✓ step action: click:check |
| 15:05:38 | +1789205738935 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 15:05:41 | +1789205741974 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:05:42 | +1789205742017 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 15:05:42 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 15:05:42 — **end**
