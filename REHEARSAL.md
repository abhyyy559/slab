# REHEARSAL.md — 5-minute arc + QA (backup: demo/demo-backup.mp4, 36s)

## Arc (commands verbatim)
| Time | Beat | Command / action |
|---|---|---|
| 0:00–0:20 | Hook: naive macro would die here | Show `?perturb=composite` chaos shot |
| 0:20–0:50 | Thesis + learn fact | "We ran webcmd learn once — adapters/ is what came out. Every replay deterministic." |
| 0:50–1:30 | v1 live | `python -m agent run --goal "Find the cheapest in-stock option on Site A that Site B confirms is deliverable within 3 days" --variant 1` → HASH lines + evidence table |
| 1:30–3:00 | **Judge presses console** (`harness/console/app.py` :8765) | detect → Recovery log → re-ground 0.2→0.8 → heal (~200ms, +2 steps) → verify |
| 3:00–3:40 | Handoff + approval modal | `--no-yes` run: teammate clicks Approve in browser |
| 3:40–4:10 | ABSTAIN beat | `--variant 6 --budget 8000 --ram 12` → refused naming `max_price AND min_ram`; medicine goal → `unsupported_goal` |
| 4:10–4:40 | Reflect beat | `propose-bump --mode good` → v2; `--mode bad` → REJECTED; `rollback --to 1` → green |
| 4:40–5:00 | Metrics | recovery cost 2, detect ~5ms, heal ~200ms, clock 42%, `reset`/`./demo.sh` |

## QA (one breath each)
1. "Just a macro recorder?" → Recorder breaks; ours re-grounds (5 signals + synonyms), logs Recovery, shows confidence — watch v4.
2. "Where's learning?" → webcmd adapters + version history (ACCEPTED + REJECTED + rollback in versions.jsonl).
3. "Citations real?" → URL + verbatim snippet + offset + sha; infeasible proves honest ABSTAIN.
4. "Safe?" → browser-modal approval before submits; no CAPTCHA/login/payments; own mocks + one read-only sandbox site.
5. "What breaks?" → FAILURES.md: timeout→snapshot fallback, rename→re-ground, unknown goal→ABSTAIN, open-domain→not supported.
6. "Detect 3ms?" → DOM mutation → next scan (polling cadence); reasoning lives in heal (~200ms).
7. "Why not 90% tokens?" → webcmd doesn't expose token counts; we measured wall-clock 42% and say so.
