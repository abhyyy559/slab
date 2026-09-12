# SENTRY run — v3/clean

- **started:** 2026-09-12 19:23:27
- **goal:** (none)

| t | ts | event | detail |
|---|---|---|---|
| 19:23:28 | +1789221208688 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=163 · result=ok · url=http://127.0.0.1:8000/site_a/search.html |
| 19:23:28 | +1789221208688 | • step | ✓ step action: goto:search |
| 19:23:28 | +1789221208696 | ⛓ hash | HASH seq=1 7d2e46e86368... (goto:search) |
| 19:23:29 | +1789221209096 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:23:29 | +1789221209207 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:23:29 | +1789221209273 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=62 · result=ok |
| 19:23:29 | +1789221209273 | • step | ✓ step action: click:filter |
| 19:23:29 | +1789221209273 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 19:23:29 | +1789221209298 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:23:29 | +1789221209312 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:23:29 | +1789221209386 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=70 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:23:29 | +1789221209390 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:23:29 | +1789221209392 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 19:23:29 | +1789221209784 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:23:29 | +1789221209784 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · payload={'pin': '500002'} · mode=cli |
| 19:23:29 | +1789221209792 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?product=Redmi%20Note%208GB · mode=cli |
| 19:23:29 | +1789221209843 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=51 · result=ok · candidate=Redmi Note 8GB |
| 19:23:29 | +1789221209849 | • step | ✓ step action: click:check |
| 19:23:29 | +1789221209849 | ⛓ hash | HASH seq=4 ed17c9c25b5a... (click:check) |
| 19:23:30 | +1789221210271 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=False |
| 19:23:30 | +1789221210271 | · LOOP_FALLBACK | reason=Redmi Note 8GB not deliverable · next=next-cheapest eligible |
| 19:23:30 | +1789221210317 | · goto | seq=5 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=42 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Nova%20Mini%208GB · candidate=Nova Mini 8GB · attempt=2 |
| 19:23:30 | +1789221210322 | • step | ✓ step action: goto:delivery:Nova Mini 8GB |
| 19:23:30 | +1789221210322 | ⛓ hash | HASH seq=5 217cda3bde74... (goto:delivery:Nova Mini 8GB) |
| 19:23:30 | +1789221210771 | · ground | seq=5 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:23:30 | +1789221210843 | · click | seq=6 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=63 · result=ok · candidate=Nova Mini 8GB |
| 19:23:30 | +1789221210843 | • step | ✓ step action: click:check |
| 19:23:30 | +1789221210853 | ⛓ hash | HASH seq=6 ed17c9c25b5a... (click:check) |
| 19:23:31 | +1789221211283 | · delivery_verdict | seq=6 · step=4 · target=Nova Mini 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=False |
| 19:23:31 | +1789221211283 | · LOOP_FALLBACK | reason=Nova Mini 8GB not deliverable · next=next-cheapest eligible |
| 19:23:31 | +1789221211365 | · goto | seq=7 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=78 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?product=Oppo%20A%208GB · candidate=Oppo A 8GB · attempt=3 |
| 19:23:31 | +1789221211367 | • step | ✓ step action: goto:delivery:Oppo A 8GB |
| 19:23:31 | +1789221211367 | ⛓ hash | HASH seq=7 217cda3bde74... (goto:delivery:Oppo A 8GB) |
| 19:23:31 | +1789221211877 | · ground | seq=7 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:23:31 | +1789221211985 | · click | seq=8 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=107 · result=ok · candidate=Oppo A 8GB |
| 19:23:31 | +1789221211993 | • step | ✓ step action: click:check |
| 19:23:31 | +1789221211995 | ⛓ hash | HASH seq=8 ed17c9c25b5a... (click:check) |
| 19:23:32 | +1789221212430 | · delivery_verdict | seq=8 · step=4 · target=Oppo A 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=False |
| 19:23:32 | +1789221212430 | · LOOP_FALLBACK | reason=Oppo A 8GB not deliverable · next=next-cheapest eligible |
| 19:23:32 | +1789221212440 | · ABSTAIN | reason=no_deliverable_candidate · constraint=b_confirms_deliverable_3d · attempts=[{'candidate': 'Redmi Note 8GB', 'price': 12999, 'deliverable': False, 'observed': 'Delivery not available to PIN 500002'}, {'candidate': 'N |

**finished:** 2026-09-12 19:23:32 — **end**
