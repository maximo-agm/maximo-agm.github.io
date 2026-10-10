/* Highlight website: the shared top menu.
   Every page has <div class="nav" data-hlx-nav></div> followed by this script.
   To change the menu on every page at once, edit MENU below and push.
   A page can mark its own entry with data-current="home|ideas", which shows
   that entry as plain text instead of a link.
   CHROME STAYS AT 2.1.0: never add a Chrome entry above 2.1.0 here until the
   owner says so (see docs/Website Tree.txt). */
(function(){
  var BASE='https://sites.google.com/view/highlight-mxm/';

  var MENU=[
    {key:'home',label:'HOME',href:'home'},
    {label:'LEARN & EXPLORE',items:[
      {label:'Getting started',href:'learn-and-explore/getting-started'},
      {label:'Feature tour',href:'learn-and-explore/feature-tour'},
      {label:'Pattern rules',href:'learn-and-explore/regex-rules'},
      {label:'Presets',href:'learn-and-explore/Presets220'},
      {label:'FAQ',href:'learn-and-explore/faq-and-troubleshooting'}
    ]},
    {label:'CHANGELOG',wide:true,groups:[
      {label:'Chrome',tc:'t-chrome',items:[
        {label:'v2.1.0 — The Release',href:'changelogs/chrome-changelogs/210Chrome-A7K29Xm4'},
        {label:'Updates are planned'}
      ]},
      {label:'Edge',tc:'t-edge',items:[
        {label:'v2.3.1 — The Weight of a Presence',href:'changelogs/edge-changelogs/231Edge-EsufWHwz'},
        {label:'v2.3.2 — The Weave of a Style',href:'changelogs/edge-changelogs/232Edge-pc73FLTV'},
        {label:'v2.3.3 — The Pitch of a Sound',href:'changelogs/edge-changelogs/233Edge-Dq2Vn8Lw'},
        {label:'v2.3.4 — The Pulse of a Change',href:'changelogs/edge-changelogs/234Edge-yAa5h3j5'},
        {label:'v2.4.0 — The Colour of a Moment',href:'changelogs/edge-changelogs/240Edge-Vb4bFpIu'}
      ]},
      {label:'Firefox',tc:'t-firefox',items:[
        {label:'v2.3.0 — The Shape of the Unwritten',href:'changelogs/firefox-changelogs/230Firefox-F4h6T2z9'},
        {label:'v2.3.1 — The Weight of a Presence',href:'changelogs/firefox-changelogs/231Firefox-M1x8R5v3'},
        {label:'v2.3.2 — The Weave of a Style',href:'changelogs/firefox-changelogs/232Firefox-hOVRhSBP'},
        {label:'v2.3.3 — The Pitch of a Sound',href:'changelogs/firefox-changelogs/233Firefox-Xs5Tc3Hb'},
        {label:'v2.3.4 — The Pulse of a Change',href:'changelogs/firefox-changelogs/234Firefox-yedkCB5l'},
        {label:'v2.4.0 — The Colour of a Moment',href:'changelogs/firefox-changelogs/240Firefox-L8AC5DJ8'}
      ]}
    ]},
    {key:'ideas',label:'IDEAS & FEEDBACK',href:'ideas-and-feedback'}
  ];

  function el(tag,cls,text){
    var n=document.createElement(tag);
    if(cls)n.className=cls;
    if(text)n.textContent=text;
    return n;
  }

  function link(item,cls){
    if(!item.href)return el('span',(cls?cls+' ':'')+'navsub-disabled',item.label);
    var a=el('a',cls,item.label);
    a.href=BASE+item.href;
    return a;
  }

  function dropdown(entry){
    var d=el('details','navdrop');
    d.setAttribute('name','navdrop');
    var s=el('summary','',entry.label+' ');
    s.appendChild(el('span','navchev'));
    d.appendChild(s);
    var menu=el('div','navmenu'+(entry.wide?' navmenu-wide':''));
    (entry.items||[]).forEach(function(it){menu.appendChild(link(it));});
    (entry.groups||[]).forEach(function(g){
      var box=el('div','navgroup');
      var head=el('div','navgroup-label '+g.tc);
      head.appendChild(el('span','nd'));
      head.appendChild(document.createTextNode(g.label));
      box.appendChild(head);
      g.items.forEach(function(it){box.appendChild(link(it,'navsub'));});
      menu.appendChild(box);
    });
    d.appendChild(menu);
    return d;
  }

  function render(host){
    if(host.hlxNavDone)return;
    host.hlxNavDone=true;
    var current=host.getAttribute('data-current');
    while(host.firstChild)host.removeChild(host.firstChild);
    MENU.forEach(function(entry){
      if(entry.items||entry.groups)host.appendChild(dropdown(entry));
      else if(entry.key&&entry.key===current)host.appendChild(el('span','navcurrent',entry.label));
      else host.appendChild(link(entry));
    });
  }

  function run(){[].forEach.call(document.querySelectorAll('[data-hlx-nav]'),render);}

  run();
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);
})();
