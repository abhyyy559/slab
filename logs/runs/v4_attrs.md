# SENTRY run — v4/attrs

- **started:** 2026-09-12 14:41:16
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:16 | +1789204276627 | · PERTURB_INJECTED | target=attrs · seq=0 |
| 14:41:17 | +1789204277544 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=92 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=attrs |
| 14:41:17 | +1789204277548 | • step | ✓ step action: goto:search |
| 14:41:17 | +1789204277550 | ⛓ hash | HASH seq=1 a6971e264d7d... (goto:search) |
| 14:41:17 | +1789204277915 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:41:18 | +1789204278003 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:18 | +1789204278048 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=41 · result=ok |
| 14:41:18 | +1789204278050 | • step | ✓ step action: click:filter |
| 14:41:18 | +1789204278052 | ⛓ hash | HASH seq=2 6632c0d30fc8... (click:filter) |
| 14:41:18 | +1789204278072 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:18 | +1789204278106 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=26 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:18 | +1789204278114 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:18 | +1789204278116 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:41:18 | +1789204278507 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:18 | +1789204278520 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:41:18 | +1789204278526 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=attrs&product=Pixel%20Lite%208GB · mode=cli |
| 14:41:18 | +1789204278579 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=49 · result=ok · candidate=Pixel Lite 8GB |
| 14:41:18 | +1789204278585 | • step | ✓ step action: click:check |
| 14:41:18 | +1789204278588 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:41:21 | +1789204281615 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:41:21 | +1789204281638 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:41:21 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:41:21 — **end**
