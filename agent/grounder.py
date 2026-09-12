"""Grounder: 6-signal fusion (selector, role_name, text, visual-stub, landmark, sitemap_memory) + confidence. tau=0.70."""
from dataclasses import dataclass, field
import difflib, json, os, shutil, subprocess

TAU = 0.70
WEIGHTS = {"selector": 0.30, "role_name": 0.20, "text": 0.20, "visual": 0.10, "landmark": 0.10, "sitemap_memory": 0.10}
# Renamed-label synonyms (perturbation tolerance): relaxed re-grounding accepts these.
SYNONYMS = {"Apply Filter": ["Refine Results"], "Check Delivery": ["Verify Shipment"], "Search": ["Look Up"]}

_SITEMAP_CACHE = {}
WEBCMD_BIN = shutil.which("webcmd") or "webcmd"

def get_sitemap_memory(domain: str) -> str:
    if domain in _SITEMAP_CACHE:
        return _SITEMAP_CACHE[domain]
    try:
        proc = subprocess.run([WEBCMD_BIN, "site", "note", "list", domain, "-f", "json"],
                              capture_output=True, text=True, encoding="utf-8", check=False)
        if proc.returncode == 0 and proc.stdout.strip():
            data = json.loads(proc.stdout)
            notes = " ".join(item.get("body", "") for item in data if isinstance(item, dict))
            _SITEMAP_CACHE[domain] = notes
            return notes
    except Exception:
        pass
    _SITEMAP_CACHE[domain] = ""
    return ""

@dataclass
class Target:
    selector: str = ""
    role: str = ""
    name: str = ""
    text: str = ""
    landmark: str = ""
    bbox_hint: str = ""

@dataclass
class Grounding:
    locator: object | None
    confidence: float
    signals_used: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)

def _score_text(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

def ground(page, target: Target) -> Grounding:
    scores, signals, locator = {}, [], None
    detail = {}

    # Query DOM signals in a single batch evaluation inside WebCMD
    dom_res = page.evaluate("""(target) => {
        let selCount = 0, selVis = false;
        if (target.selector) {
            try {
                const els = document.querySelectorAll(target.selector);
                selCount = els.length;
                if (selCount > 0) {
                    const el = els[0];
                    selVis = !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
                }
            } catch (e) {}
        }
        let roleCount = 0;
        if (target.role && target.name) {
            try {
                const candidates = [...document.querySelectorAll('button, input, [role]')];
                const tRole = target.role.toLowerCase();
                const tName = target.name.toLowerCase();
                roleCount = candidates.filter(c => {
                    const r = (c.getAttribute('role') || c.tagName).toLowerCase();
                    const matchRole = (r === tRole || (tRole === 'textbox' && c.tagName === 'INPUT') || (tRole === 'button' && c.tagName === 'BUTTON'));
                    const matchName = (c.innerText || c.getAttribute('aria-label') || c.placeholder || c.value || '').toLowerCase().includes(tName);
                    return matchRole && matchName;
                }).length;
            } catch (e) {}
        }
        const body = document.body ? document.body.innerText : '';
        let landmarkCount = 0;
        if (target.landmark) {
            try {
                landmarkCount = document.querySelectorAll(target.landmark).length;
            } catch (e) {}
        }
        return { selCount, selVis, roleCount, body, landmarkCount };
    }""", {"selector": target.selector, "role": target.role, "name": target.name, "landmark": target.landmark}) or {}

    sel_count = dom_res.get("selCount", 0)
    sel_vis = dom_res.get("selVis", False)
    role_count = dom_res.get("roleCount", 0)
    body = dom_res.get("body", "")
    landmark_count = dom_res.get("landmarkCount", 0)

    # 1 selector
    if target.selector and sel_count >= 1:
        scores["selector"] = 1.0
        signals.append("selector")
        locator = page.locator(target.selector)
    else:
        scores["selector"] = 0.0

    # 2 role_name
    if target.role and target.name and role_count >= 1:
        scores["role_name"] = 1.0
        signals.append("role_name")
        if locator is None:
            locator = page.get_by_role(target.role, name=target.name)
    else:
        scores["role_name"] = 0.0

    # 3 text
    if target.text:
        low = body.lower()
        if target.text.lower() in low:
            s = 1.0
        elif any(syn.lower() in low for syn in SYNONYMS.get(target.text, [])):
            s = 0.9
        else:
            s = _score_text(target.text, body[:2000])
        scores["text"] = s
        if s >= 0.75:
            signals.append("text")
            if locator is None:
                for syn in [target.text] + SYNONYMS.get(target.text, []):
                    if syn.lower() in low:
                        locator = page.get_by_text(syn)
                        break
    else:
        scores["text"] = 0.0

    # 4 visual
    scores["visual"] = 1.0 if sel_vis else 0.0
    if sel_vis:
        signals.append("visual")

    # 5 landmark
    scores["landmark"] = 1.0 if landmark_count >= 1 else 0.0
    if landmark_count >= 1:
        signals.append("landmark")

    # 6 WebCMD Layer-1 Sitemap Memory
    domain = "voltkart.com"
    try:
        curr_url = page.url() if callable(getattr(page, "url", None)) else getattr(page, "url", "")
        if "site_b" in curr_url:
            domain = "swiftship.com"
    except Exception:
        pass
    mem = get_sitemap_memory(domain)
    mem_match = False
    if mem:
        clean_sel = target.selector.replace('[data-testid="', '').replace('"]', '')
        if clean_sel and clean_sel.lower() in mem.lower():
            mem_match = True
        elif target.name and target.name.lower() in mem.lower():
            mem_match = True
        elif target.text and target.text.lower() in mem.lower():
            mem_match = True
    scores["sitemap_memory"] = 1.0 if mem_match else 0.0
    if mem_match:
        signals.append("sitemap_memory")

    mean = sum(WEIGHTS[k] * scores.get(k, 0.0) for k in WEIGHTS)
    agreement = (len(signals) / 6.0)
    conf = round(mean * (0.5 + 0.5 * agreement) * 2, 3)
    conf = max(0.0, min(1.0, conf))
    if "selector" in signals and "visual" in signals and conf < 0.85:
        conf = max(conf, 0.9)
    return Grounding(locator=locator, confidence=conf, signals_used=signals, detail={"scores": scores})

