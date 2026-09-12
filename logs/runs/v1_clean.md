# SENTRY run — v1/clean

- **started:** 2026-09-12 16:01:04
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:06 | +1789209066037 | · BROWSER_WINDOW | mode=headed · raised=True · slow_mo=800 · keep_open_ms=4000 · stage={'screen_w': 1536, 'screen_h': 960} |
| 16:01:07 | +1789209067205 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=1166 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 16:01:07 | +1789209067206 | • step | ✓ step action: goto:search |
| 16:01:07 | +1789209067214 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 16:01:07 | +1789209067626 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:01:09 | +1789209069371 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:10 | +1789209070279 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=878 · result=ok |
| 16:01:10 | +1789209070279 | • step | ✓ step action: click:filter |
| 16:01:10 | +1789209070279 | ⛓ hash | HASH seq=2 65409d2577ee... (click:filter) |
| 16:01:10 | +1789209070298 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:10 | +1789209070309 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:11 | +1789209071178 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=869 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:11 | +1789209071180 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:11 | +1789209071180 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 16:01:12 | +1789209072338 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:12 | +1789209072373 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=browser_modal |
| 16:01:14 | +1789209074419 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=browser_modal |
| 16:01:15 | +1789209075269 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=847 · result=ok · candidate=Redmi Note 8GB |
| 16:01:15 | +1789209075270 | • step | ✓ step action: click:check |
| 16:01:15 | +1789209075270 | ⛓ hash | HASH seq=4 5886560144fb... (click:check) |
| 16:01:15 | +1789209075698 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:01:15 | +1789209075715 | 📊 metric | METRIC detect=0ms heal=0ms extra=0 status=pass |

**finished:** 2026-09-12 16:01:15 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 0 · recoveries 0

**finished:** 2026-09-12 16:01:19 — **end**
