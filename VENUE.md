# VENUE.md — first-15-minutes checklist (fill on site, then demo)

- [ ] Rubric: Luma 30/25/20/15/10 or brief 60/40? → record answer:
- [ ] Sandbox provided or own mocks only? → record answer:
- [ ] Team size rule (1–4 or 2–4)? → record answer:
- [ ] Network/keys: venue Wi-Fi reliable? LLM keys needed? (we need none — keyless-first) →
- [ ] Live perturbation injection by judges allowed? (our whole demo) → record answer:
- [ ] What counts as "irreversible"? (default: enquiry/delivery-check submit → approval modal) → record answer:

After filling: `./demo.sh` (Git Bash) or the two python commands in TASKS.md, then
`python -m agent run --goal "Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days" --variant 1`.
If any answer invalidates the plan, log it in DECISIONS.md before changing code.
