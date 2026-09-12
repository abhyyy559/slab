"""Live-site probe (v5 family): read-only cheapest-in-stock extraction on an
arbitrary public URL. NEVER logs in, never solves CAPTCHAs, never retries a
block. Any wall -> ABSTAIN with a named reason. ToS: probe only sites whose
terms permit automation (practice sandboxes); Amazon/Flipkart/Facebook-style
targets ABSTAIN at the wall instead of bypassing it.
"""
import json
import pathlib
import time

from agent.evidence import make_claim
from agent.grounder import Target, ground

BLOCK_MARKERS = {
    "auth_wall": ("log in", "sign in", "login required", "account required"),
    "captcha": ("captcha", "recaptcha", "verify you are human", "i am not a robot"),
    "bot_block": ("cloudflare", "akamai", "access denied", "forbidden", "request blocked"),
    "rate_limit": ("too many requests", "rate limit", "429"),
}


def classify_block(html: str, status: int | None = None) -> str | None:
    """Pure classifier (unit-tested). Returns a reason or None if the page is readable."""
    if status in (401, 403):
        return "auth_wall"
    if status == 429:
        return "rate_limit"
    low = (html or "").lower()
    for reason, markers in BLOCK_MARKERS.items():
        if any(m in low for m in markers):
            return reason
    return None


def main(site_url: str = "https://books.toscrape.com/", budget: float = 20.0) -> dict:
    from playwright.sync_api import sync_playwright
    t0 = time.time()
    out = {"site": site_url, "pattern": "cheapest-in-stock-under-budget", "ts": int(t0 * 1000)}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            try:
                page.goto(site_url, wait_until="domcontentloaded", timeout=20000)
            except Exception as e:
                out.update(status="ABSTAIN", failed_constraint="unreachable",
                           reason=f"{type(e).__name__}")
                return out
            page.wait_for_timeout(1500)
            html = page.content()
            blocked = classify_block(html)
            if blocked:
                out.update(status="ABSTAIN", failed_constraint=blocked,
                           reason="wall detected; will not bypass")
                return out
            g = ground(page, Target(selector="article", role="link", name="",
                                    text="in stock", landmark="main"))
            cards = page.evaluate("""() => [...document.querySelectorAll(
                'article.product_pod, .quote, [data-product], .product')].slice(0, 60).map(a => ({
                    title: ((a.querySelector('h3 a') || {}).title)
                        || ((a.querySelector('.text') || {}).textContent) || '',
                    price: ((a.querySelector('.price_color, .price') || {}).textContent) || '',
                    stock: a.innerText || '' }))""")
            rows = []
            for c in cards:
                import re
                m = re.search(r"[£$₹]?\s*([\d,]+\.\d+|\d+)", c["price"] or "")
                if not m:
                    continue
                try:
                    price = float(m.group(1).replace(",", ""))
                except ValueError:
                    continue
                rows.append({"title": (c["title"] or "").strip()[:120], "price": price})
            if not rows:
                out.update(status="ABSTAIN", failed_constraint="no_product_cards",
                           cards_seen=len(cards), ground_confidence=g.confidence)
                return out
            eligible = [r for r in rows if r["price"] <= budget]
            if not eligible:
                out.update(status="ABSTAIN", failed_constraint="budget_unmet",
                           cheapest_seen=min(rows, key=lambda r: r["price"]))
                return out
            cheapest = min(eligible, key=lambda r: r["price"])
            snippet = next((s for s in [cheapest["title"], str(cheapest["price"])]
                            if s and s in html), cheapest["title"])
            out.update(status="pass", cheapest=cheapest, visible_cards=len(rows),
                       ground_confidence=g.confidence, signals=g.signals_used,
                       evidence=make_claim(
                           f"Cheapest under {budget}: {cheapest['title']} at {cheapest['price']}",
                           site_url, html, snippet, action_log_ref=0),
                       elapsed_ms=int((time.time() - t0) * 1000))
            return out
        finally:
            browser.close()


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--site-url", default="https://books.toscrape.com/")
    ap.add_argument("--budget", type=float, default=20.0)
    a = ap.parse_args()
    result = main(a.site_url, a.budget)
    pathlib.Path("logs/transfer.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
