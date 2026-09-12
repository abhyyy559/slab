"""Mock DOM contracts: anyone may restyle the mocks, but these must hold or the
agent breaks. Catches silent teammate/OneDrive edits (incident 2026-09-12:
richer VoltKart chrome appeared mid-stream; contracts held, runs re-verified).
"""
import pathlib

A = pathlib.Path("mocks/site_a/search.html").read_text(encoding="utf-8")
B = pathlib.Path("mocks/site_b/check.html").read_text(encoding="utf-8")

def test_site_a_contracts():
    for tid in ("search-box", "search-button", "max-price", "min-ram",
                "apply-filter", "results"):
        assert f'data-testid="{tid}"' in A, tid
    assert A.count('<article data-testid="product-card"') == 3
    assert ">Search</button>" in A
    assert ">Apply Filter</button>" in A
    assert "<h2>Pixel Lite 8GB</h2>" in A  # evidence title source (price lives in .price span)
    assert "Rs 18,999" in A
    assert 'src="/chaos.js"' in A
    assert "__chaosThrottleMs" in A

def test_site_b_contracts():
    for tid in ("pin-input", "check-button", "delivery-status"):
        assert f'data-testid="{tid}"' in B, tid
    assert ">Check Delivery</button>" in B
    assert "Delivery available to PIN 500001 in 2-3 days" in B
    assert 'src="/chaos.js"' in B
    assert "__chaosThrottleMs" in B
