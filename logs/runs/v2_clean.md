# SENTRY run — v2/clean

- **started:** 2026-09-12 19:23:24
- **goal:** (none)

| t | ts | event | detail |
|---|---|---|---|
| 19:23:25 | +1789221205496 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=151 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 19:23:25 | +1789221205496 | • step | ✓ step action: goto:search |
| 19:23:25 | +1789221205496 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 19:23:25 | +1789221205963 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:23:26 | +1789221206140 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:23:26 | +1789221206219 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=79 · result=ok |
| 19:23:26 | +1789221206228 | • step | ✓ step action: click:filter |
| 19:23:26 | +1789221206228 | ⛓ hash | HASH seq=2 35038e6f445b... (click:filter) |
| 19:23:26 | +1789221206244 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:23:26 | +1789221206261 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:23:26 | +1789221206368 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=107 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:23:26 | +1789221206368 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:23:26 | +1789221206377 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:23:26 | +1789221206838 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:23:26 | +1789221206842 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:23:26 | +1789221206842 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 19:23:26 | +1789221206920 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=77 · result=ok · candidate=Redmi Note 8GB |
| 19:23:26 | +1789221206928 | • step | ✓ step action: click:check |
| 19:23:26 | +1789221206928 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 19:23:27 | +1789221207358 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:23:27 | +1789221207407 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:23:27 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:23:27 — **end**
