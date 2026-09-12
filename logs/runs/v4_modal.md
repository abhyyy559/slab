# SENTRY run — v4/modal

- **started:** 2026-09-12 16:01:41
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days

| t | ts | event | detail |
|---|---|---|---|
| 16:01:41 | +1789209101361 | · PERTURB_INJECTED | target=modal · seq=0 |
| 16:01:41 | +1789209101898 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=96 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=modal |
| 16:01:41 | +1789209101899 | • step | ✓ step action: goto:search |
| 16:01:41 | +1789209101900 | ⛓ hash | HASH seq=1 a723c4ad2b51... (goto:search) |
| 16:01:42 | +1789209102583 | · RECOVERY · event | trigger=modal · expected=clean_page · observed=chaos-modal visible · detected_at_ms=1789209102231 · time_to_detect_ms=6 · strategy=re_plan · steps=['dismissed:#chaos-modal'] · time_to_heal_ms=343 · verified=False |
| 16:01:42 | +1789209102585 | ⚠ recovery | ⚠ RECOVERY: modal -> re_plan |
| 16:01:42 | +1789209102587 | ✓ healed | ✓ HEALED in 343ms (verified=False) |
| 16:01:42 | +1789209102628 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 16:01:42 | +1789209102667 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:42 | +1789209102701 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=30 · result=ok |
| 16:01:42 | +1789209102701 | • step | ✓ step action: click:filter |
| 16:01:42 | +1789209102702 | ⛓ hash | HASH seq=2 8c5e8b087237... (click:filter) |
| 16:01:42 | +1789209102714 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 16:01:42 | +1789209102724 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 16:01:42 | +1789209102756 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=30 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 16:01:42 | +1789209102758 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 16:01:42 | +1789209102759 | ⛓ hash | HASH seq=3 217cda3bde74... (goto:delivery:Redmi Note 8GB) |
| 16:01:43 | +1789209103085 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 16:01:43 | +1789209103086 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 16:01:43 | +1789209103086 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=modal&product=Redmi%20Note%208GB · mode=cli |
| 16:01:43 | +1789209103110 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=23 · result=ok · candidate=Redmi Note 8GB |
| 16:01:43 | +1789209103111 | • step | ✓ step action: click:check |
| 16:01:43 | +1789209103111 | ⛓ hash | HASH seq=4 9a4af1d23de2... (click:check) |
| 16:01:46 | +1789209106123 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 16:01:46 | +1789209106147 | 📊 metric | METRIC detect=6ms heal=343ms extra=1 status=pass |

**finished:** 2026-09-12 16:01:46 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · extra steps 1 · recoveries 1

**finished:** 2026-09-12 16:01:46 — **end**
