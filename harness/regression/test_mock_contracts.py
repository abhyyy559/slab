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
E = pathlib.Path("mocks/site_b/enquiry.html").read_text(encoding="utf-8")


def test_site_a_id_contracts():
    for tid in ("search-box", "search-button", "max-price", "min-ram",
                "apply-filter", "results"):
        assert f'data-testid="{tid}"' in A, tid
    # The catalogue is rendered client-side from CATALOG, so the card markup lives in
    # a template string rather than as literal DOM. Pin the template + the data instead.
    assert 'data-testid="product-card"' in A, "card template must set the product-card testid"
    assert "var CATALOG = [" in A, "catalogue data block must exist"
    assert ">Search</button>" in A
    assert ">Apply Filter</button>" in A
    assert 'data-testid="price"' in A, "cards must expose a price testid"
    assert 'data-testid="product-link"' in A
    assert 'src="/chaos.js"' in A
    assert "__chaosThrottleMs" in A


def test_site_a_catalogue_shape():
    """The catalogue must stay a real search space: several brands, a spread of prices
    and RAM, and at least one out-of-stock listing so 'cheapest in-stock' is a real
    constraint and not a formality."""
    import json
    import re
    block = A.split("var CATALOG = [", 1)[1].split("];", 1)[0]
    rows = re.findall(r"\{([^{}]*)\}", block)
    assert len(rows) >= 12, f"catalogue too small to be a search space: {len(rows)}"
    names = re.findall(r'name:"([^"]+)"', block)
    assert len(names) == len(rows), "every catalogue row needs a name"
    assert len(set(names)) == len(names), "catalogue names must be unique"
    prices = [int(p) for p in re.findall(r'price:(\d+)', block)]
    rams = [int(r) for r in re.findall(r'ram:(\d+)', block)]
    assert min(prices) < 10000 and max(prices) > 30000, "prices should span a real range"
    assert min(rams) <= 6 and max(rams) >= 12, "RAM should span a real range"
    assert "stock:false" in block, "keep at least one out-of-stock listing"
    # Every card must render the machine-readable hooks the agent extracts from.
    for attr in ("data-name=", "data-price=", "data-ram=", "data-stock=", "data-rating="):
        assert attr in A, f"card template must emit {attr}"


def test_site_a_out_of_stock_is_visible_but_not_renderable_as_available():
    """An out-of-stock card must still render (a judge should see it) but carry the
    signal the agent uses to exclude it."""
    assert 'data-stock="' in A
    assert "Out of stock" in A
    assert "Notify me when available" in A


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
    # The page computes deliverability per-product, so the exact sentence lives in the
    # script. Pin the outcomes the agent's constraint checker must classify correctly.
    assert "Delivery available to PIN " in B and "in 2-3 days" in B
    assert "Not serviceable:" in B, "unserved-product message must exist"
    assert "outside the 3-day metro SLA" in B, "slow-line message must exist"
    assert 'src="/chaos.js"' in B
    assert "__chaosThrottleMs" in B


def test_site_b_structure_contracts():
    assert 'aria-label="PIN code"' in B, "PIN input keeps an accessible name"
    assert 'inputmode="numeric"' in B, "PIN input stays discoverable by input mode"
    assert 'id="status"' in B, "status div keeps a stable id"
    assert 'role="status"' in B, "status div keeps role=status for structural read"
    # The page's own lookup helpers must survive an id strip.
    assert "pinEl()" in B and "statusEl()" in B and "checkButton()" in B


# --- Enquiry desk (step 5: the irreversible cross-site write) ------------------
def test_enquiry_id_contracts():
    for tid in ("enquiry-product", "enquiry-name", "enquiry-contact",
                "enquiry-message", "enquiry-submit", "enquiry-status"):
        assert f'data-testid="{tid}"' in E, tid
    assert ">Send enquiry</button>" in E
    assert 'src="/chaos.js"' in E
    assert "__chaosThrottleMs" in E


def test_enquiry_structure_contracts():
    # Must survive a testid strip + rename: accessible names, labels, live region.
    for lab in ('aria-label="Product"', 'aria-label="Your name"',
                'aria-label="Contact"', 'aria-label="Message"'):
        assert lab in E, lab
    assert 'role="status"' in E and 'aria-live="polite"' in E
    assert 'id="status"' in E
    # The page's own lookup helpers must survive an id/testid strip.
    assert "productEl()" in E and "statusEl()" in E and "submitButton()" in E
    # Positive-proof confirmation copy the detector greps for.
    assert "Enquiry received" in E and "Reference" in E


def test_enquiry_accepts_cross_site_product_handoff():
    # The rubric's cross-site requirement: the product chosen on Site A arrives as a
    # query param and lands in the form. Without this the handoff is decorative.
    assert 'get("product")' in E or "get(\"product\")" in E, "enquiry must read ?product="
    assert "productEl().value = q" in E or ".value = q" in E
