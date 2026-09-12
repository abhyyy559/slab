# ONE-PAGER — SENTRY

## Problem
Brittle web macros break on trivial UI change; judges/clients don't trust agent claims without citations.

## Approach
Learn once (webcmd or hand-authored JSON) -> replay with 5-signal grounding + confidence gate -> detect mismatch -> recover (re-locate/re-plan/backtrack + verify) -> extractive evidence + constraint check + approval gate -> reflect (version bump guarded by regression + rollback).

## Metrics (own runs only)
Live 3/3, offline >=9/10, detect <500ms, heal <3s, extra steps <=2, citation precision 1.0, transfer pass-or-abstain, token/time saved >=60%.

## Limitations
Same-family transfer only. No CAPTCHA/login/payments. 5+1 variants. Static mocks first, real sites only if ToS allows.
