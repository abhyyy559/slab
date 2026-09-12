# SENTRY run — v4/strip

- **started:** 2026-09-12 14:41:06
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:06 | +1789204266403 | · PERTURB_INJECTED | target=strip · seq=0 |
| 14:41:07 | +1789204267199 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=75 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=strip |
| 14:41:07 | +1789204267199 | • step | ✓ step action: goto:search |
| 14:41:07 | +1789204267203 | ⛓ hash | HASH seq=1 00d071ad25b4... (goto:search) |
| 14:41:07 | +1789204267544 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 14:41:07 | +1789204267640 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.88 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:07 | +1789204267683 | · click | seq=2 · step=2 · target=filter_button · confidence=0.88 · signals=['role_name', 'text', 'visual'] · duration_ms=40 · result=ok |
| 14:41:07 | +1789204267687 | • step | ✓ step action: click:filter |
| 14:41:07 | +1789204267689 | ⛓ hash | HASH seq=2 2ae1b5ba55e9... (click:filter) |
| 14:41:07 | +1789204267704 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:07 | +1789204267740 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=32 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:07 | +1789204267744 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:07 | +1789204267746 | ⛓ hash | HASH seq=3 51c04ef6a7ae... (goto:delivery:Pixel Lite 8GB) |
| 14:41:08 | +1789204268089 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:08 | +1789204268089 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:41:08 | +1789204268089 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Pixel%20Lite%208GB · mode=cli |
| 14:41:08 | +1789204268136 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=43 · result=ok · candidate=Pixel Lite 8GB |
| 14:41:08 | +1789204268139 | • step | ✓ step action: click:check |
| 14:41:08 | +1789204268141 | ⛓ hash | HASH seq=4 fa30951fc289... (click:check) |
| 14:41:11 | +1789204271170 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:41:11 | +1789204271185 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:41:11 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:41:11 — **end**
