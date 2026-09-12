# SENTRY run — v4/extra_step

- **started:** 2026-09-12 19:27:44
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 19:27:44 | +1789221464031 | · PERTURB_INJECTED | target=extra_step · seq=0 |
| 19:27:45 | +1789221465343 | · BROWSER_WINDOW | mode=headed · raised=True · slow_mo=1999 · keep_open_ms=4000 · stage={'screen_w': 1536, 'screen_h': 960} |
| 19:27:47 | +1789221467947 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=2601 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=extra_step |
| 19:27:47 | +1789221467947 | • step | ✓ step action: goto:search |
| 19:27:47 | +1789221467961 | ⛓ hash | HASH seq=1 695f69c6cb1a... (goto:search) |
| 19:27:50 | +1789221470992 | · RECOVERY · event | trigger=extra_step · expected=clean_page · observed=chaos-confirm visible · detected_at_ms=1789221468496 · time_to_detect_ms=50 · strategy=re_plan · steps=['dismissed:#chaos-confirm'] · time_to_heal_ms=2446 · verified=False |
| 19:27:50 | +1789221470997 | ⚠ recovery | ⚠ RECOVERY: extra_step -> re_plan |
| 19:27:51 | +1789221471000 | ✓ healed | ✓ HEALED in 2446ms (verified=False) |
| 19:27:51 | +1789221471113 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:27:53 | +1789221473202 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:27:55 | +1789221475237 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:27:55 | +1789221475324 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:27:57 | +1789221477452 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=2084 · result=ok |
| 19:27:57 | +1789221477452 | • step | ✓ step action: click:filter |
| 19:27:57 | +1789221477455 | ⛓ hash | HASH seq=2 65409d2577ee... (click:filter) |
| 19:27:57 | +1789221477470 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:27:57 | +1789221477486 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:27:57 | +1789221477489 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:27:59 | +1789221479593 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=2100 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:27:59 | +1789221479599 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:27:59 | +1789221479601 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:28:01 | +1789221481939 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:28:02 | +1789221482047 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:28:02 | +1789221482095 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=browser_modal |
| 19:28:09 | +1789221489271 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Redmi%20Note%208GB · mode=browser_modal |
| 19:28:11 | +1789221491334 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=2061 · result=ok · candidate=Redmi Note 8GB |
| 19:28:11 | +1789221491336 | • step | ✓ step action: click:check |
| 19:28:11 | +1789221491339 | ⛓ hash | HASH seq=4 2fc35734b4a1... (click:check) |
