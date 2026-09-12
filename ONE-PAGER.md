# ONE-PAGER — SENTRY: recovery engine, benchmarked on medicine-finder

## Problem
Every team demos a shopper. Shoppers are brittle: one renamed button kills the macro, and nobody trusts agent claims without citations. The scored thing in Track 01 is not shopping — it is **surviving live UI chaos with proof**.

## What SENTRY is
**A recovery layer any browser agent needs — benchmarked against the hardest test we could construct: a cross-site workflow under live, judge-operated UI chaos.** Benchmark: *"Aarav's grandmother needs medicine X. Find the cheapest in-stock option (Site A pharmacy), confirm it is available at the nearest clinic branch (Site B), reserve pickup — with human approval."* The shopping is the test bench. The recovery engine is the product.

## Approach
Learn once (webcmd or hand-authored JSON) -> replay with 5-signal grounding + confidence gate (tau=0.70) -> detect mismatch -> recover (re-locate/re-plan/backtrack + verify) -> extractive evidence + constraint check + browser-modal approval gate -> reflect (regression-guarded version bump + rollback). Cross-site handoff is a **loop**: Site B availability feeds back into the Site A choice (cheapest *deliverable*, not cheapest listed). Perturbed runs **strip stable `data-testid`s** — baseline uses them, chaos run does not.

## Metrics we own (own runs only, no bluffing)
Headline: **recovery cost** — extra steps + heal time per perturbation, averaged across the run. Plus: live 3/3, offline >=9/10, detect <500ms, heal <3s, extra steps <=2, citation precision 1.0, transfer pass-or-honest-ABSTAIN. Learning curve: >=3 trials logged before any "learning" claim. Credibility test: one run against real public HTML we did not write (books.toscrape.com) alongside mocks.

## Limitations
Same-family transfer only. No CAPTCHA/login/payments. 5+1 variants. Static mocks first, real sites only if ToS allows.
