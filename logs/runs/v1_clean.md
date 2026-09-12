# SENTRY run — v1/clean

- **started:** 2026-09-12 14:41:16
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:16 | +1789204276730 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=81 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 14:41:16 | +1789204276732 | • step | ✓ step action: goto:search |
| 14:41:16 | +1789204276738 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:41:17 | +1789204277072 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:41:17 | +1789204277144 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:17 | +1789204277222 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=64 · result=ok |
| 14:41:17 | +1789204277223 | • step | ✓ step action: click:filter |
| 14:41:17 | +1789204277225 | ⛓ hash | HASH seq=2 f64d4b85c2c3... (click:filter) |
| 14:41:17 | +1789204277242 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:17 | +1789204277286 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=41 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:17 | +1789204277289 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:17 | +1789204277291 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:41:17 | +1789204277620 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:17 | +1789204277635 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:41:17 | +1789204277636 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · mode=cli |
| 14:41:17 | +1789204277695 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=57 · result=ok · candidate=Pixel Lite 8GB |
| 14:41:17 | +1789204277696 | • step | ✓ step action: click:check |
| 14:41:17 | +1789204277697 | ⛓ hash | HASH seq=4 96777ddd79d4... (click:check) |
| 14:41:18 | +1789204278117 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:41:18 | +1789204278131 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:41:18 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:41:18 — **end**
