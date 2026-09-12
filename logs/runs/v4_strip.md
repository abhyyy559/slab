# SENTRY run — v4/strip

- **started:** 2026-09-12 15:26:31
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 15:26:31 | +1789206991408 | · PERTURB_INJECTED | target=strip · seq=0 |
| 15:26:32 | +1789206992932 | · BROWSER_WINDOW | mode=headed · raised=True · slow_mo=800 · keep_open_ms=4000 · stage={'screen_w': 1536, 'screen_h': 960} |
| 15:26:34 | +1789206994019 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=1083 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=strip |
| 15:26:34 | +1789206994039 | • step | ✓ step action: goto:search |
| 15:26:34 | +1789206994081 | ⛓ hash | HASH seq=1 35408ad28619... (goto:search) |
| 15:26:34 | +1789206994545 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 15:26:36 | +1789206996308 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.88 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:26:37 | +1789206997232 | · click | seq=2 · step=2 · target=filter_button · confidence=0.88 · signals=['role_name', 'text', 'visual'] · duration_ms=885 · result=ok |
| 15:26:37 | +1789206997237 | • step | ✓ step action: click:filter |
| 15:26:37 | +1789206997237 | ⛓ hash | HASH seq=2 c2dbc58cb4a7... (click:filter) |
| 15:26:37 | +1789206997257 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 15:26:37 | +1789206997271 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 15:26:38 | +1789206998144 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=867 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 15:26:38 | +1789206998156 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 15:26:38 | +1789206998156 | ⛓ hash | HASH seq=3 a42c14bbab0e... (goto:delivery:Redmi Note 8GB) |
| 15:26:39 | +1789206999335 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 15:26:39 | +1789206999352 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=browser_modal |
| 15:26:41 | +1789207001686 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=strip&product=Redmi%20Note%208GB · mode=browser_modal |
| 15:26:42 | +1789207002528 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=834 · result=ok · candidate=Redmi Note 8GB |
| 15:26:42 | +1789207002528 | • step | ✓ step action: click:check |
| 15:26:42 | +1789207002528 | ⛓ hash | HASH seq=4 fbe6950daeee... (click:check) |
| 15:26:45 | +1789207005562 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 15:26:45 | +1789207005613 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 15:26:45 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 15:26:49 — **end**
