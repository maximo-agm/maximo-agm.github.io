import io, sys, os

CSS = """
  .hlx-glow { position: fixed; inset: 0; pointer-events: none; z-index: 0;
              background: radial-gradient(900px 560px at 78% -12%, var(--c-soft), transparent 64%),
                          radial-gradient(700px 480px at -6% 108%, var(--c-soft), transparent 60%);
              opacity: .85; animation: hlxDrift 24s ease-in-out infinite alternate; }
  @keyframes hlxDrift {
    0%   { transform: translate3d(0, 0, 0) scale(1); }
    50%  { transform: translate3d(-2.5%, 1.6%, 0) scale(1.05); }
    100% { transform: translate3d(2%, -1.8%, 0) scale(1.03); }
  }
  .wrap { position: relative; z-index: 1; }

  .reveal { opacity: 0; transform: translateY(16px); will-change: opacity, transform;
            transition: opacity .58s cubic-bezier(.22,.61,.36,1), transform .58s cubic-bezier(.22,.61,.36,1); }
  .reveal.is-in { opacity: 1; transform: none; }

  @media (prefers-reduced-motion: reduce) {
    .hlx-glow { animation: none; }
    .reveal { opacity: 1; transform: none; transition: none; }
  }
"""

JS = """
<script>
(function () {
  var reduce = false;
  try { reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { reduce = false; }

  var glow = document.createElement('div');
  glow.className = 'hlx-glow';
  if (document.body.firstChild) document.body.insertBefore(glow, document.body.firstChild);
  else document.body.appendChild(glow);

  var SELECTORS = __SELECTORS__;
  var nodes = [];
  SELECTORS.forEach(function (sel) {
    Array.prototype.forEach.call(document.querySelectorAll(sel), function (n) {
      if (nodes.indexOf(n) === -1) nodes.push(n);
    });
  });
  if (!nodes.length) return;

  nodes.forEach(function (n) {
    var siblings = n.parentNode ? Array.prototype.filter.call(n.parentNode.children, function (c) {
      return nodes.indexOf(c) !== -1;
    }) : [n];
    var pos = siblings.indexOf(n);
    n.style.transitionDelay = (Math.max(0, pos) * 90) + 'ms';
    n.classList.add('reveal');
  });

  function countUp(card) {
    var el = card.querySelector('.chapter-rank, .rank, .step-rank');
    if (!el || el.getAttribute('data-counted')) return;
    var raw = (el.textContent || '').trim();
    if (!/^\\d+$/.test(raw)) return;
    el.setAttribute('data-counted', '1');
    var target = parseInt(raw, 10);
    var pad = raw.length;
    if (reduce || target === 0) { el.textContent = raw; return; }
    var started = null;
    var dur = 620;
    function frame(ts) {
      if (started === null) started = ts;
      var p = Math.min(1, (ts - started) / dur);
      var eased = 1 - Math.pow(1 - p, 3);
      var val = Math.round(target * eased);
      el.textContent = String(val).padStart(pad, '0');
      if (p < 1) requestAnimationFrame(frame);
      else el.textContent = raw;
    }
    requestAnimationFrame(frame);
  }

  if (reduce || !('IntersectionObserver' in window)) {
    nodes.forEach(function (n) { n.classList.add('is-in'); countUp(n); });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var n = entry.target;
      n.classList.add('is-in');
      var delay = parseInt(n.style.transitionDelay, 10) || 0;
      setTimeout(function () { countUp(n); }, delay + 120);
      io.unobserve(n);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });

  nodes.forEach(function (n) { io.observe(n); });
})();
</script>
"""

TARGETS = {
    'index.html': ['.release-columns .chapter', '.start-grid .chapter', '.start-primary', '.store'],
    'about.html': ['.three .cut', '.section-title + .cut'],
    'getting-started.html': ['.three .cut', '.steps .cut', '.next .cut', '.store'],
    'ideas-and-feedback.html': ['.steps .cut'],
    'feature-tour.html': ['.feature > .cut', '.feature > .shot', '.feature > .carousel', '.section-title + .cut', '.chrome-note'],
}

for name, sels in TARGETS.items():
    path = os.path.join('.', name)
    s = io.open(path, encoding='utf-8').read()
    if 'hlx-glow' in s:
        print('skip (already)', name)
        continue
    j = s.rindex('</style>')
    s = s[:j] + CSS + s[j:]
    js = JS.replace('__SELECTORS__', repr(sels).replace("'", '"'))
    k = s.rindex('</body>')
    s = s[:k] + js + s[k:]
    io.open(path, 'w', encoding='utf-8').write(s)
    print('motion added', name)
