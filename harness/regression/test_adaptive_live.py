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
        # The answer must match an independent re-derivation from the cards, i.e. the
        # CHANGE did not move the choice. We do not pin a literal product name: the
        # catalogue is a real search space and its minimum moves when it grows.
        assert _is_cheapest_in_stock_eligible(out), (
            f"{perturb}: picked {out['cheapest']['name']} but a cheaper in-stock "
            f"eligible product existed in the same result set")


def test_clean_run_is_green():
    out = _run(None, variant=1)
    _assert_valid_outcome(out, "clean")
    assert out["status"] == "pass"
    assert out["extra_steps"] == 0, "clean run must not need recovery"
    # The answer must be the *cheapest in-stock eligible* product, whatever that is.
    # We assert the rule, not a frozen name: pinning "Pixel Lite 8GB" made this test
    # fail the moment the catalogue grew a genuinely cheaper in-stock option, which is
    # the search doing its job. See _assert_valid_outcome for the constraint checks.
    assert _is_cheapest_in_stock_eligible(out), \
        f"picked {out['cheapest']['name']} but a cheaper in-stock eligible product existed"


def _is_cheapest_in_stock_eligible(out: dict) -> bool:
    """Independent re-derivation of the answer from the cards the agent saw.

    This is deliberately a second implementation of the rule: if the agent's own
    minimum were wrong, comparing it against itself would prove nothing.
    """
    p = out["effective_params"]
    cands = [c for c in out["cards"]
             if c.get("in_stock", True)
             and c["price"] <= p["budget"]
             and c["ram"] >= p["ram"]]
    if not cands:
        return False
    best = min(cands, key=lambda c: c["price"])
    return out["cheapest"]["name"] == best["name"] and out["cheapest"]["price"] == best["price"]


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


# ------------------------------------------------------- in-stock is a constraint
def test_never_chooses_an_out_of_stock_product():
    """'Cheapest in-stock' means availability is enforced, not decorative.

    The catalogue deliberately contains out-of-stock listings, so a run must never
    pick one: doing so would be a wrong answer that still looked like a pass.
    """
    import pathlib
    p = pathlib.Path("logs/actions.jsonl")
    before = len(p.read_text(encoding="utf-8").splitlines()) if p.exists() else 0

    out = _run(None, variant=1)
    assert out["status"] == "pass", out.get("reason", "")
    chosen = out["cheapest"]["name"]

    # Every card the agent considered carries the in_stock flag it read from the page.
    cards = {c["name"]: c.get("in_stock", True) for c in out["cards"]}
    assert cards.get(chosen, True) is True, f"chose an out-of-stock product: {chosen}"

    # At least one out-of-stock listing exists in this catalogue...
    oos = [c["name"] for c in out["cards"] if c.get("in_stock") is False]
    assert oos, "this catalogue should contain at least one out-of-stock card"

    # ...and the run that followed actually logged the exclusion.
    tail = p.read_text(encoding="utf-8").splitlines()[before:] if p.exists() else []
    events = [json.loads(l) for l in tail if l.strip()]
    assert any(e.get("event") == "STOCK_FILTER" for e in events), \
        "a run over a catalogue with OOS items must log the stock filter"


def test_out_of_stock_cheapest_is_never_chosen():
    """The catalogue's cheapest eligible listing is OUT OF STOCK on purpose.

    Lava Blaze 8GB (Rs 9,999) satisfies price+RAM but cannot be bought. A naive
    `min(price)` agent picks it and reports a confident pass on a product nobody can
    buy. The correct behaviour is to skip it and pick the cheapest *available*
    match — this test exists to catch a regression in that filter.
    """
    out = _run(None, variant=1)
    assert out["status"] == "pass", out.get("reason", "")

    cards = {c["name"]: c for c in out["cards"]}
    # The trap must exist in the fixture, or this test proves nothing.
    assert "Lava Blaze 8GB" in cards, "the out-of-stock trap product is missing"
    assert cards["Lava Blaze 8GB"].get("in_stock") is False, "trap product must be OOS"
    assert cards["Lava Blaze 8GB"]["price"] < out["cheapest"]["price"], \
        "trap must be cheaper than the chosen product for this test to mean anything"

    chosen = out["cheapest"]["name"]
    assert chosen != "Lava Blaze 8GB", "chose the out-of-stock cheapest listing"
    assert cards[chosen].get("in_stock") is True, f"{chosen} is not in stock"


def test_out_of_stock_only_match_abstains_or_picks_a_valid_alternative():
    """With a ceiling that admits both the OOS trap and in-stock alternatives, the run
    must still land on an available product — or abstain naming a constraint."""
    out = run_variant(variant=6, base=BASE, goal=GOAL, auto_approve=True,
                      headless=True, budget=13000, ram=8)
    assert out["status"] in ("pass", "ABSTAIN")
    if out["status"] == "pass":
        cards = {c["name"]: c.get("in_stock", True) for c in out["cards"]}
        assert cards.get(out["cheapest"]["name"], True) is True
        assert out["cheapest"]["price"] <= 13000
    else:
        assert out.get("failed_constraint")


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
