# SENTRY run — v4/rename

- **started:** 2026-09-12 16:01:36
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:36 | +1789209096623 | · PERTURB_INJECTED | target=rename · seq=0 |
| 16:01:37 | +1789209097159 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=98 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename |
| 16:01:37 | +1789209097160 | • step | ✓ step action: goto:search |
| 16:01:37 | +1789209097161 | ⛓ hash | HASH seq=1 e3d8d082eea9... (goto:search) |
| 16:01:37 | +1789209097508 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789209097498 · time_to_detect_ms=3 · strategy=re_locate · time_to_heal_ms=7 · verified=False |
| 16:01:37 | +1789209097508 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 16:01:37 | +1789209097508 | ✓ healed | ✓ HEALED in 7ms (verified=False) |
| 16:01:37 | +1789209097565 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:01:37 | +1789209097637 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789209097629 · time_to_detect_ms=3 · strategy=re_locate · time_to_heal_ms=5 · verified=False |
| 16:01:37 | +1789209097638 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 16:01:37 | +1789209097638 | ✓ healed | ✓ HEALED in 5ms (verified=False) |
| 16:01:37 | +1789209097664 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:37 | +1789209097713 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=47 · result=ok |
| 16:01:37 | +1789209097714 | • step | ✓ step action: click:filter |
| 16:01:37 | +1789209097714 | ⛓ hash | HASH seq=2 8abc8136a040... (click:filter) |
| 16:01:37 | +1789209097727 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:37 | +1789209097737 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:37 | +1789209097786 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=46 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:37 | +1789209097787 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:37 | +1789209097788 | ⛓ hash | HASH seq=3 8693c8664bfa... (goto:delivery:Redmi Note 8GB) |
| 16:01:38 | +1789209098133 | · RECOVERY · event | trigger=label_renamed · expected=clean_page · observed=Verify Shipment · detected_at_ms=1789209098127 · time_to_detect_ms=2 · strategy=re_locate · time_to_heal_ms=3 · verified=False |
| 16:01:38 | +1789209098133 | ⚠ recovery | ⚠ RECOVERY: label_renamed -> re_locate |
| 16:01:38 | +1789209098133 | ✓ healed | ✓ HEALED in 3ms (verified=False) |
| 16:01:38 | +1789209098154 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:38 | +1789209098154 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 16:01:38 | +1789209098155 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Redmi%20Note%208GB · mode=cli |
| 16:01:38 | +1789209098175 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=20 · result=ok · candidate=Redmi Note 8GB |
| 16:01:38 | +1789209098176 | • step | ✓ step action: click:check |
| 16:01:38 | +1789209098177 | ⛓ hash | HASH seq=4 5b840b9e89d4... (click:check) |
| 16:01:41 | +1789209101194 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:01:41 | +1789209101217 | 📊 metric | METRIC detect=2ms heal=5ms extra=0 status=pass |

**finished:** 2026-09-12 16:01:41 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 3

**finished:** 2026-09-12 16:01:41 — **end**
