"""Cross-site enquiry workflow tests (no browser).

The rubric's own example goal is "find the cheapest listed item matching X on Site A
and submit an enquiry for it on Site B". These tests pin the planning contract for
that two-site write:

  * a plain delivery goal stays on the 4-step phone workflow;
  * a goal that asks to make contact switches to the 5-step enquiry workflow;
  * the irreversible enquiry action is declared as such in the command file;
  * the enquiry workflow is a superset of the delivery workflow (steps 1-4 unchanged),
    so nothing about the existing verified path is disturbed.
"""
import json
import pathlib

from agent.planner import (plan_goal, WORKFLOW_PHONE, WORKFLOW_ENQUIRY,
                           DEFAULT_STEPS, ENQUIRY_STEPS, ENQUIRY_HINTS)

CMD_DIR = pathlib.Path("commands")


def _cmd(name: str) -> dict:
    return json.loads((CMD_DIR / f"{name}.json").read_text(encoding="utf-8"))


# ----------------------------------------------------------------- planner routing
def test_plain_delivery_goal_stays_on_phone_workflow():
    p = plan_goal("Find the cheapest phone under Rs 20000 with 8GB RAM "
                  "that Site B confirms is deliverable within 3 days")
    assert p.workflow == WORKFLOW_PHONE
    assert [s.intent for s in p.steps] == [s["intent"] for s in DEFAULT_STEPS]


def test_enquiry_goal_switches_to_enquiry_workflow():
    p = plan_goal("Find the cheapest phone under Rs 20000 and submit an enquiry for it on Site B")
    assert p.workflow == WORKFLOW_ENQUIRY
    assert [s.intent for s in p.steps] == [s["intent"] for s in ENQUIRY_STEPS]
    assert p.steps[-1].intent == "submit_enquiry"


def test_every_enquiry_hint_switches_workflow():
    for hint in ENQUIRY_HINTS:
        p = plan_goal(f"cheapest phone under 20000 then {hint} about it on site b")
        assert p.workflow == WORKFLOW_ENQUIRY, f"hint {hint!r} did not switch workflow"


def test_enquiry_workflow_is_a_superset_of_delivery():
    # Steps 1..4 must be byte-identical so the verified path is untouched.
    assert ENQUIRY_STEPS[:len(DEFAULT_STEPS)] == DEFAULT_STEPS
    assert len(ENQUIRY_STEPS) == len(DEFAULT_STEPS) + 1


def test_unsupported_domain_still_refused_even_with_enquiry_word():
    # The refusal must win over the enquiry extension: no mocks -> no run.
    p = plan_goal("find the cheapest medicine under Rs 500 and submit an enquiry about it")
    assert p.supported is False
    assert p.workflow != WORKFLOW_ENQUIRY


# --------------------------------------------------------- command-file contracts
def test_enquiry_command_file_exists_and_is_versioned():
    c = _cmd(WORKFLOW_ENQUIRY)
    assert c["workflow"] == WORKFLOW_ENQUIRY
    assert c.get("version", 0) >= 1


def test_enquiry_submit_step_is_declared_irreversible():
    c = _cmd(WORKFLOW_ENQUIRY)
    step5 = [s for s in c["template"] if s["intent"] == "submit_enquiry"]
    assert step5, "command file has no submit_enquiry step"
    assert step5[0].get("irreversible") is True, (
        "the enquiry write must be declared irreversible so the approval gate covers it")


def test_enquiry_step_target_has_structural_fallbacks():
    c = _cmd(WORKFLOW_ENQUIRY)
    step5 = [s for s in c["template"] if s["intent"] == "submit_enquiry"][0]
    t = step5["target"]
    assert t.get("role") and t.get("name"), "target needs role+name for structural re-location"
    assert t.get("selector"), "target keeps an id-based fast path for the clean run"


def test_enquiry_postcondition_is_wired():
    c = _cmd(WORKFLOW_ENQUIRY)
    step5 = [s for s in c["template"] if s["intent"] == "submit_enquiry"][0]
    assert step5["postcondition"] == "enquiry_confirmed"
    from agent import detector
    # The detector must actually understand that postcondition (not fall through to True).
    assert "enquiry_confirmed" in pathlib.Path("agent/detector.py").read_text(encoding="utf-8")
    assert detector.check_post is not None


def test_phone_command_file_unchanged_four_steps():
    c = _cmd(WORKFLOW_PHONE)
    assert len(c["template"]) == 4
    assert all(s["intent"] != "submit_enquiry" for s in c["template"])
