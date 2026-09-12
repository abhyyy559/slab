# SENTRY run — v2/clean

- **started:** 2026-09-12 14:38:34
- **goal:** (none)

| t | ts | event | detail |
|---|---|---|---|
| 14:38:35 | +1789204115796 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=82 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 14:38:35 | +1789204115799 | • step | ✓ step action: goto:search |
| 14:38:35 | +1789204115800 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:38:36 | +1789204116170 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:38:36 | +1789204116303 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:38:36 | +1789204116388 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=81 · result=ok |
| 14:38:36 | +1789204116389 | • step | ✓ step action: click:filter |
| 14:38:36 | +1789204116390 | ⛓ hash | HASH seq=2 f95c90209cf4... (click:filter) |
| 14:38:36 | +1789204116402 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:38:36 | +1789204116468 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=63 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:38:36 | +1789204116469 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:38:36 | +1789204116472 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:38:36 | +1789204116818 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:38:36 | +1789204116820 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:38:36 | +1789204116822 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · mode=cli |
| 14:38:36 | +1789204116882 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=57 · result=ok · candidate=Pixel Lite 8GB |
| 14:38:36 | +1789204116884 | • step | ✓ step action: click:check |
| 14:38:36 | +1789204116885 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:38:37 | +1789204117312 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:38:37 | +1789204117349 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:38:37 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:38:37 — **end**
