# SENTRY run — v4/throttle

- **started:** 2026-09-12 16:01:51
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:51 | +1789209111150 | · PERTURB_INJECTED | target=throttle · seq=0 |
| 16:01:51 | +1789209111684 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=86 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=throttle |
| 16:01:51 | +1789209111684 | • step | ✓ step action: goto:search |
| 16:01:51 | +1789209111686 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 16:01:52 | +1789209112018 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:01:52 | +1789209112102 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:52 | +1789209112147 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=45 · result=ok |
| 16:01:52 | +1789209112148 | • step | ✓ step action: click:filter |
| 16:01:52 | +1789209112149 | ⛓ hash | HASH seq=2 7d2e46e86368... (click:filter) |
| 16:01:52 | +1789209112161 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:52 | +1789209112170 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:52 | +1789209112202 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=30 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:52 | +1789209112204 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:52 | +1789209112205 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 16:01:52 | +1789209112532 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:52 | +1789209112533 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 16:01:52 | +1789209112534 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Redmi%20Note%208GB · mode=cli |
| 16:01:52 | +1789209112581 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=45 · result=ok · candidate=Redmi Note 8GB |
| 16:01:52 | +1789209112582 | • step | ✓ step action: click:check |
| 16:01:52 | +1789209112583 | ⛓ hash | HASH seq=4 217cda3bde74... (click:check) |
| 16:01:55 | +1789209115601 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:01:55 | +1789209115627 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 16:01:55 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 16:01:55 — **end**
