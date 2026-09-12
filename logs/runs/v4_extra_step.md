# SENTRY run — v4/extra_step

- **started:** 2026-09-12 16:01:46
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:46 | +1789209106239 | · PERTURB_INJECTED | target=extra_step · seq=0 |
| 16:01:46 | +1789209106760 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=91 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=extra_step |
| 16:01:46 | +1789209106762 | • step | ✓ step action: goto:search |
| 16:01:46 | +1789209106762 | ⛓ hash | HASH seq=1 695f69c6cb1a... (goto:search) |
| 16:01:47 | +1789209107446 | · RECOVERY · event | trigger=extra_step · expected=clean_page · observed=chaos-confirm visible · detected_at_ms=1789209107090 · time_to_detect_ms=6 · strategy=re_plan · steps=['dismissed:#chaos-confirm'] · time_to_heal_ms=348 · verified=False |
| 16:01:47 | +1789209107448 | ⚠ recovery | ⚠ RECOVERY: extra_step -> re_plan |
| 16:01:47 | +1789209107450 | ✓ healed | ✓ HEALED in 348ms (verified=False) |
| 16:01:47 | +1789209107485 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:01:47 | +1789209107536 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:47 | +1789209107561 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=24 · result=ok |
| 16:01:47 | +1789209107562 | • step | ✓ step action: click:filter |
| 16:01:47 | +1789209107562 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 16:01:47 | +1789209107571 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:47 | +1789209107582 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:47 | +1789209107620 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=36 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:47 | +1789209107620 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:47 | +1789209107620 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 16:01:47 | +1789209107950 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:47 | +1789209107951 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 16:01:47 | +1789209107951 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · mode=cli |
| 16:01:48 | +1789209108001 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=48 · result=ok · candidate=Redmi Note 8GB |
| 16:01:48 | +1789209108002 | • step | ✓ step action: click:check |
| 16:01:48 | +1789209108004 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 16:01:51 | +1789209111026 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:01:51 | +1789209111026 | 📊 metric | METRIC detect=6ms heal=348ms extra=1 status=pass |

**finished:** 2026-09-12 16:01:51 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 1 · recoveries 1

**finished:** 2026-09-12 16:01:51 — **end**
