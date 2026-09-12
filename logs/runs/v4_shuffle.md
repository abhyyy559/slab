# SENTRY run — v4/shuffle

- **started:** 2026-09-12 16:01:31
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:31 | +1789209091974 | · PERTURB_INJECTED | target=shuffle · seq=0 |
| 16:01:32 | +1789209092539 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=88 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=shuffle |
| 16:01:32 | +1789209092540 | • step | ✓ step action: goto:search |
| 16:01:32 | +1789209092540 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 16:01:32 | +1789209092916 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:01:32 | +1789209092993 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:33 | +1789209093035 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=40 · result=ok |
| 16:01:33 | +1789209093036 | • step | ✓ step action: click:filter |
| 16:01:33 | +1789209093037 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 16:01:33 | +1789209093047 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:33 | +1789209093053 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:33 | +1789209093101 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=47 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=shuffle&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:33 | +1789209093101 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:33 | +1789209093101 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 16:01:33 | +1789209093435 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:33 | +1789209093436 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=shuffle&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 16:01:33 | +1789209093437 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=shuffle&product=Redmi%20Note%208GB · mode=cli |
| 16:01:33 | +1789209093466 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=28 · result=ok · candidate=Redmi Note 8GB |
| 16:01:33 | +1789209093468 | • step | ✓ step action: click:check |
| 16:01:33 | +1789209093469 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 16:01:36 | +1789209096496 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:01:36 | +1789209096516 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 16:01:36 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 16:01:36 — **end**
