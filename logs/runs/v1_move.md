# SENTRY run — v1/move

- **started:** 2026-09-12 16:04:59
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:04:59 | +1789209299797 | · PERTURB_INJECTED | target=move · seq=0 |
| 16:05:00 | +1789209300863 | · BROWSER_WINDOW | mode=headed · raised=True · slow_mo=1000 · keep_open_ms=4000 · stage={'screen_w': 1536, 'screen_h': 960} |
| 16:05:02 | +1789209302011 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=1141 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=move |
| 16:05:02 | +1789209302013 | • step | ✓ step action: goto:search |
| 16:05:02 | +1789209302017 | ⛓ hash | HASH seq=1 b0f62bd5ec8d... (goto:search) |
| 16:05:02 | +1789209302404 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789209302372 · time_to_detect_ms=10 · strategy=re_locate · time_to_heal_ms=20 · verified=False |
| 16:05:02 | +1789209302404 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 16:05:02 | +1789209302406 | ✓ healed | ✓ HEALED in 20ms (verified=False) |
| 16:05:02 | +1789209302435 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:05:04 | +1789209304560 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789209304518 · time_to_detect_ms=29 · strategy=re_locate · time_to_heal_ms=13 · verified=False |
| 16:05:04 | +1789209304560 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 16:05:04 | +1789209304560 | ✓ healed | ✓ HEALED in 13ms (verified=False) |
| 16:05:04 | +1789209304605 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:05:05 | +1789209305706 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=1066 · result=ok |
| 16:05:05 | +1789209305708 | • step | ✓ step action: click:filter |
| 16:05:05 | +1789209305712 | ⛓ hash | HASH seq=2 e14da8d49099... (click:filter) |
| 16:05:05 | +1789209305731 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:05:05 | +1789209305743 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:05:06 | +1789209306835 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=1089 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:05:06 | +1789209306835 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:05:06 | +1789209306846 | ⛓ hash | HASH seq=3 246060fc45d4... (goto:delivery:Redmi Note 8GB) |
| 16:05:08 | +1789209308232 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789209308198 · time_to_detect_ms=19 · strategy=re_locate · time_to_heal_ms=14 · verified=False |
| 16:05:08 | +1789209308233 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 16:05:08 | +1789209308236 | ✓ healed | ✓ HEALED in 14ms (verified=False) |
| 16:05:08 | +1789209308276 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:05:08 | +1789209308315 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=browser_modal |
| 16:05:10 | +1789209310471 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · mode=browser_modal |
| 16:05:11 | +1789209311516 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=1045 · result=ok · candidate=Redmi Note 8GB |
| 16:05:11 | +1789209311522 | • step | ✓ step action: click:check |
| 16:05:11 | +1789209311522 | ⛓ hash | HASH seq=4 c9a258ecff44... (click:check) |
| 16:05:14 | +1789209314551 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:05:14 | +1789209314575 | 📊 metric | METRIC detect=19ms heal=15ms extra=0 status=pass |

**finished:** 2026-09-12 16:05:14 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 3

**finished:** 2026-09-12 16:05:18 — **end**
