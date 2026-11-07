(function(){
  function setupToggles(){
    [].forEach.call(document.querySelectorAll('.ch-toggle'),function(btn){
      btn.addEventListener('click',function(){
        var panel=document.getElementById(btn.getAttribute('aria-controls'));
        var open=btn.getAttribute('aria-expanded')==='true';
        btn.setAttribute('aria-expanded',String(!open));
        if(panel)panel.classList.toggle('open',!open);
        var label=btn.querySelector('.ch-toggle-text');
        if(label)label.textContent=open?btn.getAttribute('data-label-more'):btn.getAttribute('data-label-less');
      });
    });
  }

  var reduce=false;
  try{reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}

  function setupToc(){
    [].forEach.call(document.querySelectorAll('.toc a[href^="#"]'),function(a){
      a.addEventListener('click',function(e){
        var target=document.getElementById(a.getAttribute('href').slice(1));
        if(!target)return;
        e.preventDefault();
        target.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'});
      });
    });
  }

  setupToggles();
  setupToc();

  if(reduce||!('IntersectionObserver' in window))return;

  document.documentElement.classList.add('hlx-armed');

  [].forEach.call(document.querySelectorAll('.kicker'),function(k){
    k.style.setProperty('--chars',Math.max(1,k.textContent.length));
    k.classList.add('is-typing');
  });

  [].forEach.call(document.querySelectorAll('.h1-a'),function(h){
    var text=h.textContent;
    for(var i=0;i<2;i++){
      var s=document.createElement('span');
      s.className='glx';
      s.setAttribute('aria-hidden','true');
      s.textContent=text;
      h.appendChild(s);
    }
    h.classList.add('is-glitch');
  });

  var SEL='[data-reveal],h1,.ch-num,.chapter-num,.srule,.next,.rail,.ident,.toc,.form-embed,.chapter-top';
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  },{threshold:.12});

  function clearDelay(e){
    if(e.target!==this||e.propertyName!=='opacity')return;
    this.style.transitionDelay='';
    this.removeEventListener('transitionend',clearDelay);
  }

  function handle(n){
    if(n.hlxSeen)return;
    n.hlxSeen=true;
    if(n.hasAttribute('data-reveal')){
      var sibs=n.parentNode?[].filter.call(n.parentNode.children,function(c){return c.hasAttribute('data-reveal');}):[n];
      var i=Math.max(0,sibs.indexOf(n));
      n.style.transitionDelay=((i%8)*90)+'ms';
      n.addEventListener('transitionend',clearDelay);
    }
    io.observe(n);
  }

  function scan(root){
    if(root.nodeType!==1)return;
    if(root.matches&&root.matches(SEL))handle(root);
    [].forEach.call(root.querySelectorAll(SEL),handle);
  }

  scan(document.body);

  var queued=false;
  var pending=[];
  if('MutationObserver' in window){
    new MutationObserver(function(ms){
      ms.forEach(function(m){[].push.apply(pending,m.addedNodes);});
      if(queued)return;
      queued=true;
      requestAnimationFrame(function(){
        queued=false;
        var list=pending;
        pending=[];
        list.forEach(scan);
      });
    }).observe(document.body,{childList:true,subtree:true});
  }
})();
