(function(){
  var reduce=false;
  try{reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;}catch(e){}
  var nodes=[].slice.call(document.querySelectorAll('[data-reveal]'));
  nodes.forEach(function(n){
    var sibs=n.parentNode?[].filter.call(n.parentNode.children,function(c){return c.hasAttribute&&c.hasAttribute('data-reveal');}):[n];
    n.style.transitionDelay=(Math.max(0,sibs.indexOf(n))*90)+'ms';
  });
  if(reduce||!('IntersectionObserver' in window)){
    nodes.forEach(function(n){n.classList.add('in');});
    return;
  }
  var io=new IntersectionObserver(function(es){
    es.forEach(function(e){
      if(!e.isIntersecting)return;
      e.target.classList.add('in');
      io.unobserve(e.target);
    });
  },{rootMargin:'0px 0px -8% 0px',threshold:.12});
  nodes.forEach(function(n){io.observe(n);});
})();
