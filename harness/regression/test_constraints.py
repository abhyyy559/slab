"""Negative-match guard for the deliverability checker (verification infrastructure).

Bug class: substring-matching a bare positive word ("available") also matches its
negation ("not available"). The checker must require positive proof AND reject
negative-tagged strings. Caught live by the regression guard 2026-09-12.
"""
import pytest

from agent.constraints import deliverable_within_days

NEGATIVES = [
    "Delivery not available to PIN 500002",
    "Delivery unavailable to PIN 500002",
    "Item out of stock, delivery unavailable",
    "No delivery to this region currently",
    "Currently unavailable at this branch",
    "We cannot deliver within 3 days",
    "",
]

POSITIVES = [
    "Delivery available to PIN 500001 in 2-3 days",
]

@pytest.mark.parametrize("text", NEGATIVES)
def test_rejects_negative_tagged_strings(text):
    assert deliverable_within_days(text) is False

@pytest.mark.parametrize("text", POSITIVES)
def test_accepts_positive_proof(text):
    assert deliverable_within_days(text) is True
