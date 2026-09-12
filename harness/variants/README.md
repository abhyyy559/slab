# Variants (cap 5+1). v1 practiced baseline; v4 perturbed; v5 transfer; v6 infeasible ABSTAIN.
- 1: mocks site_a/search + site_b/check, budget 20000 ram 8 pin 500001 (baseline, no perturb)
- 2: same, budget 25000 (practiced param shift)
- 3: same, pin 500002 (practiced param shift)
- 4: composite perturb (seed 42: shuffle+rename+modal+extra_step+throttle+strip_testids), deterministic via `?perturb=composite`; judge-operated live via console (mock pages poll :8765/status). Gate: pass with <=2 extra steps + Recovery entry per perturbation.
- 5: transfer same-family (books.toscrape.com credibility run)
- +1: infeasible (budget 8000 + 12GB RAM) -> ABSTAIN naming max_price AND min_ram.
  Run: `python -m agent run --goal "..." --variant 6 --budget 8000 --ram 12 --base http://127.0.0.1:8000` (exit 2, ABSTAIN banner).
