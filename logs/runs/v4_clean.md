# SENTRY run — v4/clean

- **started:** 2026-09-12 16:01:29
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:30 | +1789209090483 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=95 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 16:01:30 | +1789209090483 | • step | ✓ step action: goto:search |
| 16:01:30 | +1789209090488 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 16:01:30 | +1789209090818 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:01:30 | +1789209090886 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:30 | +1789209090943 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=56 · result=ok |
| 16:01:30 | +1789209090946 | • step | ✓ step action: click:filter |
| 16:01:30 | +1789209090948 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 16:01:30 | +1789209090967 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:30 | +1789209090978 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:31 | +1789209091040 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=60 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:31 | +1789209091042 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:31 | +1789209091043 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 16:01:31 | +1789209091383 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:31 | +1789209091383 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 16:01:31 | +1789209091384 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 16:01:31 | +1789209091431 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=45 · result=ok · candidate=Redmi Note 8GB |
| 16:01:31 | +1789209091434 | • step | ✓ step action: click:check |
| 16:01:31 | +1789209091436 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 16:01:31 | +1789209091847 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:01:31 | +1789209091858 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 16:01:31 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 16:01:31 — **end**
