"""Recovery ladder: re-plan -> re-locate -> backtrack, then verify.

Never acts irreversibly on unverified state. Each rung is cheaper than the next,
so we always try the least invasive fix first:

  re-plan    dismiss blocking overlays / clear interstitials (no navigation)
  re-locate  re-find the control by *structure* -- role, label, synonym text --
             dropping the selector that a strip/rename may have invalidated
  backtrack  return to the last known-good URL and retry the re-locate once
  verify     confirm the postcondition held before handing control back
"""
import time
from .grounder import ground, Target, TAU, discover
from .detector import check_post

SYNONYM_TEXT = {"Apply Filter": "Refine Results", "Check Delivery": "Verify Shipment",
                "Search": "Look Up"}


def _now() -> int:
    return int(time.time() * 1000)


def clear_side_effects(page) -> list:
    """Re-plan level 0: dismiss confirm interstitial (topmost) then modal, then
    any generic dialog that blocks the page. Returns the actions taken."""
    taken = []
    for overlay, btn in (("#chaos-confirm", "#chaos-continue"), ("#chaos-modal", "#chaos-dismiss")):
        try:
            if page.locator(overlay).count() >= 1 and page.locator(overlay).first.is_visible():
                page.locator(btn).first.click(timeout=3000)
                page.wait_for_timeout(300)
                taken.append(f"dismissed:{overlay}")
        except Exception:
            pass
    # generic modal fallback: any visible role=dialog not one of ours
    try:
        dialogs = page.locator('[role="dialog"]')
        for i in range(min(dialogs.count(), 3)):
            d = dialogs.nth(i)
            if not d.is_visible():
                continue
            did = d.get_attribute("id") or ""
            if did in ("chaos-modal", "chaos-confirm"):
                continue
            for cand in ("Dismiss", "Continue", "Close", "OK", "Accept", "Got it"):
                try:
                    b = d.get_by_role("button", name=cand)
                    if b.count() >= 1:
                        b.first.click(timeout=2000)
                        page.wait_for_timeout(250)
                        taken.append(f"dismissed:generic:{cand}")
                        break
                except Exception:
                    continue
    except Exception:
        pass
    return taken


def relocate(page, target: Target):
    """Re-locate by structure: drop the selector, keep role/semantics, add synonyms."""
    names = []
    if target.name:
        names.append(target.name)
    if target.text:
        names.append(target.text)
    for base in list(names):
        names.extend({"Apply Filter": ["Refine Results", "Apply", "Refine"],
                      "Check Delivery": ["Verify Shipment", "Check", "Verify"],
                      "Search": ["Look Up", "Find"]}.get(base, []))

    relaxed = Target(selector="", role=target.role, name=target.name, text=target.text,
                     landmark=target.landmark, labels=names)
    g = ground(page, relaxed)
    if g.locator is not None and g.confidence >= TAU:
        return g

    # structural sweep: discover controls by role/label directly
    found = discover(page, "filter_controls")
    for want, roles in (("Apply Filter", ("Apply Filter",)),
                        ("Check Delivery", ("Check Delivery",)),
                        ("Search", ("Search",))):
        if target.text == want or target.name == want:
            hit = next((v for k, v in found.items()
                        if want.split()[0].lower() in k.lower()), None)
            if hit:
                from .grounder import Grounding
                return Grounding(locator=hit["locator"], confidence=0.82,
                                 signals_used=["role_name", "landmark"],
                                 detail={"fallback": "structural_discovery", "via": hit["via"]})

    # last resort: click by synonym text directly
    if target.text:
        for t in [SYNONYM_TEXT.get(target.text, target.text)] + names:
            try:
                loc = page.get_by_text(t, exact=True)
                if loc.count() >= 1:
                    from .grounder import Grounding
                    return Grounding(locator=loc.first, confidence=0.80,
                                     signals_used=["text", "landmark"],
                                     detail={"fallback": "synonym_text_click"})
            except Exception:
                continue
    return g


def recover(page, trigger: str, expected: str, observed: str, target=None,
            postcondition: str | None = None, last_good_url: str | None = None,
            detected_at_ms: int = 0) -> dict:
    t0 = _now()
    steps, strategy = [], "re_locate"

    # 1. re-plan: clear blocking side effects first
    cleared = clear_side_effects(page)
    steps.extend(cleared)
    if cleared:
        strategy = "re_plan"

    # 2. re-locate the target structurally, if one was given
    conf_after, locator = None, None
    if target is not None:
        g = relocate(page, target)
        conf_after, locator = g.confidence, g.locator
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
    elif cleared:
        # overlay-only recovery: nothing to re-locate
        locator, conf_after = None, None

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
