import json,re
import os; S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
R=json.load(open(S+'rank/R.json')); RPHall=json.load(open(S+'rank/RPH.json'))
NOTES={
 'ysl':"<b>Unisex scents:</b> Tuxedo and Babycat are from YSL's unisex Le Vestiaire range, so they appear on both tabs.",
 'jc':"<b>Women-focused:</b> Jimmy Choo's range leans women's, so the men's list is short.",
 'armani':"<b>Short list:</b> only Armani's 20 most popular scents could be read from Parfumo. Acqua di Giò Profumo has been replaced by Acqua di Giò Parfum, so it may be hard to find.",
 'lv':"<b>Mostly unisex:</b> Louis Vuitton markets most of its range to everyone, so the two tabs overlap a lot. Prices are high, around twice Tom Ford Private Blend.",
 'dior':"<b>Gaps:</b> Parfumo's 40 most popular Dior list didn't include Sauvage Parfum or Dior Homme (2020), so they're missing here. Search for them and use Look up.",
 'tiffany':"<b>Women-focused:</b> Tiffany has only two men's scents with enough ratings. The 1989 Tiffany for Men Cologne rates well but is an old release and may be hard to find.",
 'rl':"<b>Short list:</b> only Ralph Lauren's 20 most popular scents could be read from Parfumo, and three of them are women's.",
 'montblanc':"<b>Short list:</b> only Montblanc's 20 most popular scents could be read from Parfumo, three of them women's plus the unisex Patchouli Ink.",
 'rabanne':"<b>Weak scorers included:</b> Rabanne's lower-rated scents, such as Phantom and Lady Million, sit near the bottom of the lists.",
 'gb':"<b>All unisex:</b> the whole range is unisex, so both tabs show the same list. About 20% concentration and tested in very humid conditions.",
 'tommy':"<b>Low scores:</b> Freedom (3.9) and several others sit at the bottom. Many Tommy scents have under 50 ratings.",
 'xerjoff':"<b>Unisex house:</b> Xerjoff makes almost no gendered scents, so both tabs show nearly the same list.",
 'azzaro':"<b>Men-focused:</b> Eau Belle is the only women's Azzaro among its 20 most popular, so the women's tab is mostly unisex or short.",
 'tomford':"<b>Mostly unisex:</b> Tom Ford's Private Blend range is unisex, so the two tabs overlap a lot.",
 'versace':"<b>Short list:</b> only Versace's 20 most popular scents could be read from Parfumo.",
 'zara':"<b>Unconfirmed labels:</b> Zara sells some scents in both its men's and women's sections, so several are marked 'gender not confirmed' and appear on the men's tab.",
 'creed':"<b>Women's tab:</b> Creed's women's scents rate well below its men's and unisex ones, so unisex Creeds lead that tab.",
 'jomalone':"<b>Layering house:</b> Jo Malone is officially unisex. The women's labels for its florals come from Fragrantica. Expect 3 to 5 hours from the Colognes.",
 'lelabo':"<b>All unisex:</b> every Le Labo scent is unisex, so both tabs show the same list. Santal 33 is the famous one but rates only 7.3.",
 'burberry':None,'prada':None,
 'rayhaan':"<b>Women's tab:</b> Rayhaan makes almost no women's-labelled scents. Divine is the only one with enough ratings, so the rest of that tab is unisex.",
 'lattafa':"<b>Partial list:</b> only Lattafa's 40 most popular scents could be read from Parfumo. Few are labelled women's, so unisex scents make up most of the women's tab.",
 'hawas':"<b>Heads up:</b> Hawas is a Rasasi line, not a separate brand. Hawas for Her's 8.4 comes from just 34 ratings.",
 'armaf':"<b>Women's line:</b> only three women's Armaf scents have enough ratings, so the rest of the women's tab is unisex.",
 'arabiyat':"<b>Few rated scents:</b> most Arabiyat Prestige scents have under 50 ratings on Parfumo, so only these are ranked.",
 'fw':"<b>Same family:</b> French Avenue is a Fragrance World label and has its own row. Few Fragrance World scents are labelled women's or unisex, so the women's tab is short.",
}
CSS='''
.totop{align-self:flex-end;font:inherit;font-size:13px;font-weight:600;color:var(--accent);background:transparent;border:1px solid var(--line);border-radius:999px;padding:6px 14px;cursor:pointer}
.totop:hover{border-color:var(--accent)}
.rlist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:10px}
.ritem{display:grid;grid-template-columns:72px 1fr;gap:12px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px}
.rpic{display:flex;flex-direction:column;align-items:center;gap:6px}
.rnum{font-family:var(--mono);font-size:12px;color:var(--muted)}
.rimg{width:72px;height:72px;object-fit:contain;background:#fff;border-radius:10px;padding:3px;display:block}
.rpic svg{width:44px}
.rbody{min-width:0;display:flex;flex-direction:column;gap:6px}
.rname{font-family:var(--display);font-size:19px;font-weight:700;line-height:1.2;margin:0}
.rmeta{font-family:var(--mono);font-size:11.5px;color:var(--muted)}
.rrow{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.updated{font-family:var(--mono);font-size:11.5px;color:var(--muted);margin:0}
.updated b{color:var(--ink);font-weight:600}
.lookup{display:flex;flex-direction:column;gap:10px}
.lookup[hidden]{display:none}
.lkrow{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:13.5px;color:var(--muted)}
.lkbtn{font:inherit;font-size:13.5px;font-weight:600;color:var(--bg);background:var(--accent);border:0;border-radius:999px;padding:7px 16px;cursor:pointer}
.lkbtn:disabled{opacity:.6;cursor:default}
.lkout{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px;display:flex;flex-direction:column;gap:8px}
.lkout[hidden]{display:none}
.lkout h3{font-family:var(--display);font-size:22px;margin:0;line-height:1.2}
.lkout .lklabel{font-family:var(--mono);font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted)}
.lkout p{margin:0;font-size:14px}
.lkout .warn{font-size:12.5px;color:var(--muted);font-style:italic}
.lklinks{display:flex;flex-wrap:wrap;gap:6px}
.lklinks a{font-size:12.5px;font-weight:600;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:999px;padding:4px 12px}
.lklinks a:hover{border-color:var(--accent);color:var(--accent)}
'''
RENDER=r'''function render(){
  const q=query.trim().toLowerCase();let shown=0;
  el.innerHTML=B.map(b=>{
    const all=houseRows(b);
    const rows=all.map((x,i)=>({x,i})).filter(({x})=>!q||(b.name+" "+x.n+" "+(x.f?x.f.notes.join(" ")+" "+(x.f.insp||"")+" "+x.f.s:"")).toLowerCase().includes(q));
    if(!rows.length&&(q||!b.note))return"";shown++;
    const open=!!q||openSet.has(b.id);const tab=G==="men"?"men's":"women's";
    return `<section class="brand${open?" open":""}" id="${b.id}">
    <button class="brand-head" aria-expanded="${open}" aria-controls="p-${b.id}" data-id="${b.id}">
      <span class="bname">${esc(b.name)}<span class="tag">${esc(b.tag)}</span></span>
      <span class="bmeta">${all.length?`No. 1 ${tab}: <b>${esc(all[0].n)}</b> · ${all.length} ranked${q?` · ${rows.length} match`:""}`:`No ${tab} scents with reliable data`}</span>
      <span class="chev" aria-hidden="true"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg></span>
    </button>
    <div class="panel" id="p-${b.id}" ${open?"":"hidden"}>
      ${b.note?`<p class="note">${b.note}</p>`:""}
      ${rows.length?`<ol class="rlist">${rows.map(({x,i})=>rowHTML(b,x,i)).join("")}</ol>`:""}
      <div class="sources">Sources: ${b.src.map(s=>`<a href="${s[1]}" target="_blank" rel="noopener">${esc(s[0])}</a>`).join("")}</div>
      <button class="totop" type="button">↑ Back to top</button>
    </div></section>`}).join("");
  document.getElementById("empty").hidden=shown>0;
  updateLookup(q,shown);
}'''
JS=r'''
const RPHOTO=k=>!k?null:((typeof DS!=="undefined"?(DS.designer.PH[k]||DS.arabian.PH[k]):PH[k])||RPH[k]||null);
const GL={m:"men",f:"women",u:"unisex","?":"gender not confirmed"};
const nrm=s=>s.toLowerCase().replace(/[^a-z0-9]/g,"");
const adj=(r,c)=>(c*r+780)/(c+100);
const HR={};
function houseRows(b){
  const key=(typeof C!=="undefined"?C:"")+b.id+G;if(HR[key])return HR[key];
  const picks=[...(b.men||[]),...(b.women||[])];
  const byImg={},byName={};picks.forEach(f=>{if(f.img)byImg[f.img]=byImg[f.img]||f;byName[nrm(f.n)]=byName[nrm(f.n)]||f});
  const used=new Set();
  const fk=f=>(f.img||"")+"|"+nrm(f.n);
  let L=R.filter(x=>x.b===b.name).map(x=>{const f=(x.img&&byImg[x.img])||byName[nrm(x.n)]||null;if(f)used.add(fk(f));return {...x,f}});
  for(const f of (b[G]||[])){ if(used.has(fk(f))||(f.img&&used.has(f.img+"|"))||L.some(x=>x.f&&(x.f.img&&x.f.img===f.img||nrm(x.f.n)===nrm(f.n))))continue;
    const m=/([\d.]+) \(([\d,]+)\)/.exec(f.d||"");if(!m)continue;
    const r=+m[1],c=+m[2].replace(/,/g,"");
    const g=/women/.test(f.c)?"f":/unisex/.test(f.c)?"u":(G==="men"?"m":"f");
    const y=(/\b(19|20)\d\d\b/.exec(f.c)||[""])[0];
    L.push({n:f.n,b:b.name,g,r,c,y,cc:"",s:adj(r,c),img:f.img,f});used.add(fk(f))}
  L=G==="men"?L.filter(x=>x.g!=="f"):L.filter(x=>x.g==="f"||x.g==="u");
  L.sort((a,b)=>b.s-a.s||b.c-a.c);
  return HR[key]=L;
}
function rowHTML(b,x,i){
  const f=x.f;const ph=(f&&f.img&&RPHOTO(f.img))||RPHOTO(x.img);
  const meta=[x.cc,x.y,GL[x.g]].filter(Boolean).join(" · ");
  return `<li class="ritem"><div class="rpic">${ph?`<img class="rimg" src="${ph}" alt="${esc(x.n)} bottle" width="72" height="72" loading="lazy">`:sketch(f&&f.fam)}<span class="rnum">No. ${i+1}</span></div>
  <div class="rbody"><h3 class="rname">${esc(x.n)}</h3>${meta?`<div class="rmeta">${esc(meta)}</div>`:""}
  <div class="rrow"><span class="data">Parfumo ${x.r} (${x.c.toLocaleString()})</span><a class="buy" href="${buyUrl(b,{n:x.n,c:x.cc})}" target="_blank" rel="noopener" aria-label="Buy ${esc(x.n)} on Google Shopping (opens in a new tab)">Buy on Google <span aria-hidden="true">↗</span></a></div>
  ${f&&f.insp?`<div class="insp">Inspired by: <b>${esc(f.insp)}</b></div>`:""}
  ${f&&f.notes.length?`<div class="notes">${f.notes.map(n=>`<span>${esc(n)}</span>`).join("")}</div>`:""}
  ${f&&f.s?`<p class="says">${esc(f.s)}</p>`:""}
  ${f&&f.w&&f.w.length?`<div class="when">${f.w.map(w=>`<span>${OCC[w]}</span>`).join("")}</div>`:""}
  </div></li>`;
}
document.addEventListener("click",e=>{if(!e.target.closest(".totop"))return;window.scrollTo({top:0,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"})});
/* ---- look up a fragrance that isn't listed ---- */
const lk=document.getElementById("lookup"),lkBtn=document.getElementById("lkbtn"),lkMsg=document.getElementById("lkmsg"),lkOut=document.getElementById("lkout");
let sampleFn=null,lkCtl=null,lkQ="";
(async()=>{try{if(window.claude&&claude.use)sampleFn=await claude.use("sample")}catch(e){}})();
const gq=s=>"https://www.google.com/search?q="+encodeURIComponent(s);
function lkLinks(name){return `<div class="lklinks"><a href="${gq(name+" site:fragrantica.com")}" target="_blank" rel="noopener">Fragrantica ↗</a><a href="${gq(name+" site:parfumo.com")}" target="_blank" rel="noopener">Parfumo ↗</a><a href="${gq(name+" perfume notes review")}" target="_blank" rel="noopener">Reviews ↗</a><a href="https://www.google.com/search?tbm=shop&q=${encodeURIComponent(name+" perfume")}" target="_blank" rel="noopener">Buy on Google ↗</a></div>`}
function updateLookup(q,shown){
  if(q.length<3){lk.hidden=true;return}
  lk.hidden=false;
  lkMsg.textContent=shown?"Not the one you're after?":"It isn't in these lists.";
  lkBtn.textContent=`Look up “${query.trim()}”`;
  if(lkQ&&lkQ!==q){lkOut.hidden=true;lkOut.innerHTML="";lkCtl&&lkCtl.abort();lkBtn.disabled=false}
}
const PROMPT=name=>`A shopper searched a fragrance list for "${name}" and it wasn't there. Identify the perfume they most likely mean and describe it from what you know.
Rules: only describe a perfume you are confident exists. If you are not sure which one they mean, or don't know it, set "found" to false and suggest up to 3 close real names in "didYouMean". Never invent notes, years or ratings: use null or [] when unsure. Ratings change, so do not give one.
Reply with JSON only, no prose:
{"found":true,"name":"","brand":"","year":null,"concentration":null,"gender":"men|women|unisex|null","family":"","top":[],"heart":[],"base":[],"description":"2-3 plain sentences: how it smells and wears","bestFor":["day","night","summer","winter","office","date"],"similar":[],"confidence":"high|medium|low","didYouMean":[]}`;
lkBtn.addEventListener("click",async()=>{
  const name=query.trim();if(!name)return;lkQ=name.toLowerCase();
  lkOut.hidden=false;
  if(!sampleFn){lkOut.innerHTML=`<span class="lklabel">Search the web</span><p>Open these searches for <b>${esc(name)}</b>:</p>${lkLinks(name)}<p class="warn">Live look-ups work when this page is opened on Claude. Here, these links search the web instead.</p>`;return}
  lkCtl&&lkCtl.abort();lkCtl=new AbortController();lkBtn.disabled=true;
  lkOut.innerHTML=`<span class="lklabel">Looking up</span><p>Thinking about “${esc(name)}”…</p>${lkLinks(name)}`;
  try{
    const d=await sampleFn.json(PROMPT(name),{signal:lkCtl.signal,modelTier:"default"});
    if(lkQ!==name.toLowerCase())return;
    if(!d||!d.found){lkOut.innerHTML=`<span class="lklabel">Not recognised</span><p>Claude couldn't confidently identify “${esc(name)}”.${d&&d.didYouMean&&d.didYouMean.length?` Did you mean: <b>${d.didYouMean.map(esc).join("</b>, <b>")}</b>?`:""}</p>${lkLinks(name)}`;return}
    const full=[d.brand,d.name].filter(Boolean).join(" ");
    const L=(t,a)=>a&&a.length?`<div><span class="lklabel">${t}</span><div class="notes">${a.map(n=>`<span>${esc(n)}</span>`).join("")}</div></div>`:"";
    const meta=[d.concentration,d.year,d.gender&&d.gender!=="null"?d.gender:null,d.family].filter(Boolean).map(String).join(" · ");
    lkOut.innerHTML=`<span class="lklabel">Look-up result</span><h3>${esc(d.name||name)}</h3><div class="rmeta">${esc(d.brand||"")}${meta?" · "+esc(meta):""}</div>
      ${d.description?`<p>${esc(d.description)}</p>`:""}${L("Top notes",d.top)}${L("Heart notes",d.heart)}${L("Base notes",d.base)}
      ${d.bestFor&&d.bestFor.length?`<div class="when">${d.bestFor.map(w=>`<span>${esc(w)}</span>`).join("")}</div>`:""}
      ${d.similar&&d.similar.length?`<div class="insp">Similar: <b>${d.similar.map(esc).join(", ")}</b></div>`:""}
      ${lkLinks(full||name)}
      <p class="warn">Written by Claude from what it knows, not read from a live web page${d.confidence&&d.confidence!=="high"?`, and its confidence is ${esc(d.confidence)}`:""}. Check notes and ratings on Fragrantica or Parfumo before buying.</p>`;
  }catch(e){
    if(e&&e.code==="cancelled")return;
    lkOut.innerHTML=`<span class="lklabel">Search the web</span><p>${e&&e.code==="not_granted"?"Look-ups need your permission to use Claude.":e&&e.code==="rate_limited"?"Too many look-ups just now. Try again in a minute.":"The look-up didn't work this time."} These searches still work:</p>${lkLinks(name)}`;
  }finally{lkBtn.disabled=false}
});
'''
LOOKUP_HTML='''
  <div class="lookup" id="lookup" hidden>
    <div class="lkrow"><span id="lkmsg"></span><button class="lkbtn" id="lkbtn" type="button">Look up</button></div>
    <div class="lkout" id="lkout" aria-live="polite" hidden></div>
  </div>'''
def rep(s,a,b):
    assert a in s,a[:70]; return s.replace(a,b,1)
def patch(f,coll):
    s=open(S+'rank/'+f+'.bak').read()
    rr=[dict(x) for x in R if x['k']==coll]
    i=s.find('const PH=');j=s.find('};\n',i)+1;PH=json.loads(s[i+9:j])
    used={x['img'] for x in rr if x['img']}
    rph={k:RPHall[k] for k in used if k not in PH and k in RPHall}
    for x in rr: x.pop('p',None); x.pop('k',None); x['s']=round(x['s'],3)
    i=s.find('const B=');j=s.find(';\n',i);B=json.loads(s[i+8:j])
    for b in B:
        if b['id'] in NOTES:
            if NOTES[b['id']] is None: b.pop('note',None)
            else: b['note']=NOTES[b['id']]
    if coll=='a':
        import sys;sys.path.insert(0,S+'rank');from houses_extra import fix;B=fix(B);NH=len(B)
    s=s[:i+8]+json.dumps(B,ensure_ascii=False)+s[j:]
    s=rep(s,'@media (max-width:480px)',CSS.strip()+'\n@media (max-width:480px)')
    s=re.sub(r'placeholder="Search a fragrance, note or inspiration[^"]*"','placeholder="Search any fragrance, brand or note"',s)
    s=rep(s,'</label>\n  <nav class="index"','</label>'+LOOKUP_HTML+'\n  <nav class="index"')
    i=s.find('function render(){');j=s.find('\n}\n',i)+2
    s=s[:i]+RENDER+s[j:]
    s=re.sub(r'<div class="eyebrow">Top 10 per tab · ',r'<div class="eyebrow">Every rated scent, ranked · ',s);s=re.sub(r'· \d+ houses · Middle',f'· {NH} houses · Middle',s) if coll=='a' else s
    lede=("Switch between men's and women's, then tap a house to see every scent from it that has a Parfumo rating, ranked from best to worst. "
          "Ratings are Parfumo community scores out of 10, with the number of ratings in brackets. Scores from only a few ratings are pulled towards the average, so a 9.0 from 10 people doesn't outrank an 8.5 from 400. "
          "Men's tabs show men's and unisex scents, and women's tabs show women's and unisex, so the two overlap. "
          "Lists cover each house's 20 to 40 most popular scents on Parfumo. If a fragrance isn't here, type it in the search box and press Look up.")
    s=re.sub(r'<p class="lede">.*?</p>','<p class="lede">'+lede+'</p>',s,count=1,flags=re.S)
    upd=open(S+'UPDATED').read().strip()
    s=s.replace('<p class="lede">'+lede+'</p>','<p class="lede">'+lede+'</p>\n    <p class="updated">Ratings last updated: <b>'+upd+'</b> · source: Parfumo</p>',1)
    data='const R='+json.dumps(rr,ensure_ascii=False)+';\nconst RPH='+json.dumps(rph)+';\n'
    k=s.find('function buyUrl'); s=s[:k]+data+s[k:]
    k=s.find('render();\n</script>'); assert k>0
    s=s[:k]+JS.strip()+'\n'+s[k:]
    s=s.replace('Nothing matches that search. Try one note, such as "vanilla", or clear the box.','Nothing in these lists matches that search. Use Look up above, or clear the box.')
    open(S+f,'w').write(s); print(f,len(rr),len(rph),len(s)//1024,'KB')
patch('fragrance-shortlist.html','d'); patch('arabian-houses.html','a')
