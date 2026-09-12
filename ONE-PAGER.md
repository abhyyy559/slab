# ONE-PAGER — SENTRY: the recovery layer, demoed on a cross-site workflow

## The healing loop (the product — read this first)
SENTRY is the recovery-and-proof layer any browser agent needs. Deterministic replay runs a versioned command store through Playwright; every element is re-grounded on 5 fused signals (selector, role+name, fuzzy text, visual presence, landmark) with a confidence number and a hard gate at tau=0.70. Below tau: PAUSE, log `LOW_CONFIDENCE_PAUSE`, re-ground once relaxed, else ABSTAIN naming the failed constraint. A detector compares each step's precondition against live page state and timestamps the mismatch; recovery climbs re-locate → re-plan → backtrack, then verifies the postcondition before proceeding — never acting irreversibly on unverified state. Every action extends a sha256 hash chain printed to stdout as appended; every claim is an extractive snippet (URL + verbatim text + char offset + sha). No generated citations. No bluffing.
**CUT from pitch until demonstrated:** the learn → replay → heal → version-bump loop (no logs exist yet). `agent/learner.py` and `agent/reflect.py` are stubs. We do not say "learning" on stage until 3+ logged trials show it.

## The benchmark (the demo — the test bench, not the pitch)
*"Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days, and hold it for approval."* Site B's answer determines Site A's choice (cheapest *deliverable*, not cheapest listed) — a loop, not a hop. Perturbed runs strip stable `data-testid`s; baseline uses them and we say so on stage. Mocks are the benchmark; one run on real public HTML we did not write (books.toscrape.com) is the credibility test.

## Metrics we own (own runs only)
Headline: **recovery cost** — extra steps + heal time per perturbation, averaged across the run. Plus: live 3/3, offline ≥9/10, detect <500ms, heal <3s, extra steps ≤2, citation precision 1.0, transfer pass-or-honest-ABSTAIN. No learning-curve claim until the loop exists.

## Limitations
See FAILURES.md. Headline: open-domain transfer not supported (command store is site-specific). Same-family only. No CAPTCHA/login/payments. 5+1 variants. Approval = visible browser modal before any submit.
