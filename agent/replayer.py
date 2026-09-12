"""Replayer: executes command JSON against live mocks. Detect -> recover -> verify on every step."""
import json, pathlib, time
from .grounder import ground, Target, TAU
from .executor import do_action, state_hash
from .logger import log_action, log_hash, log_recovery, stage
from .evidence import make_claim
from .constraints import check as check_constraints, deliverable_within_days
from .approval import require_approval, require_approval_browser
from . import detector as det
from . import recovery as rec
from . import browser as bsession

def load_command(path: str) -> dict:
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

def _url(base: str, path: str, perturb: str | None) -> str:
    u = f"{base}{path}"
    return u + (f"?perturb={perturb}" if perturb else "")

def _emit_hash(seq: int, before: str, action: str, after: str):
    h = state_hash(action)
    log_hash(seq=seq, before=before, action_hash=h, after=after)
    stage("step", f"\u2713 step action: {action}")
    stage("hash", f"HASH seq={seq} {after[:12]}... ({action})")

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
    stage("recovery", f"\u26a0 RECOVERY: {r['trigger']} -> {r['strategy']}")
    stage("healed", f"\u2713 HEALED in {r['time_to_heal_ms']}ms (verified={r['verified']})")

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
                pin: str | None = None,
                slow_mo: int | None = None, keep_open_ms: int | None = None,
                raise_window: bool = True, channel: str | None = None) -> dict:
    from playwright.sync_api import sync_playwright
    from .planner import plan_goal
    cmd = load_command(command_path)
    workflow = cmd.get("workflow") or pathlib.Path(command_path).stem

    # Precedence: explicit call arguments > parameters read from the goal > command defaults.
    plan = plan_goal(goal, workflow)
    log_action(event="PLAN", goal=goal, workflow=workflow, supported=plan.supported,
               params=plan.params, unsupported=plan.unsupported, notes=plan.notes,
               steps=[s.intent for s in plan.steps])
    if not plan.supported:
        reason = "; ".join(plan.unsupported)
        log_action(event="ABSTAIN", reason="unsupported_goal", detail=reason)
        return {"status": "ABSTAIN", "failed_constraint": "unsupported_goal", "reason": reason,
                "constraints": check_constraints({"goal_maps_to_known_workflow": False}),
                "plan": plan.to_dict(), "variant": variant, "perturb": perturb}

    params = dict(cmd.get("params", {}))
    params["base"] = base
    for key in ("budget", "ram", "pin"):
        if plan.params.get(key) is not None:
            params[key] = str(plan.params[key])
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
    _write_live({"run_id": f"v{variant}/{perturb or 'clean'}", "step": "0/4",
                 "status": "running", "extra_steps": 0,
                 "detect_ms": 0, "heal_ms": 0, "elapsed_ms": 0})
    if perturb:
        log_action(event="PERTURB_INJECTED", target=perturb, seq=seq)
    # Headed runs are demonstrations: pick a legible slow_mo and hold the final
    # frame long enough to read unless the caller overrides them.
    if slow_mo is None:
        slow_mo = 250 if not headless else 0
    if keep_open_ms is None:
        keep_open_ms = 6000 if not headless else 0
    with sync_playwright() as pw:
        browser, context = bsession.launch_browser(
            pw, headless=headless, slow_mo=slow_mo, raise_window=raise_window, channel=channel)
        page = context.new_page()
        if not headless:
            bsession.focus_window(page, raise_window=raise_window)
            log_action(event="BROWSER_WINDOW", mode="headed", raised=raise_window,
                       slow_mo=slow_mo, keep_open_ms=keep_open_ms,
                       stage=bsession.describe_window())
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
            # Let the page settle: with judge-operated injection, chaos.js applies
            # its changes asynchronously ~600ms after load, so a fixed sleep races it.
            det.settle(page, quiet_ms=250, max_ms=1800 if perturb else 900)
            t = Target(selector='[data-testid="search-box"]', role="searchbox", name="Search phones",
                       text="Search phones", landmark="main", labels=["Search phones", "Search"])
            g, rec_info = _ground_or_recover(page, t, 1, "search_box", seq, last_good, stats)
            if g is None:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE search_box unrecoverable"}
            # Step 2: apply filter. Fill by structural label lookup so a stripped id
            # (perturb=strip) does not break the fill; fall back to the id selector.
            def _fill(selector: str, label: str, value: str):
                loc = None
                try:
                    cand = page.get_by_label(label)
                    if cand.count() >= 1:
                        loc = cand.first
                except Exception:
                    loc = None
                if loc is None:
                    loc = page.locator(selector).first
                try:
                    loc.fill(str(value), timeout=3000)
                    return True
                except Exception:
                    try:
                        page.fill(selector, str(value))
                        return True
                    except Exception:
                        return False

            _fill('[data-testid="max-price"]', "Max price", budget)
            _fill('[data-testid="min-ram"]', "Min RAM", ram)
            t2 = Target(selector='[data-testid="apply-filter"]', role="button", name="Apply Filter",
                        text="Apply Filter", landmark="main", labels=["Apply Filter", "Refine Results"])
            g2, rec2 = _ground_or_recover(page, t2, 2, "filter_button", seq, last_good, stats)
            if g2 is None:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE filter_button unrecoverable"}
            r2 = do_action(page, "click", g2.locator)
            seq += 1
            log_action(seq=seq, step=2, action="click", target="filter_button", confidence=g2.confidence,
                       signals=g2.signals_used, state_before_hash=r2["state_before_hash"], state_after_hash=r2["state_after_hash"],
                       duration_ms=r2["duration_ms"], result=r2["result"])
            _emit_hash(seq, r2["state_before_hash"], "click:filter", r2["state_after_hash"])
            ok2, obs2 = det.wait_for_post(page, "results_filtered", timeout_ms=6000)
            if not ok2:  # throttle delay or intercepted click: clear overlays, retry once
                t_det = int(time.time() * 1000)
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
                        ok2, obs2 = det.wait_for_post(page, "results_filtered", timeout_ms=6000)
            # Step 3: extract cheapest meeting constraints (B must confirm within 3 days -> loop).
            # Read from whichever results list is currently live: a chaos swap() re-renders the
            # list into a new container, and ab() hides every other card.
            cards = page.evaluate("""() => {
                const live = document.querySelector('#chaos-list-container')
                    || document.querySelector('[data-testid="results"]')
                    || document.querySelector('section[aria-label="Results"]') || document.body;
                return [...live.querySelectorAll('article')]
                    .filter(c => c.style.display !== 'none' && c.offsetParent !== null)
                    .map(c => {
                        const g = (n) => c.getAttribute('data-' + n) || c.getAttribute('data-' + n + '-m');
                        const h2 = c.querySelector('h2');
                        const priceTxt = (c.querySelector('.price') || {}).textContent || '';
                        return {
                            name: g('name') || (h2 ? h2.textContent.trim() : ''),
                            price: parseInt(g('price') || priceTxt.replace(/[^0-9]/g,''), 10),
                            ram: parseInt(g('ram') || (c.innerText.match(/(\\d+)\\s*GB\\s*RAM/) || [])[1], 10),
                            text: c.innerText
                        };
                    })
                    .filter(c => c.name && !isNaN(c.price));
            }""")
            eligible = [c for c in cards if c["price"] <= budget and c["ram"] >= ram]
            if not eligible:
                log_action(event="ABSTAIN", reason="no_results", constraint="max_price AND min_ram")
                return {"status": "ABSTAIN", "failed_constraint": "max_price AND min_ram",
                        "cards": cards, "plan": plan.to_dict(),
                        "effective_params": {"budget": budget, "ram": ram, "pin": pin},
                        "variant": variant, "perturb": perturb}
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
            # Step 4: site B delivery check per candidate (LOOP, not hop).
            # Approval covers the workflow's submit-like intent once, up front.
            from urllib.parse import quote as _quote

            def _site_b_url(product: str | None) -> str:
                q = []
                if perturb:
                    q.append(f"perturb={perturb}")
                if product:
                    q.append(f"product={_quote(product)}")
                return base + "/site_b/check.html" + ("?" + "&".join(q) if q else "")

            ranked = sorted(eligible, key=lambda c: c["price"])[:3]
            chosen, status_text, url2, attempts = None, "", _site_b_url(None), []
            for i, cand in enumerate(ranked):
                url2 = _site_b_url(cand["name"])
                r3 = do_action(page, "goto", None, url2)
                last_good = url2
                seq += 1
                log_action(seq=seq, step=4, action="goto", target="delivery_page", confidence=1.0,
                           signals=["selector"], state_before_hash=r3["state_before_hash"], state_after_hash=r3["state_after_hash"],
                           duration_ms=r3["duration_ms"], result=r3["result"], url=url2,
                           candidate=cand["name"], attempt=i + 1)
                _emit_hash(seq, r3["state_before_hash"], f"goto:delivery:{cand['name']}", r3["state_after_hash"])
                det.settle(page, quiet_ms=250, max_ms=1800 if perturb else 900)
                # Fill the PIN by structural label; id may have been stripped.
                _fill('[data-testid="pin-input"]', "PIN code", pin)
                t4 = Target(selector='[data-testid="check-button"]', role="button", name="Check Delivery",
                            text="Check Delivery", landmark="main", labels=["Check Delivery", "Verify Shipment"])
                g4, rec4 = _ground_or_recover(page, t4, 4, "check_button", seq, last_good, stats)
                if g4 is None:
                    return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE check_button unrecoverable"}
                if i == 0:
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
                           duration_ms=r4["duration_ms"], result=r4["result"], candidate=cand["name"])
                _emit_hash(seq, r4["state_before_hash"], "click:check", r4["state_after_hash"])
                page.wait_for_timeout(3000 if perturb else 400)
                ok4, obs4 = det.wait_for_post(page, "delivery_status_visible", timeout_ms=7000)
                if not ok4:
                    t_det = int(time.time() * 1000)
                    rr = rec.recover(page, trigger="postcondition_failed", expected="delivery_status_visible",
                                     observed=obs4, target=t4, postcondition="delivery_status_visible",
                                     last_good_url=last_good, detected_at_ms=t_det)
                    _record(stats, rr, t_det)
                    ok4, obs4 = det.check_post(page, "delivery_status_visible")
                # status read: prefer the resilient postcondition text; fall back to the id.
                status_text = obs4 if (ok4 and obs4 and not obs4.startswith(("delivery_status", "eval_"))) else ""
                if not status_text:
                    try:
                        status_text = page.inner_text('[data-testid="delivery-status"]') or ""
                    except Exception:
                        status_text = ""
                ok_deliv = deliverable_within_days(status_text)
                attempts.append({"candidate": cand["name"], "price": cand["price"],
                                 "deliverable": ok_deliv, "observed": status_text.strip()[:80]})
                log_action(seq=seq, step=4, action="delivery_verdict", target=cand["name"],
                           confidence=1.0, signals=["text"], state_before_hash="", state_after_hash="",
                           duration_ms=0, result=f"deliverable={ok_deliv}")
                if i > 0:
                    stats["extra"].append(1)  # fallback candidate = genuine extra step
                if ok_deliv:
                    chosen = cand
                    break
                log_action(event="LOOP_FALLBACK", reason=f"{cand['name']} not deliverable",
                           next="next-cheapest eligible")
            if chosen is None:
                log_action(event="ABSTAIN", reason="no_deliverable_candidate",
                           constraint="b_confirms_deliverable_3d", attempts=str(attempts))
                return {"status": "ABSTAIN", "failed_constraint": "b_confirms_deliverable_3d",
                        "attempts": attempts, "plan": plan.to_dict(),
                        "effective_params": {"budget": budget, "ram": ram, "pin": pin},
                        "variant": variant, "perturb": perturb}
            cheapest = chosen
            html_b = page.content()
            snippet_b = status_text.strip().split("\n")[0] if status_text.strip() else "delivery-status"
            ev2 = make_claim(f"Site B confirms deliverable within 3 days to PIN {pin}: {status_text.strip()}", url2, html_b, snippet_b, action_log_ref=seq)
            evidences.append(ev2)
            within_days = deliverable_within_days(status_text)
            verdict = check_constraints({"max_price": cheapest["price"] <= budget,
                                         "min_ram": cheapest["ram"] >= ram,
                                         "b_confirms_deliverable_3d": within_days})
            total_extra = sum(stats["extra"])
            heal = stats["heal"]
            dtct = stats["detect"]
            out = {"status": "pass" if verdict["decision"] == "proceed" else "ABSTAIN",
                   "cheapest": cheapest, "delivery": status_text.strip(),
                   "delivery_attempts": attempts,
                   "evidence": evidences, "constraints": verdict,
                   "plan": plan.to_dict(),
                   "effective_params": {"budget": budget, "ram": ram, "pin": pin},
                   "extra_steps": total_extra,
                   "avg_time_to_heal_ms": (sum(heal) // len(heal)) if heal else 0,
                   "avg_time_to_detect_ms": (sum(dtct) // len(dtct)) if dtct else 0,
                   "elapsed_ms": int((time.time() - t_start) * 1000),
                   "variant": variant, "perturb": perturb}
            _record_trial(variant, perturb, out["status"] == "pass", seq, total_extra, out["avg_time_to_heal_ms"])
            _write_live({"run_id": f"v{variant}/{perturb or 'clean'}", "step": "4/4",
                         "status": out["status"], "extra_steps": total_extra,
                         "detect_ms": out["avg_time_to_detect_ms"],
                         "heal_ms": out["avg_time_to_heal_ms"],
                         "elapsed_ms": out["elapsed_ms"]})
            stage("metric", f"METRIC detect={out['avg_time_to_detect_ms']}ms heal={out['avg_time_to_heal_ms']}ms "
                            f"extra={total_extra} status={out['status']}")
            return out
        finally:
            # Hold the final frame on screen so a headed run is watchable, then
            # close. Guarded: a demo must never fail on the way out.
            try:
                if not headless and keep_open_ms:
                    if raise_window:
                        bsession.focus_window(page, raise_window=True)
                    bsession.hold_open(keep_open_ms, keep_foreground=raise_window)
            except Exception:
                pass
            try:
                context.close()
            except Exception:
                pass
            browser.close()

def _write_live(state: dict):
    """Live banner state for the metrics page. Best-effort; never fails a run."""
    try:
        state["ts"] = int(time.time() * 1000)
        pathlib.Path("logs/live.json").write_text(json.dumps(state), encoding="utf-8")
    except Exception:
        pass

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
