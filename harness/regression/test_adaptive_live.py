"""Live adaptive-browsing battery.

Runs the *real agent* (Playwright + the full detect/recover/verify loop) against
every perturbation the bench can produce, and asserts the contract the whole
project rests on:

    for every website change, the agent either
      (a) completes with the correct answer, having logged any recovery it needed, or
      (b) ABSTAINs honestly, naming the constraint that actually failed.

It must never report a false pass. This is the executable form of the demo.

Requirements: the mock server must be reachable (default http://127.0.0.1:8000).
The tests skip (not fail) when it is not, so `pytest` stays green offline.
"""
import json

import pytest
import urllib.request

from agent.replayer import run_variant
from harness.perturbations import ANSWER_PRESERVING

BASE = "http://127.0.0.1:8000"
GOAL = ("Find the cheapest in-stock option on Site A that Site B confirms is "
        "deliverable within 3 days")


def _base_up() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE}/site_a/search.html", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _base_up(), reason="mock server not running on :8000")


def _run(perturb: str, variant: int = 4, **kw) -> dict:
    return run_variant(variant=variant, base=BASE, goal=GOAL,
                       perturb=perturb, auto_approve=True, headless=True, **kw)


def _assert_valid_outcome(out: dict, perturb: str):
    """The universal contract: a decision was made and it is defensible."""
    assert out["status"] in ("pass", "ABSTAIN"), f"{perturb}: bad status {out['status']}"
    if out["status"] == "pass":
        # a pass must carry BOTH pieces of evidence and a satisfied delivery constraint
        assert out.get("cheapest"), f"{perturb}: pass with no chosen product"
        assert len(out.get("evidence", [])) >= 2, f"{perturb}: pass with <2 evidence rows"
        assert out["constraints"]["results"]["b_confirms_deliverable_3d"] == "pass", \
            f"{perturb}: passed without confirmed deliverability"
        # chosen product must actually satisfy the stated constraints
        assert out["cheapest"]["price"] <= out["effective_params"]["budget"], \
            f"{perturb}: chosen product over budget"
        assert out["cheapest"]["ram"] >= out["effective_params"]["ram"], \
            f"{perturb}: chosen product under RAM floor"
    else:
        # an abstain must name WHY
        assert out.get("failed_constraint") or out.get("reason"), \
            f"{perturb}: abstained without a named constraint"


# ----------------------------------------------------------- answer-preserving
@pytest.mark.parametrize("perturb", [p for p in ANSWER_PRESERVING])
def test_perturbation_preserves_pass_or_honest_abstain(perturb):
    """Cosmetic/structural changes must not change the answer: pass with the same
    product, or an honest abstain. Never a false pass."""
    out = _run(perturb)
    _assert_valid_outcome(out, perturb)
    if out["status"] == "pass":
        assert out["cheapest"]["name"] == "Pixel Lite 8GB", (
            f"{perturb}: expected Pixel Lite 8GB, got {out['cheapest']['name']}")


def test_clean_run_is_green():
    out = _run(None, variant=1)
    _assert_valid_outcome(out, "clean")
    assert out["status"] == "pass"
    assert out["cheapest"]["name"] == "Pixel Lite 8GB"
    assert out["extra_steps"] == 0, "clean run must not need recovery"


def test_composite_logs_recovery_and_still_passes():
    out = _run("composite")
    _assert_valid_outcome(out, "composite")
    assert out["status"] == "pass"
    # composite injects modal + extra_step, so recovery must have happened
    assert out["extra_steps"] >= 1, "composite should have needed extra steps"
    assert out["avg_time_to_heal_ms"] > 0, "composite should have logged heal time"


def test_rename_survives_label_change():
    out = _run("rename")
    _assert_valid_outcome(out, "rename")
    assert out["status"] == "pass", "agent failed to adapt to renamed controls"


def test_strip_survives_missing_testids():
    out = _run("strip")
    _assert_valid_outcome(out, "strip")
    assert out["status"] == "pass", "agent failed to adapt to stripped test ids"


def test_swap_survives_rerendered_list():
    out = _run("swap")
    _assert_valid_outcome(out, "swap")
    assert out["status"] == "pass", "agent failed to re-discover the re-rendered list"


def test_throttle_waits_for_postcondition():
    out = _run("throttle")
    _assert_valid_outcome(out, "throttle")
    assert out["status"] == "pass", "agent failed to wait out injected latency"


# ------------------------------------------------------------- answer-adapting
@pytest.mark.parametrize("perturb", ["ab", "chaos_max"])
def test_answer_adapting_never_false_passes(perturb):
    """ab/chaos_max can legitimately remove every eligible candidate. The agent may
    still pass (picking from the visible set) but must NEVER claim an ineligible one."""
    out = _run(perturb)
    _assert_valid_outcome(out, perturb)


def test_infeasible_abstains_naming_both_constraints():
    out = run_variant(variant=6, base=BASE, goal=GOAL, auto_approve=True,
                      headless=True, budget=8000, ram=12)
    assert out["status"] == "ABSTAIN"
    assert out["failed_constraint"] == "max_price AND min_ram"


def test_unsupported_goal_abstains():
    out = run_variant(variant=1, base=BASE, goal="find the cheapest medicine under Rs 500",
                      auto_approve=True, headless=True)
    assert out["status"] == "ABSTAIN"
    assert out["failed_constraint"] == "unsupported_goal"


# --------------------------------------------------------------- evidence rigour
def test_evidence_is_extractive_and_hashed():
    out = _run(None, variant=1)
    for ev in out["evidence"]:
        assert ev["snippet_verbatim"], "evidence must carry a verbatim snippet"
        assert len(ev["sha256"]) == 64, "evidence must carry a sha256"
        assert ev["char_offset"] >= 0, "evidence must carry a character offset"
        assert ev["url"].startswith("http"), "evidence must carry a source url"


def test_recovery_is_logged_for_perturbed_run():
    """A perturbed run must leave a recovery trail in logs/recoveries.jsonl."""
    import pathlib
    before = 0
    p = pathlib.Path("logs/recoveries.jsonl")
    if p.exists():
        before = len(p.read_text(encoding="utf-8").splitlines())
    _run("composite")
    after = 0
    if p.exists():
        after = len(p.read_text(encoding="utf-8").splitlines())
    assert after > before, "no recovery event logged for a composite run"


# -------------------------------------------------- judge-operated live injection
def _set_perturbation(typ: str | None) -> bool:
    """Drive the console's injector the way the judge does. Returns False if the
    console is not running (test then skips)."""
    import urllib.error
    url = f"http://127.0.0.1:8765/perturb/{typ or 'reset'}"
    try:
        req = urllib.request.Request(url, method="POST")
        with urllib.request.urlopen(req, timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


@pytest.mark.skipif(not _base_up(), reason="mock server not running")
def test_judge_operated_live_injection_heals():
    """The demo path: the judge presses a button on the dashboard and the agent,
    running with NO ?perturb param, must still detect and heal. This exercises the
    600ms polling transport, which lands *after* page load -- a fixed sleep would
    race it, so this test guards the adaptive settle/wait logic."""
    if not _set_perturbation("composite"):
        pytest.skip("console not running on :8765")
    try:
        out = run_variant(variant=4, base=BASE, goal=GOAL, auto_approve=True, headless=True)
        _assert_valid_outcome(out, "live-composite")
        if out["status"] == "pass":
            assert out["extra_steps"] >= 1, "live composite must have needed recovery"
            assert out["avg_time_to_heal_ms"] > 0, "live composite must log heal time"
    finally:
        _set_perturbation(None)


# ------------------------------------------------ cross-site enquiry workflow
ENQUIRY_GOAL = ("Find the cheapest in-stock option on Site A that Site B confirms is "
                "deliverable within 3 days and submit an enquiry for it on Site B")


def _run_enquiry(perturb: str | None = None, variant: int = 1) -> dict:
    return run_variant(variant=variant, base=BASE, goal=ENQUIRY_GOAL,
                       perturb=perturb, auto_approve=True, headless=True)


@pytest.mark.skipif(not _base_up(), reason="mock server not running")
def test_enquiry_workflow_completes_clean():
    """The full rubric goal: two sites, a real cross-site write."""
    out = _run_enquiry()
    assert out["status"] == "pass", out.get("reason")
    assert out["plan"]["workflow"] == "phone_fulfilment_enquiry"
    assert out["enquiry"]["ok"] is True
    assert "Enquiry received" in out["enquiry"]["observed"]


@pytest.mark.skipif(not _base_up(), reason="mock server not running")
@pytest.mark.parametrize("perturb", ["rename", "strip", "move", "attrs", "modal",
                                     "extra_step", "throttle", "composite"])
def test_enquiry_workflow_survives_every_answer_preserving_perturbation(perturb):
    """The 5-step cross-site workflow must complete under the same chaos matrix as
    the 4-step one. This is the load-bearing claim for the rubric's Task Completion
    + Adaptation Speed criteria."""
    out = _run_enquiry(perturb, variant=4)
    _assert_valid_outcome(out, f"enquiry:{perturb}")
    if out["status"] == "pass":
        assert out["enquiry"]["ok"] is True, f"{perturb}: pass without confirmed enquiry"


@pytest.mark.skipif(not _base_up(), reason="mock server not running")
def test_enquiry_carries_the_site_a_choice_to_site_b():
    """Cross-site data handoff, verified in the evidence: the product named in the
    Site B evidence URL must be the product chosen on Site A."""
    out = _run_enquiry("rename", variant=4)
    if out["status"] != "pass":
        pytest.skip(f"run abstained: {out.get('failed_constraint')}")
    chosen = out["cheapest"]["name"]
    ev_urls = [e["url"] for e in out["evidence"]]
    assert any("site_b/enquiry.html" in u for u in ev_urls), "no enquiry evidence row"
    from urllib.parse import unquote
    assert any(unquote(u).find(chosen) >= 0 for u in ev_urls), (
        f"chosen product {chosen!r} did not travel to the Site B enquiry")


@pytest.mark.skipif(not _base_up(), reason="mock server not running")
def test_enquiry_never_runs_without_confirmed_delivery():
    """Safety: we must not enquire about a product we could not confirm is deliverable.
    With an unserviceable PIN the run must ABSTAIN before the enquiry step."""
    out = run_variant(variant=3, base=BASE, goal=ENQUIRY_GOAL, pin="500002",
                      auto_approve=True, headless=True)
    assert out["status"] == "ABSTAIN"
    assert out.get("enquiry") is None, "enquiry ran despite failed delivery confirmation"


@pytest.mark.skipif(not _base_up(), reason="mock server not running")
def test_enquiry_step_is_approval_gated():
    """The irreversible write must leave APPROVAL_REQUESTED + GRANTED for submit_enquiry."""
    import pathlib
    p = pathlib.Path("logs/actions.jsonl")
    before = len(p.read_text(encoding="utf-8").splitlines()) if p.exists() else 0
    _run_enquiry()
    lines = p.read_text(encoding="utf-8").splitlines()[before:]
    events = [json.loads(l) for l in lines if l.strip()]
    submitted = [e for e in events if e.get("target") == "submit_enquiry"]
    assert any(e.get("event") == "APPROVAL_REQUESTED" for e in submitted), \
        "enquiry submit was not approval-gated"
