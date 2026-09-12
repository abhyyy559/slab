# SENTRY run — v1/clean

- **started:** 2026-09-12 20:10:05
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 20:10:07 | +1789224007555 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=137 · result=ok · url=http://127.0.0.1:8001/site_a/search.html |
| 20:10:07 | +1789224007555 | • step | ✓ step action: goto:search |
| 20:10:07 | +1789224007566 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 20:10:07 | +1789224007963 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 20:10:08 | +1789224008007 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 20:10:08 | +1789224008038 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 20:10:08 | +1789224008091 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 20:10:08 | +1789224008200 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=79 · result=ok |
| 20:10:08 | +1789224008201 | • step | ✓ step action: click:filter |
| 20:10:08 | +1789224008202 | ⛓ hash | HASH seq=2 53f6bf1018b9... (click:filter) |
| 20:10:08 | +1789224008217 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 20:10:08 | +1789224008225 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 20:10:08 | +1789224008227 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 20:10:08 | +1789224008282 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=53 · result=ok · url=http://127.0.0.1:8001/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 20:10:08 | +1789224008283 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 20:10:08 | +1789224008284 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 20:10:08 | +1789224008585 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 20:10:08 | +1789224008653 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 20:10:08 | +1789224008668 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8001/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 20:10:08 | +1789224008670 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8001/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 20:10:08 | +1789224008728 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=55 · result=ok · candidate=Redmi Note 8GB |
| 20:10:08 | +1789224008732 | • step | ✓ step action: click:check |
| 20:10:08 | +1789224008733 | ⛓ hash | HASH seq=4 d4be8bb4f6a2... (click:check) |
| 20:10:09 | +1789224009160 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 20:10:09 | +1789224009165 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 20:10:09 | +1789224009176 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 20:10:09 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 20:10:09 — **end**
