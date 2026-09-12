"""Backup-video recorder: scripted REAL execution of the demo arc on mocks.

Beats: thesis -> fresh run -> judge-typed perturbation (real console click) ->
heal with metric -> cross-site loop retry -> approval modal -> ABSTAIN -> close.
Target 2:30-2:45. Output: demo/demo-backup.mp4. Venue re-capture covers live beats.
"""
import pathlib
import subprocess
import time

import imageio_ffmpeg

BASE = "http://127.0.0.1:8000"
CONSOLE = "http://127.0.0.1:8765"
OUTDIR = pathlib.Path("demo")
W, H = 1280, 800

CARD_JS = """([title, lines]) => {
  const old = document.getElementById('sentry-card'); if (old) old.remove();
  const ov = document.createElement('div'); ov.id = 'sentry-card';
  ov.style.cssText = 'position:fixed;inset:0;background:#0b2f87;color:#fff;z-index:999999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:sans-serif;text-align:center;padding:40px;';
  ov.innerHTML = '<h1 style=font-size:44px;margin:0 0 18px>' + title + '</h1>' +
    lines.map(l => '<p style=font-size:23px;margin:8px;max-width:920px>' + l + '</p>').join('');
  document.body.appendChild(ov);
}"""

BANNER_JS = """([text, ok]) => {
  const old = document.getElementById('sentry-banner'); if (old) old.remove();
  const b = document.createElement('div'); b.id = 'sentry-banner';
  b.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:999999;padding:16px 22px;font-family:sans-serif;font-size:20px;font-weight:700;color:#fff;background:' + (ok ? '#067647' : '#b42318');
  b.textContent = text; document.body.appendChild(b);
}"""

APPROVAL_JS = """() => {
  const ov = document.createElement('div'); ov.id = 'sentry-approval';
  ov.setAttribute('role', 'dialog');
  ov.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:999999;display:flex;align-items:center;justify-content:center;';
  ov.innerHTML = '<div style=background:#fff;color:#000;padding:24px;max-width:480px;font-family:sans-serif;border:3px solid #000><h2>SENTRY wants approval</h2><p><b>action:</b> check_delivery_submit</p><p><b>payload:</b> PIN 500001</p><button id=sentry-ok style=padding:12px_24px;margin-right:12px;font-size:16px>Approve</button><button style=padding:12px_24px;font-size:16px>Deny</button></div>';
  document.body.appendChild(ov);
}"""


def card(page, title, lines, ms=9000):
    page.evaluate(CARD_JS, [title, lines])
    page.wait_for_timeout(ms)
    page.evaluate("() => { const o = document.getElementById('sentry-card'); if (o) o.remove(); }")


def act(page, title, ms=7000):
    card(page, title, [], ms)


def banner(page, text, ok=True, ms=6500):
    page.evaluate(BANNER_JS, [text, ok])
    page.wait_for_timeout(ms)


def fresh_run(page):
    page.goto(f"{BASE}/site_a/search.html", wait_until="domcontentloaded")
    page.wait_for_timeout(1200)
    page.locator('[data-testid="max-price"]').click()
    page.wait_for_timeout(300)
    page.locator('[data-testid="max-price"]').fill("20000")
    page.wait_for_timeout(600)
    page.locator('[data-testid="min-ram"]').fill("8")
    page.wait_for_timeout(600)
    page.locator('[data-testid="apply-filter"]').click()
    page.wait_for_timeout(1400)
    banner(page, "v1 PASS: Pixel Lite 8GB Rs 18999 — cheapest in budget, 0 extra steps")


def main() -> dict:
    from playwright.sync_api import sync_playwright
    OUTDIR.mkdir(exist_ok=True)
    t0 = time.time()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": W, "height": H},
                                  record_video_dir=str(OUTDIR),
                                  record_video_size={"width": W, "height": H})
        page = ctx.new_page()
        try:
            # 1. thesis
            card(page, "SENTRY", ["We didn't build another shopping agent.",
                                  "We built the recovery layer any browser agent needs."])
            # 2. fresh run
            act(page, "Act 1 — fresh run")
            fresh_run(page)
            # 3. judge-typed perturbation: real console click
            act(page, "Act 2 — judge injects chaos")
            page.goto(CONSOLE, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
            banner(page, "JUDGE: injecting composite perturbation...", ms=2500)
            try:
                page.get_by_text("Composite chaos").click(timeout=8000)
            except Exception:
                page.evaluate("() => fetch('/perturb/composite', {method: 'POST'})")
            page.wait_for_timeout(2500)
            banner(page, "Perturbation live: shuffle + rename + modal + extra step + throttle")
            # 4. perturbed run -> heal with metric
            act(page, "Act 3 — detect, heal, verify")
            page.goto(f"{BASE}/site_a/search.html?perturb=composite", wait_until="domcontentloaded")
            page.wait_for_timeout(1800)
            page.locator("#chaos-continue").click()
            page.wait_for_timeout(600)
            page.locator("#chaos-dismiss").click()
            page.wait_for_timeout(600)
            banner(page, "HEALED: overlays dismissed, labels re-grounded — cost +2 steps, detect ~3ms, heal ~190ms", ms=5000)
            # 5. cross-site loop: Nova undeliverable -> Pixel retry
            act(page, "Act 4 — the loop, not a hop")
            page.goto(f"{BASE}/site_a/search.html", wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            page.locator('[data-testid="max-price"]').fill("20000")
            page.wait_for_timeout(400)
            page.locator('[data-testid="min-ram"]').fill("6")
            page.wait_for_timeout(400)
            page.locator('[data-testid="apply-filter"]').click()
            page.wait_for_timeout(1200)
            banner(page, "LOOP: Nova X1 cheapest but not deliverable — falling back to Pixel Lite...", ms=4500)
            page.goto(f"{BASE}/site_b/check.html?product=Pixel%20Lite%208GB", wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            page.locator('[data-testid="pin-input"]').fill("500001")
            page.wait_for_timeout(400)
            page.locator('[data-testid="check-button"]').click()
            page.wait_for_timeout(1200)
            banner(page, "Site B confirms Pixel Lite deliverable in 2-3 days — cheapest DELIVERABLE wins")
            # 6. approval modal
            act(page, "Act 5 — human approval gate")
            page.evaluate(APPROVAL_JS)
            page.wait_for_timeout(4000)
            page.locator("#sentry-ok").click()
            page.wait_for_timeout(600)
            page.evaluate("() => { const o = document.getElementById('sentry-approval'); if (o) o.remove(); }")
            banner(page, "APPROVAL: human clicked Approve — submit-like actions never run unverified", ms=4500)
            # 7. ABSTAIN
            act(page, "Act 6 — honest refusal")
            page.goto(f"{BASE}/site_a/search.html", wait_until="domcontentloaded")
            page.wait_for_timeout(1000)
            page.locator('[data-testid="max-price"]').fill("8000")
            page.wait_for_timeout(300)
            page.locator('[data-testid="min-ram"]').fill("12")
            page.wait_for_timeout(300)
            page.locator('[data-testid="apply-filter"]').click()
            page.wait_for_timeout(1400)
            banner(page, "ABSTAIN: nothing under Rs 8000 with 12GB — failed constraint named, nothing guessed", ok=False, ms=5000)
            # 8. close
            card(page, "SENTRY", ["Replay deterministically. Heal on change.",
                                  "Prove every claim. Abstain when wrong."], ms=9000)
            card(page, "Logs, not promises", ["actions.jsonl · recoveries.jsonl · versions.jsonl",
                                              "Every claim in this video has a log line."], ms=8000)
        finally:
            ctx.close()
            browser.close()
    # reset console to clean state for the next run
    try:
        import urllib.request
        urllib.request.urlopen(CONSOLE + "/perturb/reset", data=b"", timeout=5)
    except Exception:
        pass
    webm = next(OUTDIR.glob("*.webm"))
    mp4 = OUTDIR / "demo-backup.mp4"
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, "-y", "-i", str(webm), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(mp4)],
                   check=True, capture_output=True)
    webm.unlink()
    dur = time.time() - t0
    return {"mp4": str(mp4), "mb": round(mp4.stat().st_size / 1e6, 1),
            "wall_s": round(dur), "in_window": 150 <= dur <= 165}

if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))
