# SENTRY run — v4/swap

- **started:** 2026-09-12 19:40:04
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:40:04 | +1789222204644 | · PERTURB_INJECTED | target=swap · seq=0 |
| 19:40:06 | +1789222206263 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=305 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=swap |
| 19:40:06 | +1789222206277 | • step | ✓ step action: goto:search |
| 19:40:06 | +1789222206287 | ⛓ hash | HASH seq=1 a59cbaafd60f... (goto:search) |
| 19:40:06 | +1789222206945 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:40:07 | +1789222207007 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:40:07 | +1789222207078 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:40:07 | +1789222207290 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:40:07 | +1789222207410 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=107 · result=ok |
| 19:40:07 | +1789222207423 | • step | ✓ step action: click:filter |
| 19:40:07 | +1789222207431 | ⛓ hash | HASH seq=2 c56a2318d73b... (click:filter) |
| 19:40:07 | +1789222207488 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:40:07 | +1789222207519 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:40:07 | +1789222207530 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:40:07 | +1789222207634 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=97 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:40:07 | +1789222207652 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:40:07 | +1789222207659 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:40:08 | +1789222208022 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:40:08 | +1789222208265 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:40:08 | +1789222208278 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:40:08 | +1789222208285 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Redmi%20Note%208GB · mode=cli |
| 19:40:08 | +1789222208376 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=83 · result=ok · candidate=Redmi Note 8GB |
| 19:40:08 | +1789222208384 | • step | ✓ step action: click:check |
| 19:40:08 | +1789222208387 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 19:40:11 | +1789222211502 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:40:11 | +1789222211570 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:40:11 | +1789222211706 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:40:11 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:40:11 — **end**
