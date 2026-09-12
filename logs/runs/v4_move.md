# SENTRY run — v4/move

- **started:** 2026-09-12 14:41:11
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:11 | +1789204271367 | · PERTURB_INJECTED | target=move · seq=0 |
| 14:41:12 | +1789204272251 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=77 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=move |
| 14:41:12 | +1789204272251 | • step | ✓ step action: goto:search |
| 14:41:12 | +1789204272257 | ⛓ hash | HASH seq=1 f5e3e80e25a7... (goto:search) |
| 14:41:12 | +1789204272605 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789204272605 · time_to_detect_ms=0 · strategy=re_locate · time_to_heal_ms=0 · verified=False |
| 14:41:12 | +1789204272605 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 14:41:12 | +1789204272621 | ✓ healed | ✓ HEALED in 0ms (verified=False) |
| 14:41:12 | +1789204272691 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:41:12 | +1789204272789 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789204272786 · time_to_detect_ms=3 · strategy=re_locate · time_to_heal_ms=0 · verified=False |
| 14:41:12 | +1789204272789 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 14:41:12 | +1789204272805 | ✓ healed | ✓ HEALED in 0ms (verified=False) |
| 14:41:12 | +1789204272827 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:12 | +1789204272881 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=50 · result=ok |
| 14:41:12 | +1789204272884 | • step | ✓ step action: click:filter |
| 14:41:12 | +1789204272885 | ⛓ hash | HASH seq=2 5e643093e266... (click:filter) |
| 14:41:12 | +1789204272895 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:12 | +1789204272923 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=23 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:12 | +1789204272927 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:12 | +1789204272928 | ⛓ hash | HASH seq=3 a21b843d8e69... (goto:delivery:Pixel Lite 8GB) |
| 14:41:13 | +1789204273293 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789204273283 · time_to_detect_ms=1 · strategy=re_locate · time_to_heal_ms=6 · verified=False |
| 14:41:13 | +1789204273294 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 14:41:13 | +1789204273296 | ✓ healed | ✓ HEALED in 6ms (verified=False) |
| 14:41:13 | +1789204273316 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:13 | +1789204273316 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:41:13 | +1789204273331 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Pixel%20Lite%208GB · mode=cli |
| 14:41:13 | +1789204273373 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=37 · result=ok · candidate=Pixel Lite 8GB |
| 14:41:13 | +1789204273377 | • step | ✓ step action: click:check |
| 14:41:13 | +1789204273378 | ⛓ hash | HASH seq=4 24c7ee3faa02... (click:check) |
| 14:41:16 | +1789204276403 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:41:16 | +1789204276418 | 📊 metric | METRIC detect=1ms heal=2ms extra=0 status=pass |

**finished:** 2026-09-12 14:41:16 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 3

**finished:** 2026-09-12 14:41:16 — **end**
