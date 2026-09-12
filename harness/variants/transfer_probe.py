"""v5 credibility probe: same-family transfer to a real site we didn't write.

Pattern transferred: cheapest in-stock item under budget + extractive evidence.
Read-only, single page, low rate. books.toscrape.com is an explicit scrape-test
sandbox; no robots.txt published (checked 2026-09-12). Result -> logs/transfer.json.
"""
import json
import pathlib
import time

from agent.evidence import make_claim
from agent.grounder import Target, ground

SITE = "https://books.toscrape.com/"
BUDGET_GBP = 20.0

def main() -> dict:
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    out = {"site": SITE, "pattern": "cheapest-in-stock-under-budget", "ts": int(t0 * 1000)}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(SITE, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(1500)
            # Same grounder as the mock runs: re-ground by role+text on unseen DOM.
            g = ground(page, Target(selector=".product_pod", role="link",
                                    name="", text="In stock", landmark="section"))
            cards = page.evaluate("""() => [...document.querySelectorAll('article.product_pod')].map(a => ({
                title: (a.querySelector('h3 a') || {}).title || '',
                price: (a.querySelector('.price_color') || {}).textContent || '',
                stock: (a.querySelector('.instock') || {}).textContent || '' }))""")
            rows = []
            for c in cards:
                try:
                    price = float(c["price"].replace("£", "").strip())
                except ValueError:
                    continue
                if "in stock" in c["stock"].lower():
                    rows.append({"title": c["title"], "price": price})
            eligible = [r for r in rows if r["price"] <= BUDGET_GBP]
            out["ground_confidence"] = g.confidence
            out["signals"] = g.signals_used
            if not eligible:
                out.update(status="ABSTAIN", failed_constraint="budget_gbp_20",
                           visible_cards=len(rows))
                return out
            cheapest = min(eligible, key=lambda r: r["price"])
            html = page.content()
            snippet = next((s for s in [cheapest["title"], f"£{cheapest['price']}"] if s in html),
                           cheapest["title"])
            out.update(status="pass", cheapest=cheapest, visible_cards=len(rows),
                       evidence=make_claim(
                           f"Cheapest in-stock book under £{BUDGET_GBP}: "
                           f"{cheapest['title']} at £{cheapest['price']}",
                           SITE, html, snippet, action_log_ref=0),
                       elapsed_ms=int((time.time() - t0) * 1000))
            return out
        finally:
            browser.close()

if __name__ == "__main__":
    result = main()
    p = pathlib.Path("logs/transfer.json")
    p.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("status", "cheapest", "visible_cards",
                                            "ground_confidence", "elapsed_ms") if k in result},
                     indent=2))
