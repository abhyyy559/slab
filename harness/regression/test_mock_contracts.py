"""Mock DOM contracts: anyone may restyle the mocks, but these must hold or the
agent breaks. Catches silent teammate/OneDrive edits.

Two contract layers:
  1. ID contracts  -- data-testid hooks the baseline run uses (v1 must not regress).
  2. STRUCTURE contracts -- roles / labels / landmarks the *perturbation* run falls
     back on when test ids are stripped or labels renamed. If a restyle removes
     these, the adaptive path silently loses its footing, so they are pinned here.
"""
import pathlib

A = pathlib.Path("mocks/site_a/search.html").read_text(encoding="utf-8")
B = pathlib.Path("mocks/site_b/check.html").read_text(encoding="utf-8")


def test_site_a_id_contracts():
    for tid in ("search-box", "search-button", "max-price", "min-ram",
                "apply-filter", "results"):
        assert f'data-testid="{tid}"' in A, tid
    assert A.count('<article data-testid="product-card"') == 3
    assert ">Search</button>" in A
    assert ">Apply Filter</button>" in A
    assert "<h2>Pixel Lite 8GB</h2>" in A
    assert "Rs 18,999" in A
    assert 'src="/chaos.js"' in A
    assert "__chaosThrottleMs" in A


def test_site_a_structure_contracts():
    # The adaptive path (strip/rename) needs these to exist independently of ids.
    assert 'role="search"' in A, "search form must expose role=search"
    assert 'aria-label="Search phones"' in A, "search box keeps an accessible name"
    assert 'aria-label="Max price"' in A, "max-price input keeps an aria-label"
    assert 'aria-label="Min RAM"' in A, "min-ram input keeps an aria-label"
    assert 'aria-label="Filters"' in A, "filters aside keeps a landmark label"
    assert 'aria-label="Results"' in A, "results section keeps a landmark label"
    # The page's own filter reader must not depend on data-testid alone.
    assert "maxPriceEl" in A and "minRamEl" in A
    assert 'getElementById("fmax")' in A and 'getElementById("fmin")' in A


def test_site_b_id_contracts():
    for tid in ("pin-input", "check-button", "delivery-status"):
        assert f'data-testid="{tid}"' in B, tid
    assert ">Check Delivery</button>" in B
    assert "Delivery available to PIN 500001 in 2-3 days" in B
    assert 'src="/chaos.js"' in B
    assert "__chaosThrottleMs" in B


def test_site_b_structure_contracts():
    assert 'aria-label="PIN code"' in B, "PIN input keeps an accessible name"
    assert 'inputmode="numeric"' in B, "PIN input stays discoverable by input mode"
    assert 'id="status"' in B, "status div keeps a stable id"
    assert 'role="status"' in B, "status div keeps role=status for structural read"
    # The page's own lookup helpers must survive an id strip.
    assert "pinEl()" in B and "statusEl()" in B and "checkButton()" in B
