# SENTRY run — v1/composite

- **started:** 2026-09-12 16:28:19
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:28:19 | +1789210699250 | · PERTURB_INJECTED | target=composite · seq=0 |
| 16:28:20 | +1789210700767 | · BROWSER_WINDOW | mode=headed · raised=True · slow_mo=998 · keep_open_ms=4000 · stage={'screen_w': 1536, 'screen_h': 960} |
| 16:28:21 | +1789210701905 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=1136 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=composite |
| 16:28:21 | +1789210701918 | • step | ✓ step action: goto:search |
| 16:28:21 | +1789210701937 | ⛓ hash | HASH seq=1 6f565c69f0c3... (goto:search) |
| 16:28:24 | +1789210704205 | · RECOVERY · event | trigger=modal+extra_step+label_renamed+label_renamed+structure_moved · expected=clean_page · observed=chaos-modal visible+chaos-confirm visible+Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789210702590 · time_to_detect_ms=182 · strategy=re_plan · steps=['dismissed:#chaos-confirm'] · time_to_heal_ms=1420 · verified=False |
| 16:28:24 | +1789210704207 | ⚠ recovery | ⚠ RECOVERY: modal+extra_step+label_renamed+label_renamed+structure_moved -> re_plan |
| 16:28:24 | +1789210704209 | ✓ healed | ✓ HEALED in 1420ms (verified=False) |
| 16:28:24 | +1789210704280 | · ground | seq=1 · step=1 · target=search_box · confidence=0.84 · signals=['role_name', 'visual'] · duration_ms=0 · result=ok |
| 16:28:26 | +1789210706560 | · RECOVERY · event | trigger=label_renamed+label_renamed+structure_moved · expected=clean_page · observed=Refine Results+Look Up+element relocated in DOM · detected_at_ms=1789210706483 · time_to_detect_ms=53 · strategy=re_locate · time_to_heal_ms=17 · verified=False |
| 16:28:26 | +1789210706561 | ⚠ recovery | ⚠ RECOVERY: label_renamed+label_renamed+structure_moved -> re_locate |
| 16:28:26 | +1789210706561 | ✓ healed | ✓ HEALED in 17ms (verified=False) |
| 16:28:26 | +1789210706620 | · ground | seq=1 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:28:27 | +1789210707720 | · click | seq=2 · step=2 · target=filter_button · confidence=0.848 · signals=['role_name', 'text', 'visual'] · duration_ms=1068 · result=ok |
| 16:28:27 | +1789210707736 | • step | ✓ step action: click:filter |
| 16:28:27 | +1789210707738 | ⛓ hash | HASH seq=2 d9d1c9afcade... (click:filter) |
| 16:28:27 | +1789210707760 | · STOCK_FILTER | excluded=3 · detail=out of stock, not eligible: ['Pixel Fold 12GB', 'Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:28:27 | +1789210707776 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:28:28 | +1789210708852 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=1075 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:28:28 | +1789210708852 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:28:28 | +1789210708867 | ⛓ hash | HASH seq=3 988a29cfa1ed... (goto:delivery:Redmi Note 8GB) |
| 16:28:30 | +1789210710352 | · RECOVERY · event | trigger=label_renamed+structure_moved · expected=clean_page · observed=Verify Shipment+element relocated in DOM · detected_at_ms=1789210710288 · time_to_detect_ms=43 · strategy=re_locate · time_to_heal_ms=21 · verified=False |
| 16:28:30 | +1789210710352 | ⚠ recovery | ⚠ RECOVERY: label_renamed+structure_moved -> re_locate |
| 16:28:30 | +1789210710352 | ✓ healed | ✓ HEALED in 21ms (verified=False) |
| 16:28:30 | +1789210710403 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:28:30 | +1789210710444 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=browser_modal |
| 16:28:35 | +1789210715132 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=composite&product=Redmi%20Note%208GB · mode=browser_modal |
| 16:28:36 | +1789210716215 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'text', 'visual'] · duration_ms=1083 · result=ok · candidate=Redmi Note 8GB |
| 16:28:36 | +1789210716215 | • step | ✓ step action: click:check |
| 16:28:36 | +1789210716232 | ⛓ hash | HASH seq=4 be4b224d5cfe... (click:check) |
| 16:28:39 | +1789210719259 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:28:39 | +1789210719290 | 📊 metric | METRIC detect=92ms heal=486ms extra=1 status=pass |

**finished:** 2026-09-12 16:28:39 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 1 · recoveries 3

**finished:** 2026-09-12 16:28:43 — **end**
