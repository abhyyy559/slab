# SENTRY — jury brief (read in 4 minutes, demo in 5)

## One line
A browser agent that completes a cross-site shopping goal and heals itself live when the page changes — with cited proof for every claim and honest refusals when it can't.

## The 20-second pitch
"Every run before this one burned effort rediscovering the same site. We ran webcmd learn once. Every replay since has been deterministic — and when a judge breaks the page mid-run, the agent detects it in milliseconds, heals, and finishes with evidence."

## Live demo (5 min)
1. **Clean run** — dashboard → Run agent → headed Chromium window opens, fills budget/RAM, picks cheapest, jumps sites, **you click Approve** in the modal, evidence table fills. (~8s)
2. **Chaos** — press **Composite chaos** (or any of shuffle/rename/modal/extra step/throttle), run again → trace shows RECOVERY → re-ground → HEALED (+2 steps, ~190ms).
3. **One-click proof** — **Run chaos matrix**: clean + all 6 perturbs, 7/7 expected in ~60s.
4. **Refusal** — Infeasible preset (Rs 8,000 + 12 GB) → ABSTAIN naming the failed constraint.
5. **Learning** — propose bump (good) → version+1; propose bump (bad) → REJECTED; rollback → green. All in `logs/versions.jsonl`.

## Numbers (from logs, not slides)
- 93/93 trials met expectation · jitter 5/5 identical · 62-test suite green
- detect ~3ms steady-state (526ms all-time avg incl. early untuned runs — both published)
- heal ~190–290ms · recovery cost +2 steps on composite · citation integrity 1.0
- wall-clock learn→replay 6182→3587ms (~42%; webcmd exposes no token counts, so no token claims)

## Architecture (30 seconds)
Goal → planner (keyword router, refuses unknown domains) → webcmd adapters (learned once) → Playwright replay → 5-signal grounding (τ=0.70) → detector → recovery ladder (dismiss → re-ground → backtrack → verify) → extractive evidence → constraint check → approval modal → JSONL logs → reflect (guard → accept/reject/rollback).

## The 4 verification catches (say this — nobody else has it)
1. Chaos script crashed silently; agent reported a perfect pass. Caught by evidence offsets.
2. "Available" matched inside "not available". Now a 9-case test file.
3. Evidence snippet was a thumbnail emoji. Now SVG + product name.
4. Teammate edits swept in by `git add -A`. Now mock-contract tests + battery rule.

## 5 answers to have ready
1. "Just a macro recorder?" → Recorders break; ours re-grounds with confidence numbers. Watch v4.
2. "Where's the learning?" → Open `logs/versions.jsonl`: accept, reject, rollback.
3. "Citations real?" → Click one in `evidence.html`: URL + offset + sha.
4. "Detect 3ms?" → Mutation→next scan (polling cadence); reasoning lives in heal (~200ms).
5. "Amazon?" → Out of scope: bot walls and ToS. Our probe refuses at the wall; practice sandboxes pass.

## Honest limits (in FAILURES.md, say them first)
One workflow only · open-domain transfer unsupported · approval demo fires on a read-only check · token counts unmeasurable · venue rehearsal is the highest risk.
