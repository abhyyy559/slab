# SENTRY run — v4/shuffle

- **started:** 2026-09-12 14:39:49
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:39:49 | +1789204189230 | · PERTURB_INJECTED | target=shuffle · seq=0 |
| 14:39:49 | +1789204189859 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=100 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=shuffle |
| 14:39:49 | +1789204189861 | • step | ✓ step action: goto:search |
| 14:39:49 | +1789204189862 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:39:50 | +1789204190233 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:39:50 | +1789204190307 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:39:50 | +1789204190374 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=65 · result=ok |
| 14:39:50 | +1789204190374 | • step | ✓ step action: click:filter |
| 14:39:50 | +1789204190375 | ⛓ hash | HASH seq=2 6b972fe47205... (click:filter) |
| 14:39:50 | +1789204190387 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:39:50 | +1789204190420 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=31 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=shuffle&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:39:50 | +1789204190424 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:39:50 | +1789204190425 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:39:50 | +1789204190754 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:39:50 | +1789204190755 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=shuffle&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:39:50 | +1789204190756 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=shuffle&product=Pixel%20Lite%208GB · mode=cli |
| 14:39:50 | +1789204190802 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=44 · result=ok · candidate=Pixel Lite 8GB |
| 14:39:50 | +1789204190802 | • step | ✓ step action: click:check |
| 14:39:50 | +1789204190803 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:39:53 | +1789204193819 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:39:53 | +1789204193834 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:39:53 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:39:53 — **end**
