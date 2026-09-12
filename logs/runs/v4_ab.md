# SENTRY run — v4/ab

- **started:** 2026-09-12 15:05:47
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 15:05:47 | +1789205747827 | · PERTURB_INJECTED | target=ab · seq=0 |
| 15:05:48 | +1789205748940 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=113 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=ab |
| 15:05:48 | +1789205748943 | • step | ✓ step action: goto:search |
| 15:05:48 | +1789205748945 | ⛓ hash | HASH seq=1 0be231dd0986... (goto:search) |
| 15:05:49 | +1789205749314 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:05:49 | +1789205749433 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:49 | +1789205749489 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=49 · result=ok |
| 15:05:49 | +1789205749497 | • step | ✓ step action: click:filter |
| 15:05:49 | +1789205749500 | ⛓ hash | HASH seq=2 5b834e3418d4... (click:filter) |
| 15:05:49 | +1789205749519 | · STOCK_FILTER | excluded=1 · detail=out of stock, not eligible: ['Lava Blaze 8GB'] |
| 15:05:49 | +1789205749533 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:05:49 | +1789205749612 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=73 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=ab&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:05:49 | +1789205749620 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:05:49 | +1789205749622 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:05:49 | +1789205749998 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:05:50 | +1789205750008 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=ab&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:05:50 | +1789205750018 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=ab&product=Redmi%20Note%208GB · mode=cli |
| 15:05:50 | +1789205750101 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=74 · result=ok · candidate=Redmi Note 8GB |
| 15:05:50 | +1789205750113 | • step | ✓ step action: click:check |
| 15:05:50 | +1789205750116 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 15:05:53 | +1789205753143 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:05:53 | +1789205753169 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 15:05:53 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 15:05:53 — **end**
