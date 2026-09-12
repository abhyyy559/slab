# SENTRY run — v4/rename

- **started:** 2026-09-12 14:41:01
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:01 | +1789204261254 | · PERTURB_INJECTED | target=rename · seq=0 |
| 14:41:02 | +1789204262097 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=87 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename |
| 14:41:02 | +1789204262100 | • step | ✓ step action: goto:search |
| 14:41:02 | +1789204262129 | ⛓ hash | HASH seq=1 1c5a4644321a... (goto:search) |
| 14:41:02 | +1789204262489 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789204262473 · time_to_detect_ms=0 · strategy=re_locate · time_to_heal_ms=16 · verified=False |
| 14:41:02 | +1789204262516 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 14:41:02 | +1789204262518 | ✓ healed | ✓ HEALED in 16ms (verified=False) |
| 14:41:02 | +1789204262576 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:41:02 | +1789204262638 | · RECOVERY · event | trigger=label_renamed+label_renamed · expected=clean_page · observed=Refine Results+Look Up · detected_at_ms=1789204262629 · time_to_detect_ms=3 · strategy=re_locate · time_to_heal_ms=5 · verified=False |
| 14:41:02 | +1789204262639 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed -> re_locate |
| 14:41:02 | +1789204262640 | ✓ healed | ✓ HEALED in 5ms (verified=False) |
| 14:41:02 | +1789204262657 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:02 | +1789204262720 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=60 · result=ok |
| 14:41:02 | +1789204262722 | • step | ✓ step action: click:filter |
| 14:41:02 | +1789204262723 | ⛓ hash | HASH seq=2 77508ff6b8ec... (click:filter) |
| 14:41:02 | +1789204262734 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:02 | +1789204262764 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=29 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:02 | +1789204262768 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:02 | +1789204262769 | ⛓ hash | HASH seq=3 52dcb21539b9... (goto:delivery:Pixel Lite 8GB) |
| 14:41:03 | +1789204263110 | · RECOVERY · event | trigger=label_renamed · expected=clean_page · observed=Verify Shipment · detected_at_ms=1789204263101 · time_to_detect_ms=3 · strategy=re_locate · time_to_heal_ms=4 · verified=False |
| 14:41:03 | +1789204263110 | ⚠ recovery | ⚠ RECOVERY: label_renamed -> re_locate |
| 14:41:03 | +1789204263111 | ✓ healed | ✓ HEALED in 4ms (verified=False) |
| 14:41:03 | +1789204263131 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:03 | +1789204263131 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:41:03 | +1789204263142 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename&product=Pixel%20Lite%208GB · mode=cli |
| 14:41:03 | +1789204263164 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=19 · result=ok · candidate=Pixel Lite 8GB |
| 14:41:03 | +1789204263166 | • step | ✓ step action: click:check |
| 14:41:03 | +1789204263168 | ⛓ hash | HASH seq=4 b92a228914ae... (click:check) |
| 14:41:06 | +1789204266185 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:41:06 | +1789204266230 | 📊 metric | METRIC detect=2ms heal=8ms extra=0 status=pass |

**finished:** 2026-09-12 14:41:06 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 3

**finished:** 2026-09-12 14:41:06 — **end**
