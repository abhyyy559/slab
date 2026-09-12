# SENTRY run — v4/extra_step

- **started:** 2026-09-12 14:41:27
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:27 | +1789204287171 | · PERTURB_INJECTED | target=extra_step · seq=0 |
| 14:41:27 | +1789204287984 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=94 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=extra_step |
| 14:41:27 | +1789204287988 | • step | ✓ step action: goto:search |
| 14:41:27 | +1789204287991 | ⛓ hash | HASH seq=1 14d2978d562b... (goto:search) |
| 14:41:28 | +1789204288694 | · RECOVERY · event | trigger=extra_step · expected=clean_page · observed=chaos-confirm visible · detected_at_ms=1789204288323 · time_to_detect_ms=0 · strategy=re_plan · steps=['dismissed:#chaos-confirm'] · time_to_heal_ms=363 · verified=False |
| 14:41:28 | +1789204288698 | ⚠ recovery | ⚠ RECOVERY: extra_step -> re_plan |
| 14:41:28 | +1789204288702 | ✓ healed | ✓ HEALED in 363ms (verified=False) |
| 14:41:28 | +1789204288747 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:41:28 | +1789204288798 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:28 | +1789204288866 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=64 · result=ok |
| 14:41:28 | +1789204288870 | • step | ✓ step action: click:filter |
| 14:41:28 | +1789204288873 | ⛓ hash | HASH seq=2 6b972fe47205... (click:filter) |
| 14:41:28 | +1789204288887 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:28 | +1789204288932 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=37 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:28 | +1789204288941 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:28 | +1789204288944 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:41:29 | +1789204289284 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:29 | +1789204289286 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:41:29 | +1789204289290 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=extra_step&product=Pixel%20Lite%208GB · mode=cli |
| 14:41:29 | +1789204289330 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=36 · result=ok · candidate=Pixel Lite 8GB |
| 14:41:29 | +1789204289333 | • step | ✓ step action: click:check |
| 14:41:29 | +1789204289334 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:41:32 | +1789204292360 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:41:32 | +1789204292386 | 📊 metric | METRIC detect=0ms heal=363ms extra=1 status=pass |

**finished:** 2026-09-12 14:41:32 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 1 · recoveries 1

**finished:** 2026-09-12 14:41:32 — **end**
