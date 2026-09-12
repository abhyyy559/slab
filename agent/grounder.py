"""Grounder: 5-signal fusion (selector, role_name, text, visual-stub, landmark) + confidence. tau=0.70."""
from dataclasses import dataclass, field
import difflib

TAU = 0.70
WEIGHTS = {"selector": 0.35, "role_name": 0.25, "text": 0.20, "visual": 0.10, "landmark": 0.10}

@dataclass
class Target:
    selector: str = ""
    role: str = ""
    name: str = ""
    text: str = ""
    landmark: str = ""
    bbox_hint: str = ""

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

def ground(page, target: Target) -> Grounding:
    scores, signals, locator = {}, [], None
    detail = {}
    # 1 selector (exact css)
    try:
        if target.selector:
            loc = page.locator(target.selector)
            n = loc.count()
            scores["selector"] = 1.0 if n >= 1 else 0.0
            detail["selector_count"] = n
            if n >= 1 and locator is None:
                locator = loc.first
                signals.append("selector")
        else:
            scores["selector"] = 0.0
    except Exception as e:
        scores["selector"] = 0.0
        detail["selector_error"] = str(e)[:200]
    # 2 role+name (aria)
    try:
        if target.role and target.name:
            loc = page.get_by_role(target.role, name=target.name) if hasattr(page, "get_by_role") else None
            n = loc.count() if loc else 0
            scores["role_name"] = 1.0 if n >= 1 else 0.0
            detail["role_name_count"] = n
            if n >= 1:
                if locator is None:
                    locator = loc.first
                if "role_name" not in signals:
                    signals.append("role_name")
        else:
            scores["role_name"] = 0.0
    except Exception as e:
        scores["role_name"] = 0.0
        detail["role_error"] = str(e)[:200]
    # 3 fuzzy text
    try:
        if target.text:
            body = page.evaluate("() => document.body ? document.body.innerText : ''") or ""
            # best window score approximated by ratio on first 2000 chars window containing? simple global containment
            s = 1.0 if target.text.lower() in body.lower() else _score_text(target.text, body[:2000])
            scores["text"] = s
            detail["text_score"] = round(s, 3)
            if s >= 0.75 and "text" not in signals:
                signals.append("text")
                if locator is None:
                    try:
                        loc = page.get_by_text(target.text)
                        if loc.count() >= 1:
                            locator = loc.first
                    except Exception:
                        pass
        else:
            scores["text"] = 0.0
    except Exception as e:
        scores["text"] = 0.0
        detail["text_error"] = str(e)[:200]
    # 4 visual stub (phash anchor not implemented in v1 -> presence of any visible element matching selector)
    try:
        vis = False
        if locator is not None:
            try:
                vis = locator.is_visible()
            except Exception:
                vis = False
        scores["visual"] = 1.0 if vis else 0.0
        detail["visible"] = vis
        if vis and "visual" not in signals:
            signals.append("visual")
    except Exception:
        scores["visual"] = 0.0
    # 5 landmark (relative to stable landmark)
    try:
        if target.landmark:
            n = page.locator(target.landmark).count()
            s = 1.0 if n >= 1 else 0.0
            scores["landmark"] = s
            detail["landmark_count"] = n
            if s and "landmark" not in signals:
                signals.append("landmark")
        else:
            scores["landmark"] = 0.0
    except Exception:
        scores["landmark"] = 0.0
    mean = sum(WEIGHTS[k] * scores.get(k, 0.0) for k in WEIGHTS)
    agreement = (len(signals) / 5.0)
    conf = round(mean * (0.5 + 0.5 * agreement) * 2, 3)
    conf = max(0.0, min(1.0, conf))
    # boost: exact selector + visible is strong
    if "selector" in signals and "visual" in signals and conf < 0.85:
        conf = max(conf, 0.9)
    return Grounding(locator=locator, confidence=conf, signals_used=signals, detail={"scores": scores, **detail})
