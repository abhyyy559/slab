# SENTRY run — v1/clean

- **started:** 2026-09-12 15:36:26
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 15:36:27 | +1789207587453 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=100 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 15:36:27 | +1789207587454 | • step | ✓ step action: goto:search |
| 15:36:27 | +1789207587459 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 15:36:27 | +1789207587810 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 15:36:27 | +1789207587952 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:36:28 | +1789207588023 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=56 · result=ok |
| 15:36:28 | +1789207588025 | • step | ✓ step action: click:filter |
| 15:36:28 | +1789207588027 | ⛓ hash | HASH seq=2 53f6bf1018b9... (click:filter) |
| 15:36:28 | +1789207588043 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:36:28 | +1789207588058 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:36:28 | +1789207588094 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=33 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:36:28 | +1789207588094 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:36:28 | +1789207588094 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 15:36:28 | +1789207588444 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:36:28 | +1789207588464 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 15:36:28 | +1789207588465 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 15:36:28 | +1789207588529 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=61 · result=ok · candidate=Redmi Note 8GB |
| 15:36:28 | +1789207588533 | • step | ✓ step action: click:check |
| 15:36:28 | +1789207588535 | ⛓ hash | HASH seq=4 d4be8bb4f6a2... (click:check) |
| 15:36:28 | +1789207588969 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:36:29 | +1789207589014 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 15:36:29 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 15:36:29 — **end**
