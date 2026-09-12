# SENTRY run — v4/rename_strip

- **started:** 2026-09-12 19:38:59
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:38:59 | +1789222139177 | · PERTURB_INJECTED | target=rename_strip · seq=0 |
| 19:39:00 | +1789222140874 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=227 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename_strip |
| 19:39:00 | +1789222140884 | • step | ✓ step action: goto:search |
| 19:39:00 | +1789222140894 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 19:39:01 | +1789222141444 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:39:01 | +1789222141482 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:39:01 | +1789222141532 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:39:01 | +1789222141708 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:39:01 | +1789222141826 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=99 · result=ok |
| 19:39:01 | +1789222141835 | • step | ✓ step action: click:filter |
| 19:39:01 | +1789222141835 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 19:39:01 | +1789222141876 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:39:01 | +1789222141901 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:39:01 | +1789222141906 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:39:02 | +1789222142017 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=105 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:39:02 | +1789222142024 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:39:02 | +1789222142024 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:39:02 | +1789222142375 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:39:02 | +1789222142606 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:39:02 | +1789222142614 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:39:02 | +1789222142614 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Redmi%20Note%208GB · mode=cli |
| 19:39:02 | +1789222142710 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=90 · result=ok · candidate=Redmi Note 8GB |
| 19:39:02 | +1789222142717 | • step | ✓ step action: click:check |
| 19:39:02 | +1789222142721 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 19:39:05 | +1789222145792 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:39:05 | +1789222145809 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:39:05 | +1789222145876 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 19:39:05 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 19:39:05 — **end**
