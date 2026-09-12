/* SENTRY live-chaos injector. Served statically with the mocks.
   Source of truth: ?perturb= query param (deterministic runs) else console /status (judge-operated, polled 600ms). */
(function () {
  var qp = new URLSearchParams(location.search).get("perturb");
  var applied = "__init__";
  var RENAMES = [["Apply Filter", "Refine Results"], ["Check Delivery", "Verify Shipment"], ["Search", "Look Up"]];

  function setOf(a) {
    if (!a || a === "reset") return [];
    if (a === "composite") return ["shuffle", "rename", "modal", "extra_step", "throttle", "strip"];
    return [a];
  }
  function norm(a) { return (!a || a === "reset") ? null : a; }

  function stash(el) {
    if (!el.dataset.chaosOrig) el.dataset.chaosOrig = el.textContent;
    if (!el.hasAttribute("data-chaos-tid")) el.setAttribute("data-chaos-tid", el.getAttribute("data-testid") || "");
  }
  function revert() {
    document.querySelectorAll("[data-chaos-tid]").forEach(function (el) {
      el.textContent = el.dataset.chaosOrig;
      var t = el.getAttribute("data-chaos-tid");
      if (t) el.setAttribute("data-testid", t); else el.removeAttribute("data-testid");
      el.removeAttribute("data-chaos-tid"); delete el.dataset.chaosOrig;
    });
    ["chaos-modal", "chaos-confirm"].forEach(function (id) {
      var o = document.getElementById(id); if (o) o.remove();
    });
    var res = document.querySelector('[data-testid="results"], #chaos-results');
    window.__chaosThrottleMs = 0;
  }
  function shuffle() {
    var res = document.querySelector('[data-testid="results"]');
    if (!res) return;
    res.id = "chaos-results";
    Array.from(res.children).reverse().forEach(function (c) { res.appendChild(c); });
  }
  function rename(strip) {
    document.querySelectorAll("button").forEach(function (b) {
      RENAMES.forEach(function (pair) {
        if (b.textContent.trim() === pair[0]) {
          stash(b); b.textContent = pair[1];
          if (strip) b.removeAttribute("data-testid");
        }
      });
    });
  }
  function once(key) {
    /* Cookie-modal realism: interstitials show once per tab session, then stay dismissed. */
    try {
      if (sessionStorage.getItem(key)) return false;
      sessionStorage.setItem(key, "1"); return true;
    } catch (e) { return true; }
  }
  function overlay(id, title, body, btnId, btnText) {
    if (document.getElementById(id)) return;
    var ov = document.createElement("div");
    ov.id = id; ov.setAttribute("role", "dialog");
    ov.style.cssText = "position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:999998;display:flex;align-items:center;justify-content:center;";
    ov.innerHTML = '<div style="background:#fff;color:#000;padding:24px;max-width:420px;font-family:sans-serif;border:3px solid #000;">'
      + "<h2>" + title + "</h2><p>" + body + "</p>"
      + '<button id="' + btnId + '" style="padding:12px 24px;font-size:16px;">' + btnText + "</button></div>";
    document.body.appendChild(ov);
  }
  function apply(a) {
    var key = a || "none";
    if (key === applied) return;
    revert(); applied = key;
    if (!a) return;
    var set = setOf(a);
    window.__chaosThrottleMs = set.indexOf("throttle") >= 0 ? (a === "composite" ? 2000 : 2500) : 0;
    if (set.indexOf("shuffle") >= 0) shuffle();
    if (set.indexOf("rename") >= 0) rename(set.indexOf("strip") >= 0);
    if (set.indexOf("modal") >= 0 && once("chaos-modal-shown")) overlay("chaos-modal", "Special offer!", "A surprise modal blocks the page. Dismiss it to continue.", "chaos-dismiss", "Dismiss");
    if (set.indexOf("extra_step") >= 0 && once("chaos-confirm-shown")) overlay("chaos-confirm", "One more step", "The site inserted a confirmation. Continue to proceed.", "chaos-continue", "Continue");
    document.querySelectorAll("#chaos-dismiss").forEach(function (b) { b.onclick = function () { var o = document.getElementById("chaos-modal"); if (o) o.remove(); }; });
    document.querySelectorAll("#chaos-continue").forEach(function (b) { b.onclick = function () { var o = document.getElementById("chaos-confirm"); if (o) o.remove(); }; });
  }
  async function poll() {
    if (qp) { apply(norm(qp)); return; }
    try {
      var r = await fetch("http://127.0.0.1:8765/status");
      var s = await r.json();
      apply(norm(s.active));
    } catch (e) { /* console down: leave page as-is */ }
  }
  if (qp) { apply(norm(qp)); }
  else { poll(); setInterval(poll, 600); }
})();
