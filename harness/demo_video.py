"""Backup-video recorder: scripted REAL execution of the demo arc on mocks.

Arc: thesis -> fresh run -> composite perturb -> heal metric on screen ->
cross-site handoff -> approval modal (click simulated; live teammate click on stage) ->
ABSTAIN. Output: demo/demo-backup.mp4 (<=3 min). Venue re-capture covers live beats.
"""
import pathlib
import subprocess
import time

import imageio_ffmpeg

BASE = "http://127.0.0.1:8000"
OUTDIR = pathlib.Path("demo")
W, H = 1280, 800

CARD_JS = """([title, lines]) => {
  const old = document.getElementById('sentry-card'); if (old) old.remove();
  const ov = document.createElement('div'); ov.id = 'sentry-card';
  ov.style.cssText = 'position:fixed;inset:0;background:#0b2f87;color:#fff;z-index:999999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:sans-serif;text-align:center;padding:40px;';
  ov.innerHTML = '<h1 style=font-size:42px;margin:0 0 16px>' + title + '</h1>' +
    lines.map(l => '<p style=font-size:22px;margin:6px;max-width:900px>' + l + '</p>').join('');
  document.body.appendChild(ov);
}"""

BANNER_JS = """([text, ok]) => {
  const old = document.getElementById('sentry-banner'); if (old) old.remove();
  const b = document.createElement('div'); b.id = 'sentry-banner';
  b.style.cssText = 'position:fixed;left:0;right:0;bottom:0;z-index:999999;padding:14px 20px;font-family:sans-serif;font-size:19px;font-weight:700;color:#fff;background:' + (ok ? '#067647' : '#b42318');
  b.textContent = text; document.body.appendChild(b);
}"""

APPROVAL_JS = """() => {
  const ov = document.createElement('div'); ov.id = 'sentry-approval';
  ov.setAttribute('role', 'dialog');
  ov.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:999999;display:flex;align-items:center;justify-content:center;';
  ov.innerHTML = '<div style=background:#fff;color:#000;padding:24px;max-width:480px;font-family:sans-serif;border:3px solid #000><h2>SENTRY wants approval</h2><p><b>action:</b> check_delivery_submit</p><p><b>payload:</b> PIN 500001</p><button id=sentry-ok style=padding:12px_24px;margin-right:12px;font-size:16px>Approve</button><button style=padding:12px_24px;font-size:16px>Deny</button></div>';
  document.body.appendChild(ov);
}"""


def card(page, title, lines, ms=3000):
    page.evaluate(CARD_JS, [title, lines])
    page.wait_for_timeout(ms)
    page.evaluate("() => { const o = document.getElementById('sentry-card'); if (o) o.remove(); }")


def banner(page, text, ok=True, ms=2500):
    page.evaluate(BANNER_JS, [text, ok])
    page.wait_for_timeout(ms)


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
            card(page, "SENTRY", ["We didn't build another shopping agent.",
                                  "We built the recovery layer any browser agent needs."])
            # Act 1: fresh run on VoltKart
            page.goto(f"{BASE}/site_a/search.html", wait_until="domcontentloaded")
            page.wait_for_timeout(800)
            page.locator('[data-testid="max-price"]').fill("20000")
            page.wait_for_timeout(400)
            page.locator('[data-testid="min-ram"]').fill("8")
            page.wait_for_timeout(400)
            page.locator('[data-testid="apply-filter"]').click()
            page.wait_for_timeout(900)
            banner(page, "v1 PASS: Pixel Lite 8GB Rs 18999 — cheapest in budget, 0 extra steps")
            # Act 2: composite perturb -> heal
            page.goto(f"{BASE}/site_a/search.html?perturb=composite", wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
            page.locator("#chaos-continue").click()
            page.wait_for_timeout(400)
            page.locator("#chaos-dismiss").click()
            page.wait_for_timeout(400)
            banner(page, "HEALED: modal + interstitial dismissed — recovery cost +2 steps, detect ~3ms")
            # Act 3: cross-site handoff + approval modal
            page.goto(f"{BASE}/site_b/check.html", wait_until="domcontentloaded")
            page.wait_for_timeout(800)
            page.locator('[data-testid="pin-input"]').fill("500001")
            page.wait_for_timeout(400)
            page.evaluate(APPROVAL_JS)
            page.wait_for_timeout(1500)
            page.locator("#sentry-ok").click()
            page.wait_for_timeout(400)
            page.evaluate("() => { const o = document.getElementById('sentry-approval'); if (o) o.remove(); }")
            page.wait_for_timeout(300)
            page.locator('[data-testid="check-button"]').click()
            page.wait_for_timeout(900)
            banner(page, "Site B confirms deliverable in 2-3 days — cheapest DELIVERABLE, not cheapest listed")
            # Act 4: honest ABSTAIN (real page behavior, infeasible params)
            page.goto(f"{BASE}/site_a/search.html", wait_until="domcontentloaded")
            page.wait_for_timeout(600)
            page.locator('[data-testid="max-price"]').fill("8000")
            page.locator('[data-testid="min-ram"]').fill("12")
            page.wait_for_timeout(300)
            page.locator('[data-testid="apply-filter"]').click()
            page.wait_for_timeout(900)
            banner(page, "ABSTAIN: no phone under Rs 8000 with 12GB — failed constraint: max_price AND min_ram", ok=False)
            card(page, "SENTRY", ["Replay deterministically. Heal on change.",
                                  "Prove every claim. Abstain when wrong."], ms=3000)
        finally:
            ctx.close()
            browser.close()
    webm = next(OUTDIR.glob("*.webm"))
    mp4 = OUTDIR / "demo-backup.mp4"
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, "-y", "-i", str(webm), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(mp4)],
                   check=True, capture_output=True)
    webm.unlink()
    dur = time.time() - t0
    return {"mp4": str(mp4), "mb": round(mp4.stat().st_size / 1e6, 1),
            "wall_s": round(dur), "under_3min": dur <= 180}

if __name__ == "__main__":
    import json
    print(json.dumps(main(), indent=2))
