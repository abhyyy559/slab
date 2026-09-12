# SENTRY run — v4/swap

- **started:** 2026-09-12 14:35:37
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:35:37 | +1789203937488 | · PERTURB_INJECTED | target=swap · seq=0 |
| 14:35:41 | +1789203941276 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=2466 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=swap |
| 14:35:41 | +1789203941282 | • step | ✓ step action: goto:search |
| 14:35:41 | +1789203941284 | ⛓ hash | HASH seq=1 adeb63d5dce7... (goto:search) |
| 14:35:41 | +1789203941708 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:35:41 | +1789203941853 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:35:41 | +1789203941918 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=58 · result=ok |
| 14:35:41 | +1789203941927 | • step | ✓ step action: click:filter |
| 14:35:41 | +1789203941929 | ⛓ hash | HASH seq=2 60a205a5da9e... (click:filter) |
| 14:35:41 | +1789203941949 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:35:42 | +1789203942003 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=46 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:35:42 | +1789203942007 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:35:42 | +1789203942009 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
| 14:35:42 | +1789203942407 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:35:42 | +1789203942413 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Pixel%20Lite%208GB · payload={'pin': '500001'} · mode=cli |
| 14:35:42 | +1789203942417 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=swap&product=Pixel%20Lite%208GB · mode=cli |
| 14:35:42 | +1789203942462 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=41 · result=ok · candidate=Pixel Lite 8GB |
| 14:35:42 | +1789203942465 | • step | ✓ step action: click:check |
| 14:35:42 | +1789203942467 | ⛓ hash | HASH seq=4 d056732a69e6... (click:check) |
| 14:35:45 | +1789203945497 | · delivery_verdict | seq=4 · step=4 · target=Pixel Lite 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 14:35:45 | +1789203945555 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 14:35:45 — **pass**

Chosen: Pixel Lite 8GB @ Rs 18999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 14:35:45 — **end**
