"""Replayer: executes command JSON against live mocks. Detect -> recover -> verify on every step."""
import json, pathlib, time
from .grounder import ground, Target, TAU
from .executor import do_action, state_hash
from .logger import log_action, log_hash, log_recovery
from .evidence import make_claim
from .constraints import check as check_constraints
from .approval import require_approval, require_approval_browser
from . import detector as det
from . import recovery as rec

def load_command(path: str) -> dict:
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

def _url(base: str, path: str, perturb: str | None) -> str:
    u = f"{base}{path}"
    return u + (f"?perturb={perturb}" if perturb else "")

def _emit_hash(seq: int, before: str, action: str, after: str):
    h = state_hash(action)
    log_hash(seq=seq, before=before, action_hash=h, after=after)
    print(f"HASH seq={seq} {after[:12]}... ({action})", flush=True)

def _record(stats: dict, r: dict, detected_at_ms: int):
    """Count genuine extra steps (dismissals, backtracks, retries — not re-grounds)."""
    n = sum(1 for s in r["steps"] if s.startswith("dismissed:") or s.startswith("backtracked:"))
    stats["extra"].append(n)
    stats["heal"].append(r["time_to_heal_ms"])
    stats["detect"].append(r["time_to_detect_ms"])
    log_recovery(trigger=r["trigger"], expected=r["expected"], observed=r["observed"],
                 detected_at_ms=detected_at_ms, time_to_detect_ms=r["time_to_detect_ms"],
                 strategy=r["strategy"], steps=r["steps"],
                 time_to_heal_ms=r["time_to_heal_ms"], verified=r["verified"],
                 confidence_after=r["confidence_after"])

def _handle_scan(page, changes: list, last_good: str | None, stats: dict) -> dict | None:
    """Clear blocking side effects found by scan. Returns recovery record (or None if clean)."""
    if not changes:
        return None
    t_det = changes[0].timestamp_ms
    r = rec.recover(page, trigger="+".join(c.type for c in changes),
                    expected="clean_page", observed="+".join(c.observed for c in changes),
                    postcondition=None, last_good_url=last_good, detected_at_ms=t_det)
    _record(stats, r, t_det)
    return r

def _ground_or_recover(page, target: Target, step: int, name: str, seq: int, last_good: str | None, stats: dict):
    t0 = int(time.time() * 1000)
    g = ground(page, target)
    changes = det.scan(page)
    if changes:
        _handle_scan(page, changes, last_good, stats)
        g = ground(page, target)  # re-ground after clearing overlays
    log_action(seq=seq, step=step, action="ground", target=name, confidence=g.confidence,
               signals=g.signals_used, state_before_hash="", state_after_hash="", duration_ms=0,
               result="ok" if g.confidence >= TAU and g.locator is not None else "LOW_CONFIDENCE_PAUSE")
    if g.confidence < TAU or g.locator is None:
        t_det = int(time.time() * 1000)
        r = rec.recover(page, trigger="low_confidence", expected=name,
                        observed=f"conf={g.confidence}", target=target,
                        last_good_url=last_good, detected_at_ms=t_det)
        _record(stats, r, t_det)  # re-ground itself costs 0; backtrack (if any) counted in _record
        if r["locator"] is None or (r["confidence_after"] or 0) < TAU:
            return None, r
        from .grounder import Grounding
        g = Grounding(locator=r["locator"], confidence=r["confidence_after"],
                      signals_used=["recovered"], detail={"strategy": r["strategy"]})
    return g, None

def run_variant(variant: int = 1, base: str = "http://127.0.0.1:8000",
                command_path: str = "commands/phone_delivery_check.json",
                goal: str = "", perturb: str | None = None,
                auto_approve: bool = True, headless: bool = True,
                budget: int | None = None, ram: int | None = None,
                pin: str | None = None) -> dict:
    from playwright.sync_api import sync_playwright
    cmd = load_command(command_path)
    params = dict(cmd.get("params", {}))
    params["base"] = base
    if budget is not None:
        params["budget"] = str(budget)
    if ram is not None:
        params["ram"] = str(ram)
    if pin is not None:
        params["pin"] = str(pin)
    budget, ram, pin = int(params["budget"]), int(params["ram"]), str(params["pin"])
    seq = 0
    stats = {"extra": [], "heal": [], "detect": []}
    evidences, last_good = [], None
    t_start = time.time()
    if perturb:
        log_action(event="PERTURB_INJECTED", target=perturb, seq=seq)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        page = browser.new_page()
        try:
            # Step 1: open search
            url1 = _url(base, "/site_a/search.html", perturb)
            r = do_action(page, "goto", None, url1)
            last_good = url1
            seq += 1
            log_action(seq=seq, step=1, action="goto", target="search_page", confidence=1.0,
                       signals=["selector"], state_before_hash="", state_after_hash=r["state_after_hash"],
                       duration_ms=r["duration_ms"], result=r["result"], url=url1)
            _emit_hash(seq, "", "goto:search", r["state_after_hash"])
            page.wait_for_timeout(700 if perturb else 300)  # let chaos.js apply
            t = Target(selector='[data-testid="search-box"]', role="textbox", name="Search phones", text="Search phones", landmark="main")
            g, rec_info = _ground_or_recover(page, t, 1, "search_box", seq, last_good, stats)
            if g is None:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE search_box unrecoverable"}
            # Step 2: apply filter
            page.fill('[data-testid="max-price"]', str(budget))
            page.fill('[data-testid="min-ram"]', str(ram))
            t2 = Target(selector='[data-testid="apply-filter"]', role="button", name="Apply Filter", text="Apply Filter", landmark="main")
            g2, rec2 = _ground_or_recover(page, t2, 2, "filter_button", seq, last_good, stats)
            if g2 is None:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE filter_button unrecoverable"}
            r2 = do_action(page, "click", g2.locator)
            seq += 1
            log_action(seq=seq, step=2, action="click", target="filter_button", confidence=g2.confidence,
                       signals=g2.signals_used, state_before_hash=r2["state_before_hash"], state_after_hash=r2["state_after_hash"],
                       duration_ms=r2["duration_ms"], result=r2["result"])
            _emit_hash(seq, r2["state_before_hash"], "click:filter", r2["state_after_hash"])
            ok2, obs2 = det.check_post(page, "results_filtered")
            if not ok2:  # throttle delay or intercepted click: wait, clear overlays, retry once
                t_det = int(time.time() * 1000)
                page.wait_for_timeout(3000)
                rr = rec.recover(page, trigger="postcondition_failed", expected="results_filtered",
                                 observed=obs2, target=t2, postcondition="results_filtered",
                                 last_good_url=last_good, detected_at_ms=t_det)
                _record(stats, rr, t_det)
                if not rr["verified"]:
                    if rr["locator"] is not None:
                        stats["extra"].append(1)  # retry click is a genuine extra step
                        r2b = do_action(page, "click", rr["locator"])
                        seq += 1
                        _emit_hash(seq, r2b["state_before_hash"], "click:filter:retry", r2b["state_after_hash"])
                        page.wait_for_timeout(3000)
                    ok2, obs2 = det.check_post(page, "results_filtered")
            # Step 3: extract cheapest meeting constraints (B must confirm within 3 days -> loop)
            cards = page.evaluate("""() => [...document.querySelectorAll('[data-testid="product-card"], #chaos-results > article')]
                .filter(c => c.style.display !== 'none')
                .map(c => ({name: c.dataset.name, price: parseInt(c.dataset.price,10), ram: parseInt(c.dataset.ram,10),
                            text: c.innerText}))""")
            eligible = [c for c in cards if c["price"] <= budget and c["ram"] >= ram]
            if not eligible:
                log_action(event="ABSTAIN", reason="no_results", constraint="max_price AND min_ram")
                return {"status": "ABSTAIN", "failed_constraint": "max_price AND min_ram", "cards": cards}
            cheapest = min(eligible, key=lambda c: c["price"])
            html_a = page.content()
            cand = [cheapest["text"].split("\n")[0], f"Rs {cheapest['price']}"]
            snippet = next((s for s in cand if s and s in html_a), cheapest["name"])
            ev1 = make_claim(f"Cheapest phone >= {ram}GB under Rs {budget} is {cheapest['name']} at Rs {cheapest['price']}",
                             url1, html_a, snippet, action_log_ref=seq)
            evidences.append(ev1)
            log_action(seq=seq, step=3, action="extract", target="cheapest", confidence=0.95,
                       signals=["selector", "text"], state_before_hash="", state_after_hash="",
                       duration_ms=0, result=f"ok:{cheapest['name']}:{cheapest['price']}")
            # Step 4: site B delivery check within 3 days (approval gate: submit-like)
            url2 = _url(base, "/site_b/check.html", perturb)
            r3 = do_action(page, "goto", None, url2)
            last_good = url2
            seq += 1
            log_action(seq=seq, step=4, action="goto", target="delivery_page", confidence=1.0,
                       signals=["selector"], state_before_hash=r3["state_before_hash"], state_after_hash=r3["state_after_hash"],
                       duration_ms=r3["duration_ms"], result=r3["result"], url=url2)
            _emit_hash(seq, r3["state_before_hash"], "goto:delivery", r3["state_after_hash"])
            page.wait_for_timeout(700 if perturb else 300)
            page.fill('[data-testid="pin-input"]', pin)
            t4 = Target(selector='[data-testid="check-button"]', role="button", name="Check Delivery", text="Check Delivery", landmark="main")
            g4, rec4 = _ground_or_recover(page, t4, 4, "check_button", seq, last_good, stats)
            if g4 is None:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE check_button unrecoverable"}
            if auto_approve:
                ok = require_approval(url2, "check_delivery_submit", {"pin": pin}, auto="grant")
            else:
                ok = require_approval_browser(page, url2, "check_delivery_submit", {"pin": pin})
            if not ok:
                return {"status": "ABSTAIN", "reason": "APPROVAL_DENIED"}
            r4 = do_action(page, "click", g4.locator)
            seq += 1
            log_action(seq=seq, step=4, action="click", target="check_button", confidence=g4.confidence,
                       signals=g4.signals_used, state_before_hash=r4["state_before_hash"], state_after_hash=r4["state_after_hash"],
                       duration_ms=r4["duration_ms"], result=r4["result"])
            _emit_hash(seq, r4["state_before_hash"], "click:check", r4["state_after_hash"])
            page.wait_for_timeout(3000 if perturb else 400)
            ok4, obs4 = det.check_post(page, "delivery_status_visible")
            if not ok4:
                t_det = int(time.time() * 1000)
                rr = rec.recover(page, trigger="postcondition_failed", expected="delivery_status_visible",
                                 observed=obs4, target=t4, postcondition="delivery_status_visible",
                                 last_good_url=last_good, detected_at_ms=t_det)
                _record(stats, rr, t_det)
                ok4, obs4 = det.check_post(page, "delivery_status_visible")
            status_text = page.inner_text('[data-testid="delivery-status"]') or ""
            html_b = page.content()
            snippet_b = status_text.strip().split("\n")[0] if status_text.strip() else "delivery-status"
            ev2 = make_claim(f"Site B confirms deliverable within 3 days to PIN {pin}: {status_text.strip()}", url2, html_b, snippet_b, action_log_ref=seq)
            evidences.append(ev2)
            within_days = "2-3 days" in status_text
            verdict = check_constraints({"max_price": cheapest["price"] <= budget,
                                         "min_ram": cheapest["ram"] >= ram,
                                         "b_confirms_deliverable_3d": within_days})
            total_extra = sum(stats["extra"])
            heal = stats["heal"]
            dtct = stats["detect"]
            out = {"status": "pass" if verdict["decision"] == "proceed" else "ABSTAIN",
                   "cheapest": cheapest, "delivery": status_text.strip(),
                   "evidence": evidences, "constraints": verdict,
                   "extra_steps": total_extra,
                   "avg_time_to_heal_ms": (sum(heal) // len(heal)) if heal else 0,
                   "avg_time_to_detect_ms": (sum(dtct) // len(dtct)) if dtct else 0,
                   "elapsed_ms": int((time.time() - t_start) * 1000),
                   "variant": variant, "perturb": perturb}
            _record_trial(variant, perturb, out["status"] == "pass", seq, total_extra, out["avg_time_to_heal_ms"])
            return out
        finally:
            browser.close()

def _record_trial(variant, perturb, success: bool, steps: int, extra: int, heal_ms: int):
    try:
        p = pathlib.Path("logs/metrics.json")
        m = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        curve = m.get("learning_curve", [])
        curve.append({"trial": len(curve) + 1, "variant": variant, "perturb": perturb,
                      "success": success, "steps": steps, "extra_steps": extra, "heal_ms": heal_ms})
        m["learning_curve"] = curve
        p.write_text(json.dumps(m, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"metrics write failed: {e}")
