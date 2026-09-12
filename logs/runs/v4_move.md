# SENTRY run — v4/move

- **started:** 2026-09-12 19:42:01
- **goal:** Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days and submit an enquiry for it on Site B

| t | ts | event | detail |
|---|---|---|---|
| 19:42:01 | +1789222321285 | · PERTURB_INJECTED | target=move · seq=0 |
| 19:42:02 | +1789222322806 | · goto | seq=1 · step=1 · target=search_page · confidence=1.0 · signals=['selector'] · duration_ms=275 · result=ok · url=http://127.0.0.1:8000/site_a/search.html?perturb=move |
| 19:42:02 | +1789222322814 | • step | ✓ step action: goto:search |
| 19:42:02 | +1789222322825 | ⛓ hash | HASH seq=1 b0f62bd5ec8d... (goto:search) |
| 19:42:03 | +1789222323371 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789222323322 · time_to_detect_ms=8 · strategy=re_locate · time_to_heal_ms=27 · verified=False |
| 19:42:03 | +1789222323377 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 19:42:03 | +1789222323381 | ✓ healed | ✓ HEALED in 27ms (verified=False) |
| 19:42:03 | +1789222323512 | · ground | seq=1 · step=1 · target=search_box · confidence=0.9 · signals=['selector', 'visual'] · duration_ms=0 · result=ok |
| 19:42:03 | +1789222323571 | · fill | seq=1 · step=2 · target=max_price · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:20000 |
| 19:42:03 | +1789222323606 | · fill | seq=1 · step=2 · target=min_ram · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:8GB |
| 19:42:03 | +1789222323793 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789222323740 · time_to_detect_ms=8 · strategy=re_locate · time_to_heal_ms=41 · verified=False |
| 19:42:03 | +1789222323799 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 19:42:03 | +1789222323806 | ✓ healed | ✓ HEALED in 41ms (verified=False) |
| 19:42:03 | +1789222323889 | · ground | seq=1 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:03 | +1789222323984 | · click | seq=2 · step=2 · target=filter_button · confidence=1.0 · signals=['role_name', 'selector', 'text', 'visual'] · duration_ms=88 · result=ok |
| 19:42:03 | +1789222323998 | • step | ✓ step action: click:filter |
| 19:42:04 | +1789222324011 | ⛓ hash | HASH seq=2 598c25f75653... (click:filter) |
| 19:42:04 | +1789222324040 | · STOCK_FILTER | excluded=2 · detail=out of stock, not eligible: ['Galaxy S Lite 8GB', 'Lava Blaze 8GB'] |
| 19:42:04 | +1789222324057 | · extract | seq=2 · step=3 · target=cheapest · confidence=0.95 · signals=['selector', 'text'] · duration_ms=0 · result=ok:Redmi Note 8GB:12999 |
| 19:42:04 | +1789222324060 | · rank | seq=2 · step=3 · target=candidates · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB@12999,Nova Mini 8GB@15499,Oppo A 8GB@16499 |
| 19:42:04 | +1789222324162 | · goto | seq=3 · step=4 · target=delivery_page · confidence=1.0 · signals=['selector'] · duration_ms=93 · result=ok · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB · attempt=1 |
| 19:42:04 | +1789222324168 | • step | ✓ step action: goto:delivery:Redmi Note 8GB |
| 19:42:04 | +1789222324172 | ⛓ hash | HASH seq=3 246060fc45d4... (goto:delivery:Redmi Note 8GB) |
| 19:42:04 | +1789222324550 | · fill | seq=3 · step=4 · target=pin_input · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:500001 |
| 19:42:04 | +1789222324787 | · RECOVERY · event | trigger=structure_moved · expected=clean_page · observed=element relocated in DOM · detected_at_ms=1789222324744 · time_to_detect_ms=11 · strategy=re_locate · time_to_heal_ms=29 · verified=False |
| 19:42:04 | +1789222324800 | ⚠ recovery | ⚠ RECOVERY: structure_moved -> re_locate |
| 19:42:04 | +1789222324808 | ✓ healed | ✓ HEALED in 29ms (verified=False) |
| 19:42:04 | +1789222324926 | · ground | seq=3 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:04 | +1789222324935 | · APPROVAL_REQUESTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · payload={'pin': '500001'} · mode=cli |
| 19:42:04 | +1789222324941 | · APPROVAL_GRANTED | target=check_delivery_submit · url=http://127.0.0.1:8000/site_b/check.html?perturb=move&product=Redmi%20Note%208GB · mode=cli |
| 19:42:05 | +1789222325069 | · click | seq=4 · step=4 · target=check_button · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=116 · result=ok · candidate=Redmi Note 8GB |
| 19:42:05 | +1789222325075 | • step | ✓ step action: click:check |
| 19:42:05 | +1789222325085 | ⛓ hash | HASH seq=4 2f8e6266ceb0... (click:check) |
| 19:42:08 | +1789222328184 | · delivery_verdict | seq=4 · step=4 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=deliverable=True |
| 19:42:08 | +1789222328217 | · verify | seq=4 · step=4 · target=delivery_verdict · confidence=1.0 · signals=['trace'] · duration_ms=0 · result=ok:Redmi Note 8GB-deliverable |
| 19:42:08 | +1789222328395 | · goto | seq=5 · step=5 · target=enquiry_page · confidence=1.0 · signals=['selector'] · duration_ms=166 · result=ok · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=move&product=Redmi%20Note%208GB · candidate=Redmi Note 8GB |
| 19:42:08 | +1789222328401 | • step | ✓ step action: goto:enquiry:Redmi Note 8GB |
| 19:42:08 | +1789222328408 | ⛓ hash | HASH seq=5 dccfb6e26d60... (goto:enquiry:Redmi Note 8GB) |
| 19:42:09 | +1789222329403 | · ground | seq=5 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=0 · result=ok |
| 19:42:09 | +1789222329409 | · APPROVAL_REQUESTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=move&product=Redmi%20Note%208GB · payload={'product': 'Redmi Note 8GB', 'pin': '500001'} · mode=cli |
| 19:42:09 | +1789222329417 | · APPROVAL_GRANTED | target=submit_enquiry · url=http://127.0.0.1:8000/site_b/enquiry.html?perturb=move&product=Redmi%20Note%208GB · mode=cli |
| 19:42:09 | +1789222329636 | · click | seq=6 · step=5 · target=enquiry_submit · confidence=1.0 · signals=['landmark', 'role_name', 'selector', 'text', 'visual'] · duration_ms=202 · result=ok |
| 19:42:09 | +1789222329649 | • step | ✓ step action: click:enquiry:submit |
| 19:42:09 | +1789222329653 | ⛓ hash | HASH seq=6 39c33fda756c... (click:enquiry:submit) |
| 19:42:09 | +1789222329700 | · enquiry_verdict | seq=6 · step=5 · target=Redmi Note 8GB · confidence=1.0 · signals=['text'] · duration_ms=0 · result=confirmed=True |
| 19:42:09 | +1789222329806 | 📊 metric | METRIC detect=9ms heal=32ms extra=0 status=pass |

**finished:** 2026-09-12 19:42:09 — **pass**

Chosen: Redmi Note 8GB @ Rs 12999 · delivery: Delivery available to PIN 500001 in 2-3 days · enquiry: Enquiry received for Redmi Note 8GB. Reference SS-485092. We will reply to agent+pin500001@example.com within 1 business · extra steps 0 · recoveries 3

**finished:** 2026-09-12 19:42:09 — **end**
