# ONE-PAGER — SENTRY: the recovery layer, demoed on a cross-site workflow

## The healing loop (the product — read this first)
SENTRY is the recovery-and-proof layer any browser agent needs. Deterministic replay runs a versioned command store through Playwright; every element is re-grounded on 5 fused signals (selector, role+name, fuzzy text, visual presence, landmark) with a confidence number and a hard gate at tau=0.70. Below tau: PAUSE, log `LOW_CONFIDENCE_PAUSE`, re-ground once relaxed, else ABSTAIN naming the failed constraint. A detector compares each step's precondition against live page state and timestamps the mismatch; recovery climbs re-locate → re-plan → backtrack, then verifies the postcondition before proceeding — never acting irreversibly on unverified state. Every action extends a sha256 hash chain printed to stdout as appended; every claim is an extractive snippet (URL + verbatim text + char offset + sha). No generated citations. No bluffing.
**Learn → replay → heal → version-bump loop: DEMONSTRATED 2026-09-12.** `reflect.propose_bump` re-runs the 5-variant guard; bad lessons REJECT; good ones bump the version; `rollback` restores from `commands/.history/`. All in `logs/versions.jsonl` (1 ACCEPTED, multiple REJECTED, 2 ROLLED_BACK).

## The benchmark (the demo — the test bench, not the pitch)
We ran webcmd learn once; the adapters in `adapters/` are what came out, and every replay since has been deterministic. *"Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days, and hold it for approval."* Site B's answer determines Site A's choice (cheapest *deliverable*, not cheapest listed) — a loop, not a hop. Perturbed runs strip stable `data-testid`s; baseline uses them and we say so on stage. Mocks are the benchmark; one run on real public HTML we did not write (books.toscrape.com) is the credibility test.

## Metrics we own (own runs only)
Headline: **recovery cost** — extra steps + heal time per perturbation, averaged across the run. Wall-clock learn→replay: 6182→3587ms (~42%; tokens unexposed by webcmd, no 90% claim — their measurement, not ours). Plus: live 3/3, offline ≥9/10, detect <500ms, heal <3s, extra steps ≤2, citation precision 1.0, transfer pass-or-honest-ABSTAIN. No learning-curve claim until the loop exists.

## Limitations
See FAILURES.md. Headline: open-domain transfer not supported (command store is site-specific). Same-family only. No CAPTCHA/login/payments. 5+1 variants. Approval = visible browser modal before any submit.
