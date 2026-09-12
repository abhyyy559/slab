# SENTRY run — v1/clean

- **started:** 2026-09-12 19:27:44
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:27:46 | +1789221466057 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=255 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 19:27:46 | +1789221466061 | • step | ✓ step action: goto:search |
| 19:27:46 | +1789221466072 | ⛓ hash | HASH seq=1 abbfb3ae47f5... (goto:search) |
| 19:27:46 | +1789221466973 | · RECOVERY · event | trigger=extra_step · expected=clean_page · observed=chaos-confirm visible · detected_at_ms=1789221466581 · time_to_detect_ms=24 · strategy=re_plan · steps=['dismissed:#chaos-confirm'] · time_to_heal_ms=368 · verified=False |
| 19:27:46 | +1789221466973 | ⚠ recovery | ⚠ RECOVERY: extra_step -> re_plan |
| 19:27:46 | +1789221466973 | ✓ healed | ✓ HEALED in 368ms (verified=False) |
| 19:27:47 | +1789221467028 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:27:47 | +1789221467068 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:27:47 | +1789221467084 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:27:47 | +1789221467151 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:27:47 | +1789221467261 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=75 · result=ok |
| 19:27:47 | +1789221467269 | • step | ✓ step action: click:filter |
| 19:27:47 | +1789221467272 | ⛓ hash | HASH seq=2 53f6bf1018b9... (click:filter) |
| 19:27:47 | +1789221467285 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:27:47 | +1789221467302 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:27:47 | +1789221467302 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:27:47 | +1789221467386 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=80 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:27:47 | +1789221467386 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:27:47 | +1789221467392 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:27:47 | +1789221467682 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:27:47 | +1789221467773 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:27:47 | +1789221467797 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:27:47 | +1789221467797 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 19:27:47 | +1789221467847 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=41 · result=ok · candidate=Redmi Note 8GB |
| 19:27:47 | +1789221467847 | • step | ✓ step action: click:check |
| 19:27:47 | +1789221467854 | ⛓ hash | HASH seq=4 d4be8bb4f6a2... (click:check) |
| 19:27:48 | +1789221468281 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:27:48 | +1789221468287 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:27:48 | +1789221468321 | 📊 metric | METRIC detect=24ms heal=368ms extra=1 status=pass |

**finished:** 2026-09-12 19:27:48 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 1 · recoveries 1

**finished:** 2026-09-12 19:27:48 — **end**
