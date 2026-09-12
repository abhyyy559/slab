# SENTRY run — v4/throttle

- **started:** 2026-09-12 14:41:32
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 14:41:32 | +1789204292540 | · PERTURB_INJECTED | target=throttle · seq=0 |
| 14:41:33 | +1789204293403 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=82 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=throttle |
| 14:41:33 | +1789204293408 | • step | ✓ step action: goto:search |
| 14:41:33 | +1789204293410 | ⛓ hash | HASH seq=1 3ccb994ceed1... (goto:search) |
| 14:41:33 | +1789204293747 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 14:41:33 | +1789204293829 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 14:41:33 | +1789204293877 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=41 · result=ok |
| 14:41:33 | +1789204293882 | • step | ✓ step action: click:filter |
| 14:41:33 | +1789204293883 | ⛓ hash | HASH seq=2 3ccb994ceed1... (click:filter) |
| 14:41:33 | +1789204293899 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Pixel Lite 8GB:18999 |
| 14:41:33 | +1789204293935 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=33 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=throttle&product=Pixel%20Lite%208GB · candidate=Pixel Lite 8GB · attempt=1 |
| 14:41:33 | +1789204293939 | • step | ✓ step action: goto:delivery:Pixel Lite 8GB |
| 14:41:33 | +1789204293941 | ⛓ hash | HASH seq=3 23f1ea8eaa86... (goto:delivery:Pixel Lite 8GB) |
