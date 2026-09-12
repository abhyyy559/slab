"""Replayer: executes command JSON against live mocks. Variant 1 end-to-end."""
import json, pathlib, time
from .grounder import ground, Target, TAU
from .executor import do_action, state_hash
from .logger import log_action, log_hash
from .evidence import make_claim
from .constraints import check as check_constraints
from .approval import require_approval, require_approval_browser

def load_command(path: str) -> dict:
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))

def run_variant(variant: int = 1, base: str = "http://127.0.0.1:8000",
                command_path: str = "commands/phone_delivery_check.json",
                goal: str = "", perturb: str | None = None,
                auto_approve: bool = True, headless: bool = True) -> dict:
    from playwright.sync_api import sync_playwright
    cmd = load_command(command_path)
    params = dict(cmd.get("params", {}))
    params["base"] = base
    budget, ram, pin = int(params["budget"]), int(params["ram"]), str(params["pin"])
    seq = 0
    evidences = []
    t_start = time.time()
    if perturb:
        log_action(event="PERTURB_INJECTED", target=perturb, seq=seq)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        page = browser.new_page()
        try:
            # Step 1: open search
            url1 = f"{base}/site_a/search.html"
            r = do_action(page, "goto", None, url1)
            seq += 1
            log_action(seq=seq, step=1, action="goto", target="search_page", confidence=1.0,
                       signals=["selector"], state_before_hash="", state_after_hash=r["state_after_hash"],
                       duration_ms=r["duration_ms"], result=r["result"], url=url1)
            log_hash(seq=seq, before="", action_hash=state_hash("goto"+url1), after=r["state_after_hash"])
            t = Target(selector='[data-testid="search-box"]', role="textbox", name="Search phones", text="Search phones", landmark="main")
            g = ground(page, t)
            log_action(seq=seq, step=1, action="ground", target="search_box", confidence=g.confidence,
                       signals=g.signals_used, state_before_hash=r["state_after_hash"], state_after_hash=r["state_after_hash"],
                       duration_ms=0, result="ok" if g.confidence >= TAU else "LOW_CONFIDENCE_PAUSE")
            if g.confidence < TAU:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE search_box", "confidence": g.confidence}
            # Step 2: apply filter
            page.fill('[data-testid="max-price"]', str(budget))
            page.fill('[data-testid="min-ram"]', str(ram))
            t2 = Target(selector='[data-testid="apply-filter"]', role="button", name="Apply Filter", text="Apply Filter", landmark="main")
            g2 = ground(page, t2)
            log_action(seq=seq, step=2, action="ground", target="filter_button", confidence=g2.confidence,
                       signals=g2.signals_used, state_before_hash="", state_after_hash="", duration_ms=0,
                       result="ok" if g2.confidence >= TAU else "LOW_CONFIDENCE_PAUSE")
            if g2.confidence < TAU or g2.locator is None:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE filter_button", "confidence": g2.confidence}
            r2 = do_action(page, "click", g2.locator)
            seq += 1
            log_action(seq=seq, step=2, action="click", target="filter_button", confidence=g2.confidence,
                       signals=g2.signals_used, state_before_hash=r2["state_before_hash"], state_after_hash=r2["state_after_hash"],
                       duration_ms=r2["duration_ms"], result=r2["result"])
            log_hash(seq=seq, before=r2["state_before_hash"], action_hash=state_hash("click:filter"), after=r2["state_after_hash"])
            page.wait_for_timeout(400)
            # Step 3: extract cheapest meeting constraints
            cards = page.evaluate("""() => [...document.querySelectorAll('[data-testid="product-card"]')]
                .filter(c => c.style.display !== 'none')
                .map(c => ({name: c.dataset.name, price: parseInt(c.dataset.price,10), ram: parseInt(c.dataset.ram,10),
                            text: c.innerText}))""")
            eligible = [c for c in cards if c["price"] <= budget and c["ram"] >= ram]
            if not eligible:
                html = page.content()
                log_action(event="ABSTAIN", reason="no_results", constraint="max_price AND min_ram")
                return {"status": "ABSTAIN", "failed_constraint": "max_price AND min_ram", "cards": cards}
            cheapest = min(eligible, key=lambda c: c["price"])
            html_a = page.content()
            snippet_a = f"Rs {cheapest['price']:,}".replace(",", ",")
            # find verbatim price snippet robustly
            cand = [cheapest["text"].split("\n")[0], f"Rs {cheapest['price']}"]
            snippet = next((s for s in cand if s and s in html_a), cheapest["name"])
            ev1 = make_claim(f"Cheapest phone >= {ram}GB under Rs {budget} is {cheapest['name']} at Rs {cheapest['price']}",
                             url1, html_a, snippet, action_log_ref=seq)
            evidences.append(ev1)
            log_action(seq=seq, step=3, action="extract", target="cheapest", confidence=0.95,
                       signals=["selector", "text"], state_before_hash="", state_after_hash="",
                       duration_ms=0, result=f"ok:{cheapest['name']}:{cheapest['price']}")
            # Step 4: site B delivery check (approval gate: submit-like)
            url2 = f"{base}/site_b/check.html"
            r3 = do_action(page, "goto", None, url2)
            seq += 1
            log_action(seq=seq, step=4, action="goto", target="delivery_page", confidence=1.0,
                       signals=["selector"], state_before_hash=r3["state_before_hash"], state_after_hash=r3["state_after_hash"],
                       duration_ms=r3["duration_ms"], result=r3["result"], url=url2)
            page.fill('[data-testid="pin-input"]', pin)
            t4 = Target(selector='[data-testid="check-button"]', role="button", name="Check Delivery", text="Check Delivery", landmark="main")
            g4 = ground(page, t4)
            log_action(seq=seq, step=4, action="ground", target="check_button", confidence=g4.confidence,
                       signals=g4.signals_used, state_before_hash="", state_after_hash="", duration_ms=0,
                       result="ok" if g4.confidence >= TAU else "LOW_CONFIDENCE_PAUSE")
            if g4.confidence < TAU or g4.locator is None:
                return {"status": "ABSTAIN", "reason": "LOW_CONFIDENCE check_button", "confidence": g4.confidence}
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
            log_hash(seq=seq, before=r4["state_before_hash"], action_hash=state_hash("click:check"), after=r4["state_after_hash"])
            page.wait_for_timeout(400)
            status_text = page.inner_text('[data-testid="delivery-status"]') or ""
            html_b = page.content()
            snippet_b = status_text.strip().split("\n")[0] if status_text.strip() else "delivery-status"
            ev2 = make_claim(f"Delivery to PIN {pin}: {status_text.strip()}", url2, html_b, snippet_b, action_log_ref=seq)
            evidences.append(ev2)
            verdict = check_constraints({"max_price": cheapest["price"] <= budget,
                                         "min_ram": cheapest["ram"] >= ram,
                                         "delivery_pin_500001": "available" in status_text.lower()})
            out = {"status": "pass" if verdict["decision"] == "proceed" else "ABSTAIN",
                   "cheapest": cheapest, "delivery": status_text.strip(),
                   "evidence": evidences, "constraints": verdict,
                   "elapsed_ms": int((time.time() - t_start) * 1000), "variant": variant}
            return out
        finally:
            browser.close()
