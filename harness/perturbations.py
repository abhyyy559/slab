"""Perturbation implementations (Phase 2 wires to live DOM; v1 documents intent)."""
PERTURBATIONS = {
    "shuffle": "CSS reorder of DOM siblings without changing semantics.",
    "rename": "Swap button/label text with synonyms (Apply Filter -> Refine Results).",
    "modal": "Inject cookie/offer modal that must be dismissed.",
    "extra_step": "Insert intermediate confirmation page.",
    "throttle": "Delay responses 2-4s.",
    "composite": "All of the above, seeded.",
}
