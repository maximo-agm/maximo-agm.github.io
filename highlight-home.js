(function(){
  var reduce=false;
  try{reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  if(reduce||!('IntersectionObserver' in window))return;
  var SEL='[data-reveal],.ch-num,.chapter-num';
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  },{threshold:.12});
  function stagger(n){
    var p=n.parentNode;
    if(!p)return;
    var sibs=[].filter.call(p.children,function(c){return c.hasAttribute&&c.hasAttribute('data-reveal');});
    n.style.transitionDelay=(Math.max(0,sibs.indexOf(n))%8*90)+'ms';
    n.addEventListener('transitionend',function clear(ev){
      if(ev.propertyName!=='opacity')return;
      n.style.transitionDelay='';
      n.removeEventListener('transitionend',clear);
    });
  }
  function watch(){
    [].forEach.call(document.querySelectorAll(SEL),function(n){
      if(n.hlxSeen)return;
      n.hlxSeen=true;
      if(n.hasAttribute('data-reveal'))stagger(n);
      io.observe(n);
    });
  }
  document.documentElement.classList.add('hlx-armed');
  watch();
  var queued=false;
  new MutationObserver(function(){
    if(queued)return;
    queued=true;
    requestAnimationFrame(function(){queued=false;watch();});
  }).observe(document.body,{childList:true,subtree:true});
})();
