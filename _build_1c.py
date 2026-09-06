import io, os, base64

W = os.path.expanduser('~/mnt/HIGHLIGHT/website')
F = os.path.expanduser('~/mnt/Highlight Homepage Redesign Directions/fonts')

def b64(p):
    with open(p, 'rb') as f:
        return base64.b64encode(f.read()).decode()

orb700 = b64(os.path.join(F, 'orbitron-700.woff2'))
orb900 = b64(os.path.join(F, 'orbitron-900.woff2'))
logo = io.open(os.path.join(W, '_logo128.txt'), encoding='utf-8').read().strip()

S = "https://sites.google.com/view/highlight-mxm"
CHROME = "https://chromewebstore.google.com/detail/highlight/fifamngjkcdgdcomgdjjegepgnhdjcif"
EDGE = "https://microsoftedge.microsoft.com/addons/detail/gbhmmddcommimmoioggbgchckfjkkhfe"
FF = "https://addons.mozilla.org/en-US/firefox/addon/highlight_mxm/"

TRACKS = [
    ("Chrome", "#6FA8FF", "2.1.0", CHROME, "Add to Chrome", [
        ("02", "An update is planned", "Soon", "Chrome is still on Chapter One. The next chapters are written and waiting on review.", None),
        ("01", "The Release", "v2.1.0", "What shipped in the original release, what it asks permission for, and the issues fixed since.",
         S + "/changelogs/chrome-changelogs/210Chrome-A7K29Xm4"),
    ]),
    ("Edge", "#3FC98A", "2.3.1", EDGE, "Add to Edge", [
        ("01", "Nothing Held Back", "v2.3.1", "Highlight arrives on Edge at the version it is on now, so this chapter is everything the extension does.",
         S + "/changelogs/edge-changelogs/231Edge-EsufWHwz"),
    ]),
    ("Firefox", "#FF9E7A", "2.3.1", FF, "Add to Firefox", [
        ("02", "What Carries Over", "v2.3.1", "Your lists, rules and settings follow your Firefox account between computers.",
         S + "/changelogs/firefox-changelogs/231Firefox-M1x8R5v3"),
        ("01", "Arrival at Full Strength", "v2.3.0", "Highlight arrived on Firefox already carrying three chapters' work, so this one is everything it does.",
         S + "/changelogs/firefox-changelogs/230Firefox-F4h6T2z9"),
    ]),
]

START = [
    ("01", "Getting started", "Install it, make your first list, and see it mark a page.", S + "/learn-and-explore/getting-started"),
    ("02", "Feature tour", "Everything it can do, with the real interface and every tooltip style.", S + "/learn-and-explore/feature-tour"),
    ("03", "Pattern rules", "Highlight by shape — case numbers, dates, amounts — not by a list of words.", S + "/learn-and-explore/regex-rules"),
    ("04", "Presets", "Ready-made colour themes you can paste straight in.", S + "/learn-and-explore/presets"),
    ("05", "FAQ", "What to check when something isn't highlighting.", S + "/learn-and-explore/faq"),
]

def track_install(t):
    label, color, ver, url, cta, _ = t
    return ('<div class="track" data-reveal>'
            '<div class="track-label" style="color:%s">%s</div>'
            '<div class="track-ver">v%s</div>'
            '<a class="track-cta" style="color:%s" href="%s" target="_blank" rel="noopener">%s &#8594;</a>'
            '</div>' % (color, label, ver, color, url, cta))

def chapter(ch, color):
    num, name, ver, body, href = ch
    inner = ('<div class="ch-num" data-count-to="%s" style="color:%s">00</div>'
             '<div class="ch-name">%s</div>'
             '<div class="ch-ver">%s</div>'
             '<div class="ch-body">%s</div>') % (num, color, name, ver, body)
    if href:
        return '<a class="ch" data-reveal href="%s" target="_blank" rel="noopener">%s</a>' % (href, inner)
    return '<div class="ch ch-pending" data-reveal>%s</div>' % inner

def track_column(t):
    label, color, ver, url, cta, chapters = t
    n = len(chapters)
    return ('<details class="browser" style="--tc:%s">'
            '<summary><span class="chev"></span><span class="dot"></span>'
            '<span class="col-name">%s</span><span class="col-ver">v%s</span>'
            '<span class="col-count">%d %s</span></summary>'
            '<div class="chapters">%s</div></details>'
            % (color, label, ver, n, 'CHAPTER' if n == 1 else 'CHAPTERS',
               ''.join(chapter(c, color) for c in chapters)))

def start_row(s):
    n, label, body, href = s
    return ('<a class="srow" data-reveal href="%s" target="_blank" rel="noopener">'
            '<div class="srow-n">%s</div><div class="srow-label">%s</div><div class="srow-body">%s</div>'
            '<div class="srow-arrow">&#8594;</div></a>' % (href, n, label, body))

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Highlight &mdash; Release log</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
@font-face{font-family:'Orbitron';src:url(data:font/woff2;base64,__ORB700__) format('woff2');font-weight:700;font-display:swap;}
@font-face{font-family:'Orbitron';src:url(data:font/woff2;base64,__ORB900__) format('woff2');font-weight:900;font-display:swap;}

:root{
  --bg:#0b0c10; --ink:#ECEFF3; --body:#B8C0CC; --mute:#8A93A3; --dim:#6b7280;
  --line:rgba(255,255,255,.1); --line-soft:rgba(255,255,255,.08);
  --coral:#FF9E7A; --pink:#FF8FA8; --gold:#FFDD73; --mint:#3FC98A; --blue:#6FA8FF;
  --orb:'Orbitron',sans-serif; --mono:'IBM Plex Mono',monospace; --sans:'Sora',system-ui,sans-serif;
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;line-height:1.6;}
a{text-decoration:none;color:inherit;}

@keyframes hlxDrift{0%{transform:translate3d(0,0,0) scale(1);}50%{transform:translate3d(-3%,2%,0) scale(1.06);}100%{transform:translate3d(2%,-2%,0) scale(1.04);}}
@keyframes hlxSweepBg{from{background-size:0% 100%;}to{background-size:100% 100%;}}
@keyframes hlxInk{0%,55%{color:var(--ink);}100%{color:#0A0E14;}}
@keyframes hlxRise{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:none;}}

.stage{position:relative;overflow:hidden;padding:clamp(40px,6vw,96px) clamp(20px,5vw,88px) 80px;}
.ghost{position:absolute;right:-40px;top:10px;font-family:var(--orb);font-weight:900;
  font-size:clamp(220px,38vw,520px);line-height:1;color:var(--coral);opacity:.05;z-index:0;pointer-events:none;user-select:none;}
.glow{position:absolute;top:-200px;left:-160px;width:720px;height:560px;
  background:radial-gradient(closest-side,rgba(255,143,168,.15),transparent 70%);
  animation:hlxDrift 24s ease-in-out infinite alternate;pointer-events:none;z-index:0;}
.inner{position:relative;z-index:1;}

.topbar{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-bottom:clamp(40px,6vw,72px);}
.brand{display:flex;align-items:center;gap:12px;}
.brand img{width:28px;height:28px;border-radius:6px;display:block;}
.brand span{font-family:var(--orb);font-weight:900;font-size:18px;letter-spacing:.06em;}
.nav{display:flex;gap:28px;font-family:var(--mono);font-size:12px;letter-spacing:.1em;color:var(--mute);}
.nav a:hover{color:var(--coral);}

.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.24em;color:var(--coral);margin-bottom:20px;}
h1{margin:0;font-family:var(--orb);font-weight:900;letter-spacing:-.01em;}
.h1-a{font-size:clamp(26px,5vw,60px);line-height:1;}
.h1-b{font-size:clamp(30px,5.9vw,84px);line-height:1.04;margin:10px 0 0;}
.mark{display:inline;padding:2px 10px;border-radius:4px;
  background-image:linear-gradient(90deg,var(--coral),var(--pink));
  background-repeat:no-repeat;background-size:0% 100%;
  -webkit-box-decoration-break:clone;box-decoration-break:clone;}
.mark.go{animation:hlxSweepBg 1.1s cubic-bezier(.16,1,.3,1) .25s both, hlxInk 1.1s linear .25s both;}
.lede{margin:36px 0 0;font-weight:500;font-size:clamp(16px,1.5vw,19px);line-height:1.6;color:var(--body);}

.tracks{display:flex;flex-wrap:wrap;margin-top:clamp(40px,5vw,64px);}
.track{flex:1 1 220px;padding-right:48px;margin-right:48px;border-right:1px solid var(--line);}
.track:last-child{border-right:none;margin-right:0;padding-right:0;}
.track-label{font-family:var(--mono);font-size:12px;letter-spacing:.15em;margin-bottom:14px;}
.track-ver{font-family:var(--orb);font-weight:900;font-size:clamp(28px,3.4vw,42px);margin-bottom:10px;}
.track-cta{font-family:var(--orb);font-weight:700;font-size:16px;}
.track-cta:hover{text-decoration:underline;}

.srule{display:flex;align-items:center;gap:14px;margin-bottom:40px;}
.srule span:first-child{font-family:var(--mono);font-size:11px;letter-spacing:.2em;color:var(--mute);}
.srule .bar{flex:1;height:1px;background:var(--line);}
.block{margin-top:clamp(64px,9vw,112px);}

.drop{border-top:1px solid var(--line);}
.drop>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:14px;padding:26px 0;}
.drop>summary::-webkit-details-marker{display:none;}
.drop-title{font-family:var(--orb);font-weight:900;font-size:clamp(20px,2.4vw,30px);}
.drop-hint{font-family:var(--mono);font-size:11px;letter-spacing:.18em;color:var(--dim);margin-left:auto;}
.chev{width:14px;height:14px;flex:0 0 14px;border-right:2px solid var(--coral);border-bottom:2px solid var(--coral);
  transform:rotate(45deg);transition:transform .22s ease;margin-bottom:4px;}
details[open]>summary .chev{transform:rotate(-135deg);margin-bottom:-4px;}

.browser{border-top:1px solid var(--line-soft);}
.browser>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:14px;padding:20px 0 20px 6px;transition:padding-left .2s ease;}
.browser>summary::-webkit-details-marker{display:none;}
.browser>summary:hover{padding-left:16px;}
.browser .chev{border-color:var(--tc);}
.dot{width:10px;height:10px;border-radius:50%;display:inline-block;background:var(--tc);}
.col-name{font-family:var(--orb);font-weight:900;font-size:clamp(17px,1.9vw,22px);}
.col-ver{font-family:var(--mono);font-size:12px;color:var(--dim);}
.col-count{font-family:var(--mono);font-size:11px;letter-spacing:.16em;color:var(--dim);margin-left:auto;}
.chapters{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:0 48px;padding:0 0 22px 30px;}
@media(max-width:820px){.chapters{grid-template-columns:1fr;padding-left:16px;}}
.ch{display:block;padding:18px 0;border-top:1px solid var(--line);transition:border-color .2s ease;}
.ch:hover{border-top-color:var(--tc,var(--coral));}
.ch-num{font-family:var(--orb);font-weight:900;font-size:44px;line-height:1;margin-bottom:10px;font-variant-numeric:tabular-nums;}
.ch-name{font-family:var(--orb);font-weight:700;font-size:16px;margin-bottom:6px;}
.ch-ver{font-family:var(--mono);font-size:11px;color:var(--dim);margin-bottom:8px;}
.ch-body{font-size:13px;color:var(--mute);line-height:1.5;}
.ch-pending{opacity:.55;}
.ch-pending .ch-num{opacity:.5;}

.srow{display:flex;align-items:baseline;gap:clamp(16px,3vw,32px);padding:24px 0;border-bottom:1px solid var(--line-soft);transition:padding-left .2s ease;}
.srow:hover{padding-left:10px;}
.srow-n{font-family:var(--orb);font-weight:900;font-size:clamp(28px,3.4vw,42px);color:var(--coral);opacity:.3;width:70px;flex:0 0 70px;}
.srow:hover .srow-n{opacity:.85;}
.srow-label{font-family:var(--orb);font-weight:700;font-size:clamp(17px,1.9vw,24px);width:280px;flex:0 0 280px;}
.srow-body{font-size:15px;color:#9AA3B2;flex:1;}
.srow-arrow{color:var(--coral);opacity:0;transition:opacity .2s ease;}
.srow:hover .srow-arrow{opacity:1;}
@media(max-width:820px){.srow{flex-wrap:wrap;gap:8px;}.srow-label{width:auto;flex:1 1 auto;}.srow-body{flex:1 1 100%;}}

.cta{margin-top:80px;padding:44px 0 0;border-top:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;gap:24px;flex-wrap:wrap;}
.cta div{font-family:var(--orb);font-weight:900;font-size:clamp(22px,3vw,30px);}
.cta a{font-family:var(--orb);font-weight:700;font-size:17px;color:var(--pink);}
.cta a:hover{text-decoration:underline;}

footer{margin-top:64px;padding-top:22px;border-top:1px solid var(--line-soft);color:var(--dim);font-size:13px;}
.flinks{margin-top:12px;display:flex;gap:22px;flex-wrap:wrap;font-family:var(--mono);font-size:12px;}
.flinks a{color:var(--mute);}
.flinks a:hover{color:var(--coral);}

[data-reveal]{opacity:0;transform:translateY(18px);}
[data-reveal].in{opacity:1;transform:none;transition:opacity .55s ease,transform .55s ease;}

@media (prefers-reduced-motion: reduce){
  .glow{animation:none;}
  .mark,.mark.go{animation:none;background-size:100% 100%;color:#0A0E14;}
  [data-reveal]{opacity:1;transform:none;transition:none;}
}
</style>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-KT4JJE05JH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-KT4JJE05JH');
</script>
</head>
<body>
<div class="stage">
  <div class="ghost">04</div>
  <div class="glow"></div>
  <div class="inner">

    <div class="topbar">
      <div class="brand"><img src="__LOGO__" alt="" /><span>HIGHLIGHT</span></div>
      <div class="nav">
        <a href="__S__/learn-and-explore/getting-started">START HERE</a>
        <a href="__S__/changelogs">CHANGELOG</a>
        <a href="__S__/ideas-and-feedback">FEEDBACK</a>
      </div>
    </div>

    <div class="kicker">RELEASE LOG</div>
    <h1 class="h1-a">MARK THE WORDS</h1>
    <h1 class="h1-b"><span class="mark">YOU'RE WATCHING FOR</span></h1>
    <p class="lede">Colour-coded word lists, combination rules, pattern rules, tooltips, folders, and an alert for the words that have gone quiet. Everything runs on your device.</p>

    <div class="tracks">__TRACKS__</div>

    <div class="block">
      <details class="drop" open>
        <summary><span class="chev"></span><span class="drop-title">CHANGELOG</span><span class="drop-hint">3 BROWSERS &middot; 5 CHAPTERS</span></summary>
        __COLS__
      </details>
    </div>

    <div class="block">
      <div class="srule"><span>START HERE</span><span class="bar"></span></div>
      __START__
    </div>

    <div class="cta">
      <div>GOT AN IDEA?</div>
      <a href="__S__/ideas-and-feedback">Ideas &amp; Feedback &#8594;</a>
    </div>

    <footer>
      Highlight is a personal project, unaffiliated with any employer. Everything runs locally in your browser.
      <div class="flinks">
        <a href="__S__/about">About</a>
        <a href="__S__/learn-and-explore/presets">Presets</a>
        <a href="__S__/legal/privacy-policy">Privacy</a>
        <a href="__S__/legal/terms-of-service">Terms</a>
      </div>
    </footer>

  </div>
</div>
<script>
(function(){
  var reduce=false;
  try{reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  var mark=document.querySelector('.mark');
  var nodes=[].slice.call(document.querySelectorAll('[data-reveal]'));
  nodes.forEach(function(n){
    var sibs=n.parentNode?[].filter.call(n.parentNode.children,function(c){return c.hasAttribute&&c.hasAttribute('data-reveal');}):[n];
    n.style.transitionDelay=(Math.max(0,sibs.indexOf(n))*90)+'ms';
  });
  function countUp(n){
    var el=n.querySelector('[data-count-to]');
    if(!el||el.getAttribute('data-done'))return;
    el.setAttribute('data-done','1');
    var target=parseInt(el.getAttribute('data-count-to'),10);
    if(isNaN(target)){el.textContent=el.getAttribute('data-count-to');return;}
    var pad=String(el.getAttribute('data-count-to')).length;
    if(reduce){el.textContent=el.getAttribute('data-count-to');return;}
    var t0=null;
    function frame(ts){
      if(t0===null)t0=ts;
      var p=Math.min(1,(ts-t0)/650), e=1-Math.pow(1-p,3);
      el.textContent=String(Math.round(target*e)).padStart(pad,'0');
      if(p<1)requestAnimationFrame(frame); else el.textContent=el.getAttribute('data-count-to');
    }
    requestAnimationFrame(frame);
  }
  if(reduce||!('IntersectionObserver' in window)){
    if(mark)mark.classList.add('go');
    nodes.forEach(function(n){n.classList.add('in');countUp(n);});
    return;
  }
  if(mark){
    var mo=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ mark.classList.add('go'); mo.unobserve(mark); } });
    },{threshold:.35});
    mo.observe(mark);
  }
  document.addEventListener('toggle',function(e){
    var d=e.target;
    if(!d||!d.open||!d.querySelectorAll)return;
    [].forEach.call(d.querySelectorAll('[data-reveal]'),function(n,i){
      setTimeout(function(){ n.classList.add('in'); countUp(n); }, i*90);
    });
  },true);
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      var n=e.target;
      n.classList.add('in');
      var d=parseInt(n.style.transitionDelay,10)||0;
      setTimeout(function(){countUp(n);},d+140);
      io.unobserve(n);
    });
  },{rootMargin:'0px 0px -8% 0px',threshold:.12});
  nodes.forEach(function(n){io.observe(n);});
})();
</script>
</body>
</html>
'''

out = (HTML
       .replace('__ORB700__', orb700)
       .replace('__ORB900__', orb900)
       .replace('__TRACKS__', ''.join(track_install(t) for t in TRACKS))
       .replace('__COLS__', ''.join(track_column(t) for t in TRACKS))
       .replace('__START__', ''.join(start_row(s) for s in START))
       .replace('__S__', S)
       .replace('__LOGO__', logo))

io.open(os.path.join(W, 'index.html'), 'w', encoding='utf-8').write(out)
print('index rebuilt in 1c direction:', len(out), 'bytes')
