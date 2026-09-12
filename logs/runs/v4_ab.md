# SENTRY run — v4/ab

- **started:** 2026-09-12 19:40:24
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:40:24 | +1789222224588 | · PERTURB_INJECTED | target=ab · seq=0 |
| 19:40:26 | +1789222226277 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=256 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=ab |
| 19:40:26 | +1789222226277 | • step | ✓ step action: goto:search |
| 19:40:26 | +1789222226285 | ⛓ hash | HASH seq=1 0be231dd0986... (goto:search) |
| 19:40:26 | +1789222226815 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:40:26 | +1789222226863 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:40:26 | +1789222226898 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:40:27 | +1789222227043 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:40:27 | +1789222227155 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=107 · result=ok |
| 19:40:27 | +1789222227164 | • step | ✓ step action: click:filter |
| 19:40:27 | +1789222227176 | ⛓ hash | HASH seq=2 5b834e3418d4... (click:filter) |
| 19:40:27 | +1789222227205 | · STOCK_FILTER | excluded=1 · detail=out of stock, not eligible: ['Lava Blaze 8GB'] |
| 19:40:27 | +1789222227229 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:40:27 | +1789222227229 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Oppo A 8GB@16499,iQoo Z 8GB@18999 |
| 19:40:27 | +1789222227328 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=88 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=ab&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:40:27 | +1789222227328 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:40:27 | +1789222227336 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:40:27 | +1789222227708 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:40:27 | +1789222227938 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:40:27 | +1789222227948 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=ab&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:40:27 | +1789222227953 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=ab&product=Redmi%20Note%208GB · mode=cli |
| 19:40:28 | +1789222228081 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=127 · result=ok · candidate=Redmi Note 8GB |
| 19:40:28 | +1789222228092 | • step | ✓ step action: click:check |
| 19:40:28 | +1789222228097 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 19:40:31 | +1789222231157 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:40:31 | +1789222231180 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:40:31 | +1789222231254 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:40:31 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:40:31 — **end**
