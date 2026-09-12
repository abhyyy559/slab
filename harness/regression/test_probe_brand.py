"""Unit tests for the live-probe block classifier (ABSTAIN taxonomy)."""
from harness.variants.transfer_probe import classify_block


def test_auth_wall():
    assert classify_block("<html><body>Please log in to continue</body></html>") == "auth_wall"
    assert classify_block("", status=403) == "auth_wall"


def test_captcha():
    assert classify_block("<div>recaptcha challenge</div>") == "captcha"


def test_bot_block():
    assert classify_block("<title>Attention Required! | Cloudflare</title>") == "bot_block"


def test_rate_limit():
    assert classify_block("", status=429) == "rate_limit"
    assert classify_block("<p>Too many requests, slow down</p>") == "rate_limit"


def test_clean_page():
    assert classify_block("<html><body><article>In stock £13.99</article></body></html>") is None


def test_brand_planner_tokens():
    from agent.planner import plan_goal
    p = plan_goal("I want a Pixel phone under Rs 20000")
    assert p.supported and p.params.get("brand") == "pixel"
    q = plan_goal("Find a Samsung phone")
    assert q.supported and q.params.get("brand") == "samsung"
