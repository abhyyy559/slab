"""Learner: explores Site A and Site B flows via WebCMD browser sessions and generates workflow command JSON."""
import datetime, json, os, pathlib, shutil, subprocess, time
from .executor import WebcmdSession
from .logger import log_action

WEBCMD_BIN = shutil.which("webcmd") or "webcmd"

def _record_sitemap_note(domain: str, text: str):
    try:
        subprocess.run([WEBCMD_BIN, "site", "note", "add", domain, "--text", text],
                       capture_output=True, text=True, check=False)
    except Exception:
        pass

def learn(goal: str, site: str = "site_a", out: str = "commands/phone_delivery_check.json",
          base: str = "http://127.0.0.1:8000", profile: str | None = None) -> dict:
    """Explore Site A and Site B with WebCMD and produce strategy command JSON."""
    t0 = time.time()
    session_name = f"sentry-learner-{int(t0 * 1000)}"
    print(f"[Learner] Starting WebCMD site exploration for goal: {goal or 'cross-site check'} (site={site})", flush=True)

    with WebcmdSession(name=session_name, profile=profile) as session:
        page = session.page
        # 2. Explore Site A
        url_a = f"{base}/site_a/search.html"
        print(f"[Learner] Exploring Site A at {url_a}...", flush=True)
        page.goto(url_a)
        page.wait_for_timeout(400)

        site_a_inspection = page.evaluate("""() => {
            const search = document.querySelector('[data-testid="search-box"]');
            const maxP = document.querySelector('[data-testid="max-price"]');
            const minR = document.querySelector('[data-testid="min-ram"]');
            const applyBtn = document.querySelector('[data-testid="apply-filter"]');
            const cards = [...document.querySelectorAll('[data-testid="product-card"]')].map(c => ({
                name: c.dataset.name,
                price: c.dataset.price,
                ram: c.dataset.ram
            }));
            return {
                title: document.title,
                has_search: !!search,
                search_label: search ? (search.getAttribute('aria-label') || search.placeholder || 'Search') : '',
                has_max_price: !!maxP,
                has_min_ram: !!minR,
                has_apply: !!applyBtn,
                apply_text: applyBtn ? applyBtn.innerText.trim() : 'Apply Filter',
                card_count: cards.length,
                sample_cards: cards.slice(0, 3)
            };
        }""")

        _record_sitemap_note(
            "voltkart.com",
            f"VoltKart /site_a/search.html observed: has_search={site_a_inspection.get('has_search')}, "
            f"search_label='{site_a_inspection.get('search_label')}', has_max_price={site_a_inspection.get('has_max_price')}, "
            f"has_min_ram={site_a_inspection.get('has_min_ram')}, has_apply={site_a_inspection.get('has_apply')}, "
            f"apply_text='{site_a_inspection.get('apply_text')}', card_count={site_a_inspection.get('card_count')}."
        )

        # 3. Explore Site B
        url_b = f"{base}/site_b/check.html"
        print(f"[Learner] Exploring Site B at {url_b}...", flush=True)
        page.goto(url_b)
        page.wait_for_timeout(400)

        site_b_inspection = page.evaluate("""() => {
            const pin = document.querySelector('[data-testid="pin-input"]');
            const btn = document.querySelector('[data-testid="check-button"]');
            const status = document.querySelector('[data-testid="delivery-status"]');
            return {
                title: document.title,
                has_pin: !!pin,
                has_button: !!btn,
                button_text: btn ? btn.innerText.trim() : 'Check Delivery',
                has_status: !!status
            };
        }""")

        _record_sitemap_note(
            "swiftship.com",
            f"SwiftShip /site_b/check.html observed: has_pin={site_b_inspection.get('has_pin')}, "
            f"has_button={site_b_inspection.get('has_button')}, button_text='{site_b_inspection.get('button_text')}', "
            f"has_status={site_b_inspection.get('has_status')}."
        )

        # 4. Synthesize structured template JSON
        template = [
            {
                "step": 1,
                "intent": "open_search",
                "url": "{{base}}/site_a/search.html",
                "precondition": "search_box_visible",
                "postcondition": "results_visible",
                "target": {
                    "selector": '[data-testid="search-box"]',
                    "role": "textbox",
                    "name": site_a_inspection.get("search_label", "Search phones"),
                    "text": "Search phones",
                    "landmark": "main"
                }
            },
            {
                "step": 2,
                "intent": "apply_filter",
                "params": {"max_price": "{{budget}}", "min_ram": "{{ram}}"},
                "precondition": "filters_visible",
                "postcondition": "results_filtered",
                "target": {
                    "selector": '[data-testid="apply-filter"]',
                    "role": "button",
                    "name": site_a_inspection.get("apply_text", "Apply Filter"),
                    "text": site_a_inspection.get("apply_text", "Apply Filter"),
                    "landmark": "main"
                }
            },
            {
                "step": 3,
                "intent": "extract_cheapest",
                "postcondition": "product_selected",
                "target": {
                    "selector": '[data-testid="product-card"]',
                    "role": "",
                    "name": "",
                    "text": "Rs",
                    "landmark": '[data-testid="results"]'
                }
            },
            {
                "step": 4,
                "intent": "check_delivery",
                "url": "{{base}}/site_b/check.html",
                "precondition": "pin_input_visible",
                "postcondition": "delivery_status_visible",
                "target": {
                    "selector": '[data-testid="check-button"]',
                    "role": "button",
                    "name": site_b_inspection.get("button_text", "Check Delivery"),
                    "text": site_b_inspection.get("button_text", "Check Delivery"),
                    "landmark": "main"
                },
                "irreversible": True
            }
        ]

        workflow_data = {
            "workflow": "phone_delivery_check",
            "version": 1,
            "created": datetime.datetime.now().isoformat(),
            "site": site,
            "template": template,
            "params": {"budget": "20000", "ram": "8", "pin": "500001", "base": base},
            "preconditions": ["login_not_required", "no_captcha"],
            "negative_case": {"condition": "no_results", "action": "ABSTAIN", "constraint": "max_price AND min_ram"},
            "regression_tests": ["variant_1", "variant_2", "variant_3", "variant_perturbed"],
            "provenance": {
                "learned_by": "webcmd-learner",
                "learned_at": datetime.datetime.now().isoformat(),
                "confidence_at_learn": 0.95,
                "webcmd_version": "0.8.4",
                "site_a_inspection": site_a_inspection,
                "site_b_inspection": site_b_inspection
            }
        }

        out_path = pathlib.Path(out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(workflow_data, indent=2), encoding="utf-8")
        elapsed_ms = int((time.time() - t0) * 1000)

        log_action(event="LEARNER_COMPLETED", workflow=workflow_data["workflow"],
                   version=workflow_data["version"], path=str(out_path),
                   duration_ms=elapsed_ms, steps=len(template))

        print(f"[Learner] Successfully generated {out} in {elapsed_ms}ms with {len(template)} steps.", flush=True)
        return workflow_data

def learn_stub(goal: str, site: str, out: str):
    return learn(goal=goal, site=site, out=out)

