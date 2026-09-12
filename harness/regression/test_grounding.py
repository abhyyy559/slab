"""Unit tests for the structural grounding / detection / recovery logic.

No browser needed: we exercise the pure helpers so a regression in the reasoning
layer fails fast, and reserve the live DOM for test_adaptive_live.py.
"""
import pytest

from agent.grounder import (_candidate_names, _score_text, SYNONYMS, ROLE_HINTS,
                            LANDMARKS, TAU, WEIGHTS, Target)
from agent.detector import ChangeDetected, RENAMED_PAIRS
from agent.constraints import deliverable_within_days


# ----------------------------------------------------------------- grounder
def test_weights_sum_to_one():
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_tau_is_the_documented_gate():
    assert TAU == 0.70


def test_candidate_names_include_synonyms():
    names = _candidate_names(Target(name="Apply Filter", text="Apply Filter"))
    lowered = [n.lower() for n in names]
    assert "apply filter" in lowered
    assert "refine results" in lowered
    assert len(lowered) == len(set(lowered)), "candidate names must be de-duplicated"


def test_candidate_names_tolerates_empty_target():
    assert _candidate_names(Target()) == []


def test_score_text_is_symmetric_and_bounded():
    assert _score_text("Apply Filter", "Apply Filter") == 1.0
    assert _score_text("Apply Filter", "Refine Results") < 0.7
    assert 0.0 <= _score_text("abc", "xyz") <= 1.0
    assert _score_text("", "x") == 0.0


@pytest.mark.parametrize("label", ["Apply Filter", "Check Delivery", "Search"])
def test_role_hints_exist_for_every_control(label):
    assert label in ROLE_HINTS
    role, names = ROLE_HINTS[label]
    assert role == "button"
    assert any(n.lower() == label.lower() or label.lower() in n.lower() for n in names)


def test_landmarks_cover_the_workflow_regions():
    assert any("main" in l for l in LANDMARKS)
    assert any("search" in l for l in LANDMARKS)
    assert any("results" in l for l in LANDMARKS)


# ------------------------------------------------------------------ detector
def test_renamed_pairs_are_two_sided():
    for a, b in RENAMED_PAIRS:
        assert a and b
        assert a != b


def test_change_detected_defaults():
    c = ChangeDetected("modal", "no_blocking_modal", "chaos-modal visible")
    assert c.signals == []
    assert c.timestamp_ms == 0


# --------------------------------------------------------------- constraints
def test_deliverable_requires_positive_proof():
    assert deliverable_within_days("Delivery available to PIN 500001 in 2-3 days") is True
    assert deliverable_within_days("Delivery not available to PIN 500001") is False


@pytest.mark.parametrize("text", [
    "Delivery not available", "unavailable", "Item out of stock",
    "no delivery", "cannot deliver", "",
])
def test_deliverable_rejects_negatives(text):
    assert deliverable_within_days(text) is False
