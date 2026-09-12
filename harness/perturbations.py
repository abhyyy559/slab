"""Perturbation catalogue for the adaptive-browsing bench.

Each entry documents a class of change a real site makes without warning, and the
signal the agent is expected to fall back on. The actual DOM behaviour lives in
mocks/chaos.js; this file is the single source of truth for *what exists* and is
imported by the console (to build the injector UI) and by the tests (to iterate
the whole matrix). Keep it in sync with chaos.js `setOf()`.
"""

# Ordered so the console shows least -> most destructive.
PERTURBATIONS = {
    "rename": "Accessible names swapped for synonyms (Apply Filter -> Refine Results). "
              "Agent must match the control by role/synonym, not by exact label.",
    "strip": "data-testid removed from buttons/inputs. Agent must fall back to "
             "role + accessible name + label association.",
    "move": "Controls relocated / reordered inside their container. "
            "Agent must not rely on document order or absolute position.",
    "attrs": "data-* attributes and classes mutated. "
             "Agent must not rely on attribute selectors.",
    "modal": "Blocking offer modal injected. Agent must detect + dismiss before acting.",
    "extra_step": "Inserted confirmation interstitial. Agent must clear it and verify.",
    "throttle": "Response latency injected (2-2.5s). Agent must wait for the postcondition, "
                "not assume instant results.",
    "ab": "Every other result card hidden (A/B variant). Agent must pick from the visible set.",
    "swap": "Results list re-rendered into a new container (SPA-style). "
            "Agent must re-discover the list, not hold a stale reference.",
    "rename_strip": "Composite of rename + strip (labels and ids both gone).",
    "composite": "rename + strip + move + attrs + modal + extra_step + throttle.",
    "chaos_max": "Everything including ab + swap. Worst case.",
    "reset": "Clear all injected changes.",
}

# Everything that can be applied deterministically (?perturb=<name>) or live.
CHAOS_TYPES = [k for k in PERTURBATIONS if k != "reset"]

# Matches the console composite definition (STATE["composite"]).
COMPOSITE_SUBTYPES = ["rename", "strip", "move", "attrs", "modal", "extra_step", "throttle"]

# Perturbations that should NOT change the correct final answer.
ANSWER_PRESERVING = ["rename", "strip", "move", "attrs", "modal", "extra_step",
                     "throttle", "rename_strip", "composite"]

# Perturbations that legitimately hide candidates -> the agent may still pass by
# choosing from the visible subset, or ABSTAIN honestly.
ANSWER_ADAPTING = ["ab", "swap", "chaos_max"]
