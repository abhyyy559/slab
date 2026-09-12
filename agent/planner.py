"""Planner: NL goal -> Plan (steps with intent, site, expected_state, command_ref). LLM for decomposition only."""
from dataclasses import dataclass, field

@dataclass
class Step:
    intent: str
    site: str
    expected_state: str = ""
    command_ref: str = ""

@dataclass
class Plan:
    goal: str
    steps: list = field(default_factory=list)

DEFAULT_PLAN = [
    {"intent": "open_search", "site": "site_a", "expected_state": "search_box_visible", "command_ref": "phone_delivery_check:1"},
    {"intent": "apply_filter", "site": "site_a", "expected_state": "results_visible", "command_ref": "phone_delivery_check:2"},
    {"intent": "extract_cheapest", "site": "site_a", "expected_state": "product_selected", "command_ref": "phone_delivery_check:3"},
    {"intent": "check_delivery", "site": "site_b", "expected_state": "delivery_status_visible", "command_ref": "phone_delivery_check:4"},
]

def plan_goal(goal: str, workflow: str = "phone_delivery_check") -> Plan:
    steps = [Step(**s) for s in DEFAULT_PLAN]
    return Plan(goal=goal, steps=steps)
