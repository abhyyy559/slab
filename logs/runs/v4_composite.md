# SENTRY run — v4/composite

- **started:** 2026-09-12 14:40:13
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:40:13 | +1789204213562 | · PERTURB_INJECTED | target=composite · seq=0 |
| 14:40:14 | +1789204214142 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=81 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=composite |
| 14:40:14 | +1789204214142 | • step | ✓ step action: goto:search |
| 14:40:14 | +1789204214143 | ⛓ hash | HASH seq=1 92844c7cdd9d... (goto:search) |
| 14:40:15 | +1789204215197 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789204214484 · time_to_detect_ms=7 · strategy=re_plan · steps=['dismissed:#chaos-confirm', 'dismissed:#chaos-modal'] · time_to_heal_ms=705 · verified=False |
| 14:40:15 | +1789204215198 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 14:40:15 | +1789204215199 | ✓ healed | ✓ HEALED in 705ms (verified=False) |
| 14:40:15 | +1789204215250 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 14:40:15 | +1789204215387 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789204215363 · time_to_detect_ms=13 · strategy=re_locate · time_to_heal_ms=10 · verified=False |
| 14:40:15 | +1789204215387 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 14:40:15 | +1789204215389 | ✓ healed | ✓ HEALED in 10ms (verified=False) |
| 14:40:15 | +1789204215416 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:40:15 | +1789204215458 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=40 · result=ok |
| 14:40:15 | +1789204215460 | • step | ✓ step action: click:filter |
| 14:40:15 | +1789204215461 | ⛓ hash | HASH seq=2 96aa43cf476a... (click:filter) |
| 14:40:15 | +1789204215475 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:40:15 | +1789204215514 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=35 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:40:15 | +1789204215514 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:40:15 | +1789204215514 | ⛓ hash | HASH seq=3 2267c5022de7... (goto:delivery:Pixel Lite 8GB) |
| 14:40:15 | +1789204215923 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789204215902 · time_to_detect_ms=12 · strategy=re_locate · time_to_heal_ms=2 · verified=False |
| 14:40:15 | +1789204215923 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 14:40:15 | +1789204215923 | ✓ healed | ✓ HEALED in 2ms (verified=False) |
| 14:40:15 | +1789204215951 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:40:15 | +1789204215957 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:40:15 | +1789204215958 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Pixel%20Lite%208GB · mode=cli |
| 14:40:15 | +1789204215985 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=26 · result=ok · candidate=Pixel Lite 8GB |
| 14:40:15 | +1789204215986 | • step | ✓ step action: click:check |
| 14:40:15 | +1789204215988 | ⛓ hash | HASH seq=4 2267c5022de7... (click:check) |
| 14:40:19 | +1789204219002 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:40:19 | +1789204219025 | 📊 metric | METRIC detect=10ms heal=239ms extra=2 status=pass |

**finished:** 2026-09-12 14:40:19 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 2 · recoveries 3

**finished:** 2026-09-12 14:40:19 — **end**
