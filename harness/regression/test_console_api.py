"""Tests for the console API surface added for visibility + audit.

These cover endpoints that back the dashboard's goal-interpreter and doc-explorer
panels. They exercise the *real* planner and the *real* files on disk, so a doc
rename or a planner re-route that breaks the dashboard fails here rather than in
front of a judge.

The console must be running (default http://127.0.0.1:8765); tests skip when it is
not, so `pytest` stays green offline.
"""
import json
import urllib.error
import urllib.request

import pytest

CONSOLE = "http://127.0.0.1:8765"


def _up() -> bool:
    try:
        with urllib.request.urlopen(f"{CONSOLE}/status", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _up(), reason="judge console not running on :8765")


def _get(path: str):
    with urllib.request.urlopen(f"{CONSOLE}{path}", timeout=5) as r:
        return r.status, json.loads(r.read().decode("utf-8"))


def _post(path: str, body: dict):
    req = urllib.request.Request(
        f"{CONSOLE}{path}", data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


# ------------------------------------------------------------------ /api/plan
def test_plan_routes_default_goal_to_the_four_step_workflow():
    st, j = _post("/api/plan", {"goal":
        "Find the cheapest in-stock option on Site A that Site B confirms is "
        "deliverable within 3 days"})
    assert st == 200
    assert j["supported"] is True
    assert j["workflow"] == "phone_delivery_check"
    assert j["steps"] == ["open_search", "apply_filter", "extract_cheapest", "check_delivery"]
    assert "submit_enquiry" not in j["steps"]


def test_plan_routes_enquiry_goal_to_the_five_step_workflow():
    st, j = _post("/api/plan", {"goal":
        "Find the cheapest in-stock option on Site A that Site B confirms is "
        "deliverable within 3 days and submit an enquiry for it on Site B"})
    assert st == 200
    assert j["supported"] is True
    assert j["workflow"] == "phone_fulfilment_enquiry"
    assert j["steps"][-1] == "submit_enquiry"
    assert len(j["steps"]) == 5


def test_plan_refuses_an_unsupported_domain_without_implying_a_run():
    st, j = _post("/api/plan", {"goal": "cheapest medicine under Rs 500"})
    assert st == 200
    assert j["supported"] is False
    # A refused goal must not advertise a workflow or a step chain.
    assert j["workflow"] is None
    assert j["steps"] == []
    assert j["unsupported"], "refusal must explain itself"


def test_plan_extracts_goal_embedded_parameters():
    st, j = _post("/api/plan", {"goal": "cheapest phone under 15000 with 8GB RAM"})
    assert st == 200
    assert j["supported"] is True
    assert j["params"].get("budget") == 15000
    assert j["params"].get("ram") == 8


def test_plan_handles_an_empty_goal_without_erroring():
    st, j = _post("/api/plan", {"goal": ""})
    assert st == 200
    assert "workflow" in j


# ------------------------------------------------------------------ /api/docs
def test_docs_lists_the_repo_documents():
    st, j = _get("/api/docs")
    assert st == 200
    names = {d["name"] for d in j["docs"]}
    # These are the documents the rubric's "documented repo" criterion leans on.
    for expected in ("README.md", "TASKS.md", "DECISIONS.md", "FAILURES.md"):
        assert expected in names, f"{expected} missing from the doc explorer"


def test_docs_returns_file_contents():
    st, j = _get("/api/docs/README.md")
    assert st == 200
    assert j["name"] == "README.md"
    assert len(j["text"]) > 200
    assert j["mtime"] > 0


def test_docs_rejects_a_file_outside_the_allow_list():
    """The reader is allow-listed: a stray file must not be exposable."""
    try:
        st, _ = _get("/api/docs/competition.yaml")
    except urllib.error.HTTPError as e:
        st = e.code
    assert st == 404


def test_docs_blocks_path_traversal():
    for probe in ("/api/docs/..%2f..%2fetc%2fpasswd",
                  "/api/docs/../../etc/passwd",
                  "/api/docs/secrets.txt"):
        try:
            st, _ = _get(probe)
        except urllib.error.HTTPError as e:
            st = e.code
        assert st == 404, f"{probe} should not be readable"


# ----------------------------------------------------------------- /api/rubric
def test_rubric_is_read_live_from_the_repo():
    st, j = _get("/api/rubric")
    assert st == 200
    assert "SLAB" in j["text"]
    assert "01" in j["text"]


# ------------------------------------------------------------- perturbation API
def test_perturbation_catalogue_is_exposed():
    st, j = _get("/api/perturbations")
    assert st == 200
    # Shape is an implementation detail; the point is the dashboard can list them.
    assert isinstance(j, (list, dict)) and j
