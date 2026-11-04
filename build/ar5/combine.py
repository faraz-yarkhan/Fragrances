import json,re
D=open('fragrance-shortlist.html').read(); A=open('arabian-houses.html').read()
def part(s,start,end):
    i=s.find(start); j=s.find(end,i); return s[i+len(start):j]
def grab(s):
    ph=part(s,'const PH=','};\n')+'}'
    b='['+part(s,'const B=[','];\n')+']'
    return ph,b,part(s,'<div class="eyebrow">','</div>'),part(s,'<h1>','</h1>'),part(s,'<p class="lede">','</p>')
dph,db,deb,dh1,dle=grab(D); aph,ab,aeb,ah1,ale=grab(A)
js=lambda x:json.dumps(x,ensure_ascii=False)
def rr(s):
    i=s.find('const R=');j=s.find('];\n',i)+1;a=json.loads(s[i+8:j])
    i=s.find('const RPH=');j=s.find('};\n',i)+1;b=json.loads(s[i+10:j]);return a,b
Ra,Pa=rr(D);Rb,Pb=rr(A)
RALL=sorted(Ra+Rb,key=lambda x:(-x['s'],-x['c']));Pa.update(Pb)
data=('const P="https://www.parfumo.com/Perfumes/";\nconst DS={\n designer:{eyebrow:%s,h1:%s,lede:%s,open:"ysl",PH:%s,B:%s},\n arabian:{eyebrow:%s,h1:%s,lede:%s,open:"rayhaan",PH:%s,B:%s}\n};\nlet PH,B,C;\n'%(js(deb),js(dh1),js(dle),dph,db,js(aeb),js(ah1),js(ale),aph,ab))
data+='const R='+json.dumps(RALL,ensure_ascii=False)+';\nconst RPH='+json.dumps(Pa)+';\n'
s=D
i=s.find('const PH=');j=s.find('function buyUrl')
occ=part(s,'const OCC=',';\n')
s=s[:i]+'const OCC='+occ+';\n'+data+s[j:]
s=s.replace('let G="men",query="";const openSet=new Set(["ysl"]);','let G="men",query="";const openSet=new Set();')
s=s.replace('document.querySelectorAll(".switch button").forEach(btn=>btn.addEventListener("click",()=>{G=btn.dataset.g;document.querySelectorAll(".switch button").forEach(x=>x.setAttribute("aria-pressed",x===btn));render()}));','document.querySelectorAll(".switch button[data-g]").forEach(btn=>btn.addEventListener("click",()=>{G=btn.dataset.g;document.querySelectorAll(".switch button[data-g]").forEach(x=>x.setAttribute("aria-pressed",x===btn));render()}));')
old_idx='const idx=document.getElementById("index");idx.innerHTML=B.map(b=>`<button data-id="${b.id}">${esc(b.name)}</button>`).join("");'
assert old_idx in s
s=s.replace(old_idx,'const idx=document.getElementById("index");\nfunction setColl(c){C=DS[c]?c:"designer";const d=DS[C];PH=d.PH;B=d.B;openSet.clear();openSet.add(d.open);document.getElementById("eyebrow").innerHTML=d.eyebrow;document.getElementById("h1").innerHTML=d.h1;document.getElementById("lede").innerHTML=d.lede;document.title=C==="arabian"?"Arabian Houses Shortlist":"Designer Fragrance Shortlist";document.querySelectorAll(".coll button").forEach(x=>x.setAttribute("aria-pressed",x.dataset.c===C));idx.innerHTML=B.map(b=>`<button data-id="${b.id}">${esc(b.name)}</button>`).join("");try{history.replaceState(null,"","#"+C)}catch(e){}}\ndocument.querySelectorAll(".coll button").forEach(btn=>btn.addEventListener("click",()=>{setColl(btn.dataset.c);render();window.scrollTo(0,0)}));\nsetColl(location.hash.slice(1));')
s=s.replace('<div class="eyebrow">'+deb+'</div>','<div class="eyebrow" id="eyebrow"></div>').replace('<h1>'+dh1+'</h1>','<h1 id="h1"></h1>').replace('<p class="lede">'+dle+'</p>','<p class="lede" id="lede"></p>')
s=s.replace('<header>','<header>\n    <div class="switch coll" role="group" aria-label="Collection"><button data-c="designer" aria-pressed="true">Designer &amp; niche</button><button data-c="arabian" aria-pressed="false">Arabian houses</button></div>',1)
s=s.replace("It appears only on Zara picks, and Zara doesn't confirm it.","The houses rarely confirm it themselves.")
s=s.replace('.switch button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}','.switch button[aria-pressed="true"]{background:var(--ink);color:var(--bg)}\n.coll{margin-bottom:6px}.coll button{padding:7px 16px;font-size:14px}',1)
R=[("I could not confirm notes for the men's line.","Notes for the men's line are not confirmed."),("among the lowest on this page, so I've removed it.","among the lowest on this page, so it isn't included."),("I couldn't confirm notes for some.","Notes for some are not confirmed."),("so they've dropped off.","so they aren't included."),("so both are out of this list.","so neither is included."),("<b>Rating change:</b>","<b>Left out:</b>")]
for a,b in R:
    s=s.replace(a,b)
k=s.find('<style>');headbits=s[:k].replace('<title>Designer Fragrance Shortlist</title>\n','').replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
rest=s[k:];e=rest.find('</style>')+8
out=('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<title>Fragrance Shortlists</title>\n<meta name="description" content="Ranked men\'s and women\'s fragrance rankings of every rated scent for 27 designer and niche houses and 27 Arabian houses, with Parfumo ratings, notes and bottle photos.">\n'+headbits+rest[:e]+'\n</head>\n<body>\n'+rest[e:].lstrip('\n')+'\n</body>\n</html>\n')
open('share/fragrance-shortlists.html','w').write(out)
print(len(out)//1024,'KB')
