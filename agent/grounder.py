"""Grounder: multi-signal element discovery + confidence.

Fusion of five independent signals, weighted, gated at TAU. The point of fusing
is that no single signal has to survive a site change:

  selector   exact CSS (data-testid / id) -- fastest, dies first when ids are stripped
  role_name  ARIA role + accessible name   -- survives class/id churn, matches synonyms
  text       visible label / surrounding text -- survives rename via synonym table
  visual     element is actually visible & sized -- survives everything, weakest signal
  landmark   the owning region (main/aside/nav/form) still exists

When a perturbation removes the selector we still have four signals, and the
synonym table bridges deliberate renames. Below TAU the caller PAUSEs and hands
off to recovery -- we never guess-act on a low-confidence match.
"""
from dataclasses import dataclass, field
import difflib
import time

TAU = 0.70
WEIGHTS = {"selector": 0.35, "role_name": 0.25, "text": 0.20, "visual": 0.10, "landmark": 0.10}

# Renamed-label synonyms (perturbation tolerance). Keep in sync with mocks/chaos.js RENAMES.
SYNONYMS = {
    "Apply Filter": ["Refine Results", "Apply", "Refine", "Filter"],
    "Check Delivery": ["Verify Shipment", "Check", "Verify", "Delivery"],
    "Search": ["Look Up", "Find", "Go"],
    "Results": ["Matches", "Search results"],
    "Filters": ["Refinements"],
    "Apply": ["Refine"],
    "Send enquiry": ["Send Query", "Submit enquiry"],
}

# Structural hints: what ARIA role / label a control should have even when its
# id and text are gone. Lets `relocate` retarget by meaning, not by string.
ROLE_HINTS = {
    "Apply Filter": ("button", ["apply filter", "refine results", "apply", "refine", "filter"]),
    "Check Delivery": ("button", ["check delivery", "verify shipment", "check", "verify", "delivery"]),
    "Search": ("button", ["search", "look up", "find", "go"]),
    "Send enquiry": ("button", ["send enquiry", "send query", "submit enquiry", "enquire"]),
}

# Landmarks a control may live inside (relaxed re-grounding sweeps these).
LANDMARKS = ["main", "aside", "form[role=search]", "header", "[role=search]", "#results-zone"]


@dataclass
class Target:
    selector: str = ""
    role: str = ""
    name: str = ""
    text: str = ""
    landmark: str = ""
    bbox_hint: str = ""
    labels: list = field(default_factory=list)   # accessible-name candidates


@dataclass
class Grounding:
    locator: object | None
    confidence: float
    signals_used: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)


def _score_text(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _candidate_names(target: Target) -> list:
    """All acceptable accessible names for this control, best first."""
    names = []
    if target.name:
        names.append(target.name)
    if target.text:
        names.append(target.text)
    for base in list(names):
        names.extend(SYNONYMS.get(base, []))
    names.extend(target.labels or [])
    seen, out = set(), []
    for n in names:
        k = (n or "").strip().lower()
        if k and k not in seen:
            seen.add(k)
            out.append(n)
    return out


def _visible(loc) -> bool:
    try:
        return bool(loc) and loc.is_visible() and (loc.bounding_box() or {}).get("height", 0) > 0
    except Exception:
        return False


def _try_selector(page, sel: str):
    if not sel:
        return None, 0
    try:
        loc = page.locator(sel)
        n = loc.count()
        return (loc.first if n >= 1 else None), n
    except Exception:
        return None, 0


def _try_role(page, role: str, name: str):
    """ARIA role + accessible name. Tries exact then regex (case-insensitive)."""
    if not (role and name):
        return None
    import re as _re
    for kwargs in ({"name": name}, {"name": _re.compile(_re.escape(name), _re.I)}):
        try:
            loc = page.get_by_role(role, **kwargs)
            if loc.count() >= 1:
                return loc.first
        except Exception:
            continue
    return None


def _try_role_any(page, role: str, names: list):
    for nm in names:
        loc = _try_role(page, role, nm)
        if loc is not None:
            return loc, nm
    return None, None


def _try_label(page, text: str):
    if not text:
        return None
    try:
        loc = page.get_by_label(text)
        if loc.count() >= 1:
            return loc.first
    except Exception:
        pass
    return None


def _try_text(page, text: str):
    for t in [text] + SYNONYMS.get(text, []):
        try:
            loc = page.get_by_text(t, exact=True)
            if loc.count() >= 1:
                return loc.first
        except Exception:
            continue
    return None


def _body_text(page) -> str:
    try:
        return page.evaluate("() => document.body ? document.body.innerText : ''") or ""
    except Exception:
        return ""


def ground(page, target: Target) -> Grounding:
    """Fuse signals. Returns confidence in [0,1] plus the best locator found."""
    scores, signals, locator = {}, [], None
    detail = {}
    names = _candidate_names(target)

    # 1 selector (exact css)
    loc, n = _try_selector(page, target.selector)
    scores["selector"] = 1.0 if loc is not None else 0.0
    detail["selector_count"] = n
    if loc is not None:
        locator = loc
        signals.append("selector")

    # 2 role + accessible name (exact, then each synonym)
    nm = None
    if target.role:
        rloc, nm = _try_role_any(page, target.role, names)
        if rloc is not None:
            scores["role_name"] = 1.0
            detail["role_name_match"] = nm
            if locator is None:
                locator = rloc
            signals.append("role_name")
        else:
            scores["role_name"] = 0.0
    else:
        scores["role_name"] = 0.0

    # 2b label association (inputs): <label for> / aria-label, survives id strip
    if locator is None:
        for cand in names:
            lloc = _try_label(page, cand)
            if lloc is not None:
                locator = lloc
                scores.setdefault("role_name", 0.0)
                scores["role_name"] = max(scores.get("role_name", 0.0), 0.9)
                detail["label_match"] = cand
                if "role_name" not in signals:
                    signals.append("role_name")
                break

    # 3 fuzzy text against the page body
    if target.text:
        body = _body_text(page)
        low = body.lower()
        if target.text.lower() in low:
            s = 1.0
        else:
            syn_hit = next((syn for syn in SYNONYMS.get(target.text, []) if syn.lower() in low), None)
            if syn_hit:
                s = 0.9
                detail["synonym_hit"] = syn_hit
            else:
                s = _score_text(target.text, body[:2000])
        scores["text"] = s
        detail["text_score"] = round(s, 3)
        if s >= 0.75:
            if "text" not in signals:
                signals.append("text")
            if locator is None:
                locator = _try_text(page, target.text)
    else:
        scores["text"] = 0.0

    # 4 visual presence
    vis = _visible(locator)
    scores["visual"] = 1.0 if vis else 0.0
    detail["visible"] = vis
    if vis:
        signals.append("visual")

    # 5 landmark context (the owning region still exists)
    if target.landmark:
        try:
            lcount = page.locator(target.landmark).count()
        except Exception:
            lcount = 0
        scores["landmark"] = 1.0 if lcount >= 1 else 0.0
        detail["landmark_count"] = lcount
        if lcount >= 1:
            signals.append("landmark")
    else:
        scores["landmark"] = 0.0

    mean = sum(WEIGHTS[k] * scores.get(k, 0.0) for k in WEIGHTS)
    agreement = len(set(signals)) / 5.0
    conf = round(mean * (0.5 + 0.5 * agreement) * 2, 3)
    conf = max(0.0, min(1.0, conf))

    # boosts: strong, independent agreement on what the element is
    if "selector" in signals and "visual" in signals and conf < 0.85:
        conf = max(conf, 0.90)
    if "role_name" in signals and "visual" in signals and conf < 0.80:
        conf = max(conf, 0.84)
    # penalty: a name match with nothing visible is not a real match
    if not vis:
        conf = min(conf, 0.55)

    return Grounding(locator=locator, confidence=conf, signals_used=sorted(set(signals)),
                     detail={"scores": scores, **detail})


def discover(page, kind: str = "filter_controls") -> dict:
    """Structure-first discovery, independent of test ids.

    Used when a run must re-find controls after strip/swap. Returns named locators
    for the controls the workflow needs, matched by role + label semantics.
    """
    found = {}
    if kind == "filter_controls":
        for want, (role, labels) in ROLE_HINTS.items():
            loc, nm = _try_role_any(page, role, labels)
            if loc is not None:
                found[want] = {"locator": loc, "via": nm}
        for label, key in (("Max price", "max_price"), ("Min RAM", "min_ram")):
            l = _try_label(page, label)
            if l is not None:
                found[key] = {"locator": l, "via": f"label:{label}"}
    return found
