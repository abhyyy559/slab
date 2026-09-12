"""Chaos-engine contract tests (no browser required).

These pin the *shape* of the perturbation catalogue and the chaos.js source so a
new perturbation cannot be added to one half without the other. The live DOM
behaviour is covered by test_adaptive_live.py; this file is the fast gate that
runs on every commit.
"""
import pathlib
import re

from harness.perturbations import (PERTURBATIONS, CHAOS_TYPES, COMPOSITE_SUBTYPES,
                                   ANSWER_PRESERVING, ANSWER_ADAPTING)

CHAOS_JS = pathlib.Path("mocks/chaos.js").read_text(encoding="utf-8")


def test_catalogue_has_core_types():
    for t in ("rename", "strip", "move", "attrs", "modal", "extra_step",
              "throttle", "ab", "swap", "composite", "chaos_max"):
        assert t in PERTURBATIONS, f"missing perturbation: {t}"


def test_reset_is_not_a_chaos_type():
    assert "reset" not in CHAOS_TYPES
    assert "reset" in PERTURBATIONS


def test_composite_subtypes_are_real():
    for t in COMPOSITE_SUBTYPES:
        assert t in PERTURBATIONS, f"composite references unknown type {t}"


def test_answer_partition_is_total():
    # every chaos type is classified as either answer-preserving or answer-adapting
    for t in CHAOS_TYPES:
        assert t in ANSWER_PRESERVING or t in ANSWER_ADAPTING, f"unclassified: {t}"


def test_chaos_js_implements_every_type():
    # Each non-reset type must appear in chaos.js's setOf() dispatcher or apply().
    for t in ("rename", "strip", "move", "attrs", "modal", "extra_step",
              "throttle", "ab", "swap"):
        assert f'"{t}"' in CHAOS_JS, f"chaos.js has no handler referencing {t}"


def test_chaos_js_defines_composite_and_max():
    assert "composite" in CHAOS_JS
    assert "chaos_max" in CHAOS_JS


def test_chaos_js_rename_table_matches_grounder_synonyms():
    """A rename in the page and the synonym the agent looks for must agree."""
    from agent.grounder import SYNONYMS
    # Pull the RENAMES table out of chaos.js.
    m = re.search(r"var RENAMES\s*=\s*\[(.*?)\];", CHAOS_JS, re.S)
    assert m, "chaos.js RENAMES table not found"
    pairs = re.findall(r'\["([^"]+)",\s*"([^"]+)"\]', m.group(1))
    assert pairs, "no rename pairs parsed"
    for original, renamed in pairs:
        syns = [s.lower() for s in SYNONYMS.get(original, [])]
        assert renamed.lower() in syns, (
            f"chaos renames {original!r} -> {renamed!r} but grounder SYNONYMS "
            f"for {original!r} is {SYNONYMS.get(original)}")


def test_chaos_js_has_both_control_paths():
    assert "perturb=" in CHAOS_JS or "URLSearchParams" in CHAOS_JS, "no deterministic path"
    assert "8765/status" in CHAOS_JS, "no judge-operated polling path"


def test_chaos_js_is_idempotent_guarded():
    # apply() must short-circuit when the same type is re-applied.
    assert re.search(r'if\s*\(\s*key\s*===\s*applied\s*\)\s*return', CHAOS_JS), \
        "apply() is not idempotent-guarded"
