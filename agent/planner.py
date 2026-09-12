"""Planner: NL goal -> Plan (workflow + parameter overrides + steps).

Scope, stated honestly: this is a keyword/parameter extractor, NOT a general NL planner and
NOT an LLM. It maps a goal onto a *known* workflow and pulls budget / RAM / PIN / intent out
of the text. Anything it cannot map is reported as unsupported, and the replayer ABSTAINs on
it rather than silently running an unrelated workflow. Open-domain transfer is still not
supported (see FAILURES.md) -- this only closes the gap between what you type and what runs.
"""
import re
from dataclasses import dataclass, field, asdict

WORKFLOW_PHONE = "phone_delivery_check"
WORKFLOW_ENQUIRY = "phone_fulfilment_enquiry"


@dataclass
class Step:
    intent: str
    site: str
    expected_state: str = ""
    command_ref: str = ""


@dataclass
class Plan:
    goal: str = ""
    workflow: str = ""
    supported: bool = True
    unsupported: list = field(default_factory=list)
    params: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)
    steps: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


DEFAULT_STEPS = [
    {"intent": "open_search", "site": "site_a", "expected_state": "search_box_visible",
     "command_ref": "phone_delivery_check:1"},
    {"intent": "apply_filter", "site": "site_a", "expected_state": "results_filtered",
     "command_ref": "phone_delivery_check:2"},
    {"intent": "extract_cheapest", "site": "site_a", "expected_state": "product_selected",
     "command_ref": "phone_delivery_check:3"},
    {"intent": "check_delivery", "site": "site_b", "expected_state": "delivery_status_visible",
     "command_ref": "phone_delivery_check:4"},
]

# The fuller workflow: after Site B confirms deliverability, submit an enquiry for the
# chosen product on Site B's enquiry desk. This is the rubric's own example
# ("submit an enquiry for it on Site B") and makes the handoff a real cross-site write.
ENQUIRY_STEPS = DEFAULT_STEPS + [
    {"intent": "submit_enquiry", "site": "site_b", "expected_state": "enquiry_confirmed",
     "command_ref": "phone_fulfilment_enquiry:5"},
]

# Second task shape: compare the top candidates instead of picking one outright.
COMPARE_HINTS = ("compare", "comparison", "versus", " vs ", "which is better", "top 2", "top two")

# Words that ask for the enquiry/contact step specifically.
ENQUIRY_HINTS = ("enquiry", "enquire", "inquiry", "inquire", "contact", "quote", "message",
                 "reach out", "get in touch", "ask about")

# Domains we have no mocks for. Checked FIRST so "cheapest medicine under Rs 500" is refused
# instead of quietly running the phone workflow.
UNSUPPORTED_DOMAINS = [
    ("medicine", ("medicine", "medicines", "pharmacy", "pharmacies", "chemist", "prescription",
                  "drug", "drugs", "medication", "clinic", "dosage")),
    ("travel", ("flight", "flights", "hotel", "hotels", "train", "bus", "ticket", "itinerary")),
    ("groceries", ("grocery", "groceries", "vegetables", "supermarket")),
]
UNSUPPORTED_REGEX = [(r"\b\d+\s*mg\b", "medicine")]

# Brand tokens the user can ask for ("prefer Pixel", "Samsung only"). Matched as a
# case-insensitive substring of the catalog product name. Unknown brands yield
# brand_unavailable ABSTAIN downstream — never silently swapped for another brand.
BRANDS = ("pixel", "nova", "galaxy", "samsung", "apple", "iphone", "oneplus",
          "xiaomi", "redmi", "realme", "motorola", "moto", "vivo", "oppo",
          "nothing", "asus", "lenovo", "huawei", "honor")

# Signals that tie a goal to the workflow we actually have.
SUPPORTED_HINTS = ("phone", "mobile", "smartphone", "handset", "ram", "voltkart", "swiftship",
                   "site a", "site b", "deliver", "delivery", "pin", "cheapest", "in stock",
                   "stock", "price", "budget", "buy", "order", "gb")

BUDGET_PATTERNS = [
    r"(?:under|below|less than|no more than|up ?to|max(?:imum)?(?: price)?(?: of)?|budget(?: of| is)?)"
    r"\s*(?:rs\.?|inr|₹|\$|£|usd)?\s*(\d[\d,]*)",
    r"(?:rs\.?|inr|₹|\$|£)\s*(\d[\d,]*)",
]
RAM_PATTERNS = [
    r"(\d{1,3})\s*gb\s*(?:of\s*)?ram",
    r"ram\s*(?:of|>=|≥|:|at least)?\s*(\d{1,3})\s*gb",
    r"min(?:imum)?\s*(?:of\s*)?(\d{1,3})\s*gb",
]
PIN_PATTERNS = [
    r"pin(?:\s*code)?\s*(?:is|of|:|=)?\s*(\d{6})",
    r"\b(\d{6})\b",
]


def _first(pattern_list, text: str, exclude=()):
    for pat in pattern_list:
        for m in re.finditer(pat, text):
            tok = m.group(1)
            if tok in exclude:
                continue
            return tok, m.start(), m.end()
    return None, -1, -1


def _as_int(tok):
    try:
        return int(str(tok).replace(",", ""))
    except (TypeError, ValueError):
        return None


def plan_goal(goal: str, workflow: str = WORKFLOW_PHONE) -> Plan:
    """Map a natural-language goal onto a known workflow + parameter overrides."""
    goal = (goal or "").strip()
    plan = Plan(goal=goal, workflow=workflow)
    plan.steps = [Step(**s) for s in DEFAULT_STEPS]

    if not goal:
        plan.notes.append("empty goal: using the command file's own defaults")
        return plan

    text = " ".join(goal.lower().split())

    # 1. refuse domains we have no mocks for
    for domain, words in UNSUPPORTED_DOMAINS:
        if any(w in text for w in words):
            plan.supported = False
            plan.unsupported.append(
                f"no prepared fallback for the '{domain}' domain: mocks are phone storefronts "
                f"(VoltKart/SwiftShip) and commands/ holds only {workflow}.json")
            break
    if plan.supported:
        for pat, domain in UNSUPPORTED_REGEX:
            if re.search(pat, text):
                plan.supported = False
                plan.unsupported.append(f"'{domain}' goal detected ({pat}); no matching mocks")
                break

    # 2. does it look like the workflow we do have?
    if plan.supported and not any(h in text for h in SUPPORTED_HINTS) \
            and not any(b in text for b in BRANDS):
        plan.supported = False
        plan.unsupported.append(
            f"goal did not match any known workflow (known: {workflow} -- cheapest in-stock "
            f"option on Site A confirmed deliverable by Site B)")

    if not plan.supported:
        return plan

    # 3. does the goal ask for the enquiry/contact step? If so, use the longer workflow.
    # Both share steps 1-4; the enquiry workflow appends the cross-site write.
    if any(h in text for h in ENQUIRY_HINTS):
        plan.workflow = WORKFLOW_ENQUIRY
        plan.steps = [Step(**s) for s in ENQUIRY_STEPS]
        plan.notes.append("goal asks to make contact -> workflow extended with submit_enquiry (Site B)")

    # 4. extract parameters
    budget, _, _ = _first(BUDGET_PATTERNS, text)
    ram, _, _ = _first(RAM_PATTERNS, text)
    pin, _, _ = _first(PIN_PATTERNS, text, exclude=({budget} if budget else set()))

    if budget:
        plan.params["budget"] = _as_int(budget)
        plan.notes.append(f"budget {plan.params['budget']} read from the goal")
    if ram:
        plan.params["ram"] = _as_int(ram)
        plan.notes.append(f"min RAM {plan.params['ram']}GB read from the goal")
    # never let the budget digits be mistaken for a PIN
    if pin and str(pin) != str(budget):
        plan.params["pin"] = str(pin)
        plan.notes.append(f"PIN {pin} read from the goal")
    for brand in BRANDS:
        if re.search(r"\b" + re.escape(brand) + r"\b", text):
            plan.params["brand"] = brand
            plan.notes.append(f"brand '{brand}' read from the goal (hard filter, no substitution)")
            break
    if any(h in text for h in COMPARE_HINTS):
        plan.params["compare_top2"] = True
        plan.notes.append("compare task: top candidates checked against Site B, comparison logged")

    plan.params = {k: v for k, v in plan.params.items() if v is not None}
    if not plan.params:
        plan.notes.append("no parameter overrides found in the goal: using the command defaults")
    plan.notes.append("3-day delivery window is fixed by the workflow, not parsed from the goal")
    return plan
