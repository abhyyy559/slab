# SENTRY run — v4/rename_strip

- **started:** 2026-09-12 14:35:01
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:35:01 | +1789203901226 | · PERTURB_INJECTED | target=rename_strip · seq=0 |
| 14:35:02 | +1789203902645 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=141 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=rename_strip |
| 14:35:02 | +1789203902651 | • step | ✓ step action: goto:search |
| 14:35:02 | +1789203902658 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:35:03 | +1789203903120 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:35:03 | +1789203903280 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:35:03 | +1789203903351 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=65 · result=ok |
| 14:35:03 | +1789203903355 | • step | ✓ step action: click:filter |
| 14:35:03 | +1789203903360 | ⛓ hash | HASH seq=2 6b972fe47205... (click:filter) |
| 14:35:03 | +1789203903392 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:35:03 | +1789203903463 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=62 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:35:03 | +1789203903468 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:35:03 | +1789203903472 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:35:03 | +1789203903913 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:35:03 | +1789203903922 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:35:03 | +1789203903930 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=rename_strip&product=Pixel%20Lite%208GB · mode=cli |
| 14:35:04 | +1789203904001 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=66 · result=ok · candidate=Pixel Lite 8GB |
| 14:35:04 | +1789203904007 | • step | ✓ step action: click:check |
| 14:35:04 | +1789203904010 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:35:07 | +1789203907041 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:35:07 | +1789203907084 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:35:07 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:35:07 — **end**
