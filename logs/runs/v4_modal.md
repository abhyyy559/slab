# SENTRY run — v4/modal

- **started:** 2026-09-12 14:41:21
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:21 | +1789204281838 | · PERTURB_INJECTED | target=modal · seq=0 |
| 14:41:22 | +1789204282698 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=91 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=modal |
| 14:41:22 | +1789204282701 | • step | ✓ step action: goto:search |
| 14:41:22 | +1789204282703 | ⛓ hash | HASH seq=1 911fc9d30701... (goto:search) |
| 14:41:23 | +1789204283401 | · RECOVERY · event | trigger=modal · expected=clean_page · observed=chaos-modal visible · detected_at_ms=1789204283039 · time_to_detect_ms=0 · strategy=re_plan · steps=['dismissed:#chaos-modal'] · time_to_heal_ms=360 · verified=False |
| 14:41:23 | +1789204283401 | ⚠ recovery | ⚠ RECOVERY: modal -> re_plan |
| 14:41:23 | +1789204283403 | ✓ healed | ✓ HEALED in 360ms (verified=False) |
| 14:41:23 | +1789204283439 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:41:23 | +1789204283486 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:23 | +1789204283523 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=35 · result=ok |
| 14:41:23 | +1789204283528 | • step | ✓ step action: click:filter |
| 14:41:23 | +1789204283529 | ⛓ hash | HASH seq=2 6b972fe47205... (click:filter) |
| 14:41:23 | +1789204283538 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:23 | +1789204283569 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=27 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:23 | +1789204283571 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:23 | +1789204283574 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:41:23 | +1789204283915 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:23 | +1789204283917 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:41:23 | +1789204283920 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Pixel%20Lite%208GB · mode=cli |
| 14:41:23 | +1789204283969 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=46 · result=ok · candidate=Pixel Lite 8GB |
| 14:41:23 | +1789204283971 | • step | ✓ step action: click:check |
| 14:41:23 | +1789204283972 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:41:26 | +1789204286993 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:41:27 | +1789204287009 | 📊 metric | METRIC detect=0ms heal=360ms extra=1 status=pass |

**finished:** 2026-09-12 14:41:27 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 1 · recoveries 1

**finished:** 2026-09-12 14:41:27 — **end**
