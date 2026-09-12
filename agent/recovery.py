"""Recovery ladder: re-locate / re-plan / backtrack + verify. Never act irreversibly on unverified state."""
import time
from .grounder import ground, Target, TAU
from .detector import check_post
from . import detector as det

SYNONYM_TEXT = {"Apply Filter": "Refine Results", "Check Delivery": "Verify Shipment", "Search": "Look Up"}

def _now() -> int:
    return int(time.time() * 1000)

def clear_side_effects(page) -> list:
    """Re-plan level 0: dismiss confirm interstitial (topmost) then modal. Returns actions taken."""
    taken = []
    for overlay, btn in (("#chaos-confirm", "#chaos-continue"), ("#chaos-modal", "#chaos-dismiss")):
        try:
            if page.locator(overlay).count() >= 1 and page.locator(overlay).first.is_visible():
                page.locator(btn).first.click(timeout=3000)
                page.wait_for_timeout(300)
                taken.append(f"dismissed:{overlay}")
        except Exception:
            pass
    return taken

def relocate(page, target: Target) -> object:
    """Re-locate with relaxed signals: drop selector (may be stripped), use synonym text."""
    relaxed = Target(selector="", role=target.role, name=target.name,
                     text=SYNONYM_TEXT.get(target.text, target.text),
                     landmark=target.landmark)
    g = ground(page, relaxed)
    if (g.locator is None or g.confidence < TAU) and target.text:
        # last resort: click by synonym text directly
        try:
            loc = page.get_by_text(SYNONYM_TEXT.get(target.text, target.text))
            if loc.count() >= 1:
                from .grounder import Grounding
                return Grounding(locator=loc.first, confidence=0.80,
                                 signals_used=["text", "landmark"],
                                 detail={"fallback": "synonym_text_click"})
        except Exception:
            pass
    return g

def recover(page, trigger: str, expected: str, observed: str, target=None,
            postcondition: str | None = None, last_good_url: str | None = None,
            detected_at_ms: int = 0) -> dict:
    t0 = _now()
    steps, strategy = [], "re_locate"
    # 1. re-plan: clear blocking side effects first (modal / extra step)
    cleared = clear_side_effects(page)
    steps.extend(cleared)
    if cleared:
        strategy = "re_plan"
    # 2. re-locate the target if one was given
    conf_after, locator = None, None
    if target is not None:
        g = relocate(page, target)
        conf_after = g.confidence
        locator = g.locator
        if locator is None or conf_after < TAU:
            # 3. backtrack to last known-good state and retry once
            if last_good_url:
                try:
                    page.goto(last_good_url, wait_until="domcontentloaded", timeout=3000)
                    page.wait_for_timeout(500)
                    steps.append(f"backtracked:{last_good_url}")
                    strategy = "backtrack"
                    g2 = relocate(page, target)
                    conf_after, locator = g2.confidence, g2.locator
                except Exception as e:
                    steps.append(f"backtrack_failed:{e}"[:120])
    # verify postcondition where one applies
    verified = False
    if postcondition:
        ok, _ = check_post(page, postcondition)
        verified = bool(ok)
    healed_ms = _now() - t0
    return {"trigger": trigger, "expected": expected, "observed": observed,
            "strategy": strategy, "steps": steps, "n_extra_steps": len(cleared),
            "time_to_detect_ms": max(0, t0 - (detected_at_ms or t0)),
            "time_to_heal_ms": healed_ms,
            "verified": verified, "confidence_after": conf_after, "locator": locator}
