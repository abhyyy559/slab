# SENTRY run — v4/clean

- **started:** 2026-09-12 14:39:46
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:39:47 | +1789204187603 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=115 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 14:39:47 | +1789204187604 | • step | ✓ step action: goto:search |
| 14:39:47 | +1789204187610 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:39:47 | +1789204187970 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:39:48 | +1789204188080 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:39:48 | +1789204188156 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=73 · result=ok |
| 14:39:48 | +1789204188157 | • step | ✓ step action: click:filter |
| 14:39:48 | +1789204188158 | ⛓ hash | HASH seq=2 6b972fe47205... (click:filter) |
| 14:39:48 | +1789204188174 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:39:48 | +1789204188232 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=57 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:39:48 | +1789204188233 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:39:48 | +1789204188234 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:39:48 | +1789204188611 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:39:48 | +1789204188614 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:39:48 | +1789204188616 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Pixel%20Lite%208GB · mode=cli |
| 14:39:48 | +1789204188659 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=41 · result=ok · candidate=Pixel Lite 8GB |
| 14:39:48 | +1789204188661 | • step | ✓ step action: click:check |
| 14:39:48 | +1789204188662 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:39:49 | +1789204189095 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:39:49 | +1789204189119 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:39:49 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:39:49 — **end**
