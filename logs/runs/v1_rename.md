# SENTRY run — v1/rename

- **started:** 2026-09-12 16:05:37
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:05:37 | +1789209337377 | · PERTURB_INJECTED | target=rename · seq=0 |
| 16:05:38 | +1789209338258 | · BROWSER_WINDOW | mode=headed · raised=True · slow_mo=1000 · keep_open_ms=4000 · stage={'screen_w': 1536, 'screen_h': 960} |
| 16:05:39 | +1789209339382 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=1118 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename |
| 16:05:39 | +1789209339389 | • step | ✓ step action: goto:search |
| 16:05:39 | +1789209339398 | ⛓ hash | HASH seq=1 e3d8d082eea9... (goto:search) |
| 16:05:39 | +1789209339806 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789209339770 · time_to_detect_ms=21 · strategy=re_locate · time_to_heal_ms=14 · verified=False |
| 16:05:39 | +1789209339807 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 16:05:39 | +1789209339808 | ✓ healed | ✓ HEALED in 14ms (verified=False) |
| 16:05:39 | +1789209339835 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:05:41 | +1789209341971 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789209341938 · time_to_detect_ms=21 · strategy=re_locate · time_to_heal_ms=11 · verified=False |
| 16:05:41 | +1789209341972 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 16:05:41 | +1789209341974 | ✓ healed | ✓ HEALED in 11ms (verified=False) |
| 16:05:41 | +1789209341992 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:05:43 | +1789209343080 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=1059 · result=ok |
| 16:05:43 | +1789209343080 | • step | ✓ step action: click:filter |
| 16:05:43 | +1789209343080 | ⛓ hash | HASH seq=2 beacdb654a3a... (click:filter) |
| 16:05:43 | +1789209343100 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:05:43 | +1789209343104 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:05:44 | +1789209344197 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=1093 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:05:44 | +1789209344202 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:05:44 | +1789209344204 | ⛓ hash | HASH seq=3 8693c8664bfa... (goto:delivery:Redmi Note 8GB) |
| 16:05:45 | +1789209345575 | · RECOVERY · event | trigger=label_renamed · expected=clean_page · observed=Verify Shipment · detected_at_ms=1789209345546 · time_to_detect_ms=22 · strategy=re_locate · time_to_heal_ms=7 · verified=False |
| 16:05:45 | +1789209345575 | ⚠ recovery | ⚠ RECOVERY: label_renamed -> re_locate |
| 16:05:45 | +1789209345575 | ✓ healed | ✓ HEALED in 7ms (verified=False) |
| 16:05:45 | +1789209345603 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:05:45 | +1789209345633 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=browser_modal |
| 16:05:48 | +1789209348124 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · mode=browser_modal |
| 16:05:49 | +1789209349183 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=1059 · result=ok · candidate=Redmi Note 8GB |
| 16:05:49 | +1789209349183 | • step | ✓ step action: click:check |
| 16:05:49 | +1789209349183 | ⛓ hash | HASH seq=4 db2ca4c60099... (click:check) |
| 16:05:52 | +1789209352213 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:05:52 | +1789209352238 | 📊 metric | METRIC detect=21ms heal=10ms extra=0 status=pass |

**finished:** 2026-09-12 16:05:52 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 3

**finished:** 2026-09-12 16:05:56 — **end**
