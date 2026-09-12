/* SENTRY adaptive-chaos injector. Served statically with the mocks.
 *
 * Two control paths:
 *   deterministic  ?perturb=<type>            applied once on load (offline/CI runs)
 *   judge-operated  poll :8765/status          live injection during a demo (600ms)
 *
 * Chaos types model changes a real site makes without warning. The agent must
 * still find and drive the right controls by STRUCTURE (role, accessible name,
 * label text, landmark, ordinal position), not by brittle test ids.
 *
 *   rename        button + section labels swapped for synonyms (accessible name changes)
 *   strip         data-testid removed from interactive controls (id-based hooks die)
 *   move          controls relocated / reordered within the page (XPath fragments break)
 *   attrs         data-* attributes mutated, classes renamed (attribute selectors break)
 *   modal         blocking interstitial that must be dismissed
 *   extra_step    inserted confirmation step that must be cleared
 *   throttle      response latency injected (slow network)
 *   ab            every OTHER product card hidden (A/B variant of the result set)
 *   swap          product list replaced with an equivalent re-rendered list (SPA-ish)
 *   composite     rename + strip + move + attrs + modal + extra_step + throttle
 *   chaos_max     everything including ab + swap (worst case)
 */
(function () {
  "use strict";
  var qp = new URLSearchParams(location.search).get("perturb");
  var applied = "__init__";

  /* Accessible-name synonyms per control (the agent's SYNONYMS table mirrors these). */
  var RENAMES = [
    ["Apply Filter", "Refine Results"],
    ["Check Delivery", "Verify Shipment"],
    ["Search", "Look Up"],
    ["Apply", "Refine"]
  ];
  /* Section/heading synonyms used on the results zone. */
  var SECTION_RENAMES = [["Results", "Matches"], ["Filters", "Refinements"]];

  function setOf(a) {
    if (!a || a === "reset") return [];
    if (a === "composite") return ["rename", "strip", "move", "attrs", "modal", "extra_step", "throttle"];
    if (a === "chaos_max") return ["rename", "strip", "move", "attrs", "modal", "extra_step", "throttle", "ab", "swap"];
    return [a];
  }
  function norm(a) { return (!a || a === "reset") ? null : a; }

  /* ---------------------------------------------------------------- bookkeeping */
  function stash(el) {
    if (!el.hasAttribute("data-chaos-orig-text")) {
      el.setAttribute("data-chaos-orig-text", el.textContent);
    }
    if (!el.hasAttribute("data-chaos-tid")) {
      el.setAttribute("data-chaos-tid", el.getAttribute("data-testid") || "");
    }
    if (!el.hasAttribute("data-chaos-orig-id")) {
      el.setAttribute("data-chaos-orig-id", el.id || "");
    }
  }

  function revert() {
    document.querySelectorAll("[data-chaos-tid]").forEach(function (el) {
      el.textContent = el.getAttribute("data-chaos-orig-text") || el.textContent;
      var t = el.getAttribute("data-chaos-tid");
      if (t) el.setAttribute("data-testid", t); else el.removeAttribute("data-testid");
      var oid = el.getAttribute("data-chaos-orig-id");
      if (oid) el.id = oid; else el.removeAttribute("id");
      el.removeAttribute("data-chaos-tid");
      el.removeAttribute("data-chaos-orig-id");
      el.removeAttribute("data-chaos-orig-text");
    });
    document.querySelectorAll("[data-chaos-orig-attr]").forEach(function (el) {
      var saved = el.getAttribute("data-chaos-orig-attr");
      try { JSON.parse(saved).forEach(function (pair) {
        if (pair[1] === null) el.removeAttribute(pair[0]); else el.setAttribute(pair[0], pair[1]);
      }); } catch (e) {}
      el.removeAttribute("data-chaos-orig-attr");
    });
    document.querySelectorAll("[data-chaos-moved]").forEach(function (el) {
      var sel = el.getAttribute("data-chaos-moved");
      var home = document.querySelector(sel);
      if (home) home.appendChild(el);
      el.removeAttribute("data-chaos-moved");
    });
    document.querySelectorAll("[data-chaos-hid]").forEach(function (el) {
      el.style.display = "";
      el.removeAttribute("data-chaos-hid");
    });
    ["chaos-modal", "chaos-confirm"].forEach(function (id) {
      var o = document.getElementById(id); if (o) o.remove();
    });
    var swapped = document.getElementById("chaos-list-container");
    if (swapped) swapped.removeAttribute("id");
    window.__chaosThrottleMs = 0;
  }

  /* -------------------------------------------------------------------- effects */
  function rename(strip) {
    var map = RENAMES.concat(SECTION_RENAMES);
    document.querySelectorAll("button, a, h3, [role='button'], .results-bar .count").forEach(function (el) {
      var txt = (el.textContent || "").trim();
      map.forEach(function (pair) {
        if (txt === pair[0]) {
          stash(el);
          el.textContent = pair[1];
          if (strip) el.removeAttribute("data-testid");
        }
      });
    });
  }

  /* Remove test ids from interactive controls -> id/attribute selectors fail. */
  function strip() {
    document.querySelectorAll("[data-testid]").forEach(function (el) {
      var tag = el.tagName.toLowerCase();
      if (tag === "button" || tag === "input" || tag === "a" || tag === "select" || el.getAttribute("role")) {
        stash(el);
        el.removeAttribute("data-testid");
      }
    });
  }

  /* Relocate controls within their parent: XPath/absolute-position assumptions break. */
  function move() {
    document.querySelectorAll("aside.filters, .row, .searchbar").forEach(function (row) {
      if (row.children.length < 2) return;
      var last = row.lastElementChild;
      row.insertBefore(last, row.firstElementChild);
      last.setAttribute("data-chaos-moved", "." + (row.className.split(" ")[0] || "row"));
    });
  }

  /* Mutate classes and data-* attributes so attribute selectors stop matching. */
  function attrs() {
    document.querySelectorAll("[data-chaos-suffix]").forEach(function () {});
    document.querySelectorAll("[data-name]").forEach(function (el) {
      var saved = [];
      ["data-name", "data-price", "data-ram", "data-rating"].forEach(function (a) {
        if (el.hasAttribute(a)) { saved.push([a, el.getAttribute(a)]); el.setAttribute("data-" + a.slice(5) + "-m", el.getAttribute(a)); el.removeAttribute(a); }
      });
      if (saved.length) el.setAttribute("data-chaos-orig-attr", JSON.stringify(saved));
    });
    document.querySelectorAll("article[data-testid='product-card'], article[data-moved], section[data-testid='results']").forEach(function (el) {
      if (el.className) { el.className = el.className + " chaos-renamed"; }
    });
  }

  /* A/B variant: every other result card is hidden. */
  function ab() {
    document.querySelectorAll("[data-testid='product-card'], #chaos-results > article").forEach(function (card, i) {
      if (i % 2 === 1) { card.style.display = "none"; card.setAttribute("data-chaos-hid", "1"); }
    });
  }

  /* Replace the results list with an equivalent re-rendered list (SPA-style swap).
     The cards keep their text/structure but live in a new container with a new id. */
  function swap() {
    var res = document.querySelector("[data-testid='results']");
    if (!res || document.getElementById("chaos-list-container")) return;
    var clone = res.cloneNode(true);
    clone.id = "chaos-list-container";
    clone.removeAttribute("data-testid");
    clone.classList.add("chaos-swapped");
    res.parentNode.insertBefore(clone, res);
    res.style.display = "none";
    res.setAttribute("data-chaos-hid", "1");
  }

  function once(key) {
    try {
      if (sessionStorage.getItem(key)) return false;
      sessionStorage.setItem(key, "1"); return true;
    } catch (e) { return true; }
  }

  function overlay(id, title, body, btnId, btnText) {
    if (document.getElementById(id)) return;
    var ov = document.createElement("div");
    ov.id = id; ov.setAttribute("role", "dialog"); ov.setAttribute("aria-modal", "true");
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
    window.__chaosThrottleMs = set.indexOf("throttle") >= 0 ? (a === "composite" || a === "chaos_max" ? 2000 : 2500) : 0;
    if (set.indexOf("rename") >= 0) rename(set.indexOf("strip") >= 0);
    if (set.indexOf("strip") >= 0) strip();
    if (set.indexOf("move") >= 0) move();
    if (set.indexOf("attrs") >= 0) attrs();
    if (set.indexOf("swap") >= 0) swap();
    if (set.indexOf("ab") >= 0) ab();
    if (set.indexOf("modal") >= 0 && once("chaos-modal-shown")) {
      overlay("chaos-modal", "Special offer!", "A surprise modal blocks the page. Dismiss it to continue.", "chaos-dismiss", "Dismiss");
    }
    if (set.indexOf("extra_step") >= 0 && once("chaos-confirm-shown")) {
      overlay("chaos-confirm", "One more step", "The site inserted a confirmation. Continue to proceed.", "chaos-continue", "Continue");
    }
    document.querySelectorAll("#chaos-dismiss").forEach(function (b) {
      b.onclick = function () { var o = document.getElementById("chaos-modal"); if (o) o.remove(); };
    });
    document.querySelectorAll("#chaos-continue").forEach(function (b) {
      b.onclick = function () { var o = document.getElementById("chaos-confirm"); if (o) o.remove(); };
    });
  }

  async function poll() {
    if (qp) { apply(norm(qp)); return; }
    try {
      var r = await fetch("http://127.0.0.1:8765/status");
      var s = await r.json();
      apply(norm(s.active));
    } catch (e) { /* console down: leave the page alone */ }
  }

  if (qp) { apply(norm(qp)); }
  else { poll(); setInterval(poll, 600); }
})();
