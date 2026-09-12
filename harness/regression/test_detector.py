"""Detector unit tests: error pages, modals, renames. Uses a stub page (no browser)."""
from agent import detector as det


class _Loc:
    def __init__(self, count=0, visible=False, text=""):
        self._count, self._visible, self._text = count, visible, text
    def count(self):
        return self._count
    @property
    def first(self):
        return self
    def is_visible(self):
        return self._visible


class FakePage:
    def __init__(self, body="", title="", modal=False, confirm=False):
        self._body, self._title = body, title
        self._modal, self._confirm = modal, confirm
    def evaluate(self, _js):
        return self._body
    def title(self):
        return self._title
    def locator(self, sel):
        if sel == "#chaos-modal":
            return _Loc(1 if self._modal else 0, self._modal)
        if sel == "#chaos-confirm":
            return _Loc(1 if self._confirm else 0, self._confirm)
        return _Loc(0, False)


def test_error_page_detected():
    out = det.scan(FakePage(body="oops", title="500 Internal Server Error"))
    assert [c.type for c in out] == ["error_page"]


def test_modal_and_extra_step_detected():
    out = det.scan(FakePage(body="shop", modal=True, confirm=True))
    assert {c.type for c in out} >= {"modal", "extra_step"}
    assert all(c.timestamp_ms > 0 for c in out)


def test_rename_detected():
    out = det.scan(FakePage(body="press Refine Results to continue"))
    assert [c.type for c in out] == ["label_renamed"]
    assert out[0].expected == "Apply Filter" and out[0].observed == "Refine Results"


def test_clean_page_no_changes():
    out = det.scan(FakePage(body="Apply Filter Search phones", title="VoltKart"))
    assert out == []


def test_postcondition_checks():
    ok, obs = det.check_post(FakePage(), "results_visible")
    assert ok is False and obs == "results_missing"
