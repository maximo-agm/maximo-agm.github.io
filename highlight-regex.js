(function () {
  "use strict";
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function fallbackCopy(text) {
    var ta = document.createElement("textarea");
    ta.value = text; ta.style.cssText = "position:fixed;top:0;left:-9999px;opacity:0;";
    document.body.appendChild(ta); ta.select();
    var ok = false;
    try { ok = document.execCommand("copy"); } catch (ignored) {}
    document.body.removeChild(ta);
    return ok;
  }
  function init() {
    var pat = document.getElementById("pat");
    if (!pat) return;
    var sample = document.getElementById("sample");
    var ci = document.getElementById("ci");
    var ml = document.getElementById("ml");
    var cg = document.getElementById("cg");
    var out = document.getElementById("out");
    var status = document.getElementById("status");

    function run() {
      var source = pat.value;
      var text = sample.value;
      status.className = "play-status";
      if (!source) { out.textContent = text; status.textContent = "Enter a pattern above."; return; }
      var groupNum = parseInt(cg.value, 10);
      var useGroup = isFinite(groupNum) && groupNum >= 1;
      var flags = "g" + (ci.checked ? "i" : "") + (ml.checked ? "m" : "") + (useGroup ? "d" : "");
      var re;
      try { re = new RegExp(source, flags); }
      catch (err) {
        out.textContent = text;
        status.className = "play-status err";
        status.textContent = "Invalid pattern — " + err.message;
        return;
      }
      var html = "", cursor = 0, count = 0, guard = 0, m;
      while ((m = re.exec(text)) !== null) {
        if (++guard > 5000) break;
        var start = m.index, end = m.index + m[0].length;
        if (useGroup) {
          var ind = m.indices && m.indices[groupNum];
          if (!ind) { if (m[0].length === 0) re.lastIndex++; continue; }
          start = ind[0]; end = ind[1];
        }
        html += esc(text.slice(cursor, start)) + "<mark>" + esc(text.slice(start, end)) + "</mark>";
        cursor = end; count++;
        if (m[0].length === 0) re.lastIndex++;
      }
      html += esc(text.slice(cursor));
      out.innerHTML = html;
      status.textContent = count === 0 ? "No matches against this sample text." : ("\u2713 " + count + (count === 1 ? " match found" : " matches found"));
    }

    [pat, sample, ci, ml, cg].forEach(function (el) { el.addEventListener("input", run); el.addEventListener("change", run); });
    var presetsBox = document.getElementById("presets");
    if (presetsBox) {
      presetsBox.addEventListener("click", function (e) {
        var btn = e.target.closest(".preset-btn");
        if (!btn) return;
        pat.value = btn.getAttribute("data-p");
        sample.value = btn.getAttribute("data-s");
        cg.value = "";
        run();
      });
    }
    run();

    var recipesList = document.getElementById("recipes-list");
    if (recipesList) {
      recipesList.addEventListener("click", function (e) {
        var btn = e.target.closest(".copy-btn");
        if (!btn) return;
        var row = btn.closest(".recipe-pat");
        var holder = row ? row.querySelector("code") : null;
        if (!holder) return;
        var value = holder.textContent;
        var done = function (label) {
          var original = btn.textContent;
          btn.textContent = label;
          btn.classList.add("copied");
          setTimeout(function () { btn.textContent = original; btn.classList.remove("copied"); }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(value).then(function () { done("Copied"); }, function () { done(fallbackCopy(value) ? "Copied" : "Press Ctrl+C"); });
        } else {
          done(fallbackCopy(value) ? "Copied" : "Press Ctrl+C");
        }
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
