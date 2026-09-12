# SENTRY run — v6/clean

- **started:** 2026-09-12 19:41:09
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:41:10 | +1789222270920 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=263 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 19:41:10 | +1789222270940 | • step | ✓ step action: goto:search |
| 19:41:10 | +1789222270946 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 19:41:11 | +1789222271469 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:41:11 | +1789222271519 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:13000 |
| 19:41:11 | +1789222271560 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:41:11 | +1789222271716 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:41:11 | +1789222271806 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=82 · result=ok |
| 19:41:11 | +1789222271815 | • step | ✓ step action: click:filter |
| 19:41:11 | +1789222271815 | ⛓ hash | HASH seq=2 2a754d884f33... (click:filter) |
| 19:41:11 | +1789222271847 | · STOCK_FILTER | excluded=1 · detail=out of stock, not eligible: ['Lava Blaze 8GB'] |
| 19:41:11 | +1789222271866 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:41:11 | +1789222271882 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999 |
| 19:41:11 | +1789222271975 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=87 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:41:11 | +1789222271992 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:41:11 | +1789222271992 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:41:12 | +1789222272343 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:41:12 | +1789222272544 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:41:12 | +1789222272558 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:41:12 | +1789222272562 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 19:41:12 | +1789222272667 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=104 · result=ok · candidate=Redmi Note 8GB |
| 19:41:12 | +1789222272684 | • step | ✓ step action: click:check |
| 19:41:12 | +1789222272695 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 19:41:13 | +1789222273149 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:41:13 | +1789222273191 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:41:13 | +1789222273296 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:41:13 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:41:13 — **end**
