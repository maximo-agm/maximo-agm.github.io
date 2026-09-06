(function(){
  var reduce=false;
  try{reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
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
    nodes.forEach(function(n){n.classList.add('in');countUp(n);});
    return;
  }
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
