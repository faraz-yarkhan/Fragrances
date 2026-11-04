import json,re,csv,sys,os,glob
import os; S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
sys.path.insert(0,S+'d10')
from genders import gender
CONC=[('Eau de Toilette Concentrée','EDT Concentrée'),('EdT Concentrée','EDT Concentrée'),('Eau de Parfum Intense','EDP Intense'),('Eau de Toilette Intense','EDT Intense'),('Eau de Toilette','EDT'),('Eau de Parfum','EDP'),('Esprit de Parfum','Esprit de Parfum'),('Cologne Intense','Cologne Intense')]
def split(n):
    c=''
    for a,b in CONC:
        if n.endswith(' '+a): n=n[:-len(a)-1]; c=b; break
    n=re.sub(r'\s*\((\d{4})\)\s*',' ',n).strip()
    return n,c
adj=lambda r,c:(c*r+100*7.8)/(c+100)
key=lambda p:'p_'+p.split('/')[1][:6]
R=[]
# ---- designer: raw Parfumo brand lists
dB=json.load(open(S+'d10/newB.json')); IDMAP={'tf':'tomford'}
dname={b['id']:b['name'] for b in dB}
for f in sorted(glob.glob(S+'d10/raw/b*.txt')):
    cur=None
    for line in open(f):
        line=line.strip()
        if line.startswith('## '): cur=re.sub(r'2$','',line[3:].strip()); continue
        if '|' not in line or not cur: continue
        p=[x.strip() for x in line.split('|')]
        if len(p)<5: continue
        try: r=float(p[2]); c=int(p[3])
        except: continue
        n,cc=split(p[0]); g=gender(cur,p[0])
        R.append(dict(n=n,b=dname[IDMAP.get(cur,cur)],k='d',g=g,r=r,c=c,y=p[1] if re.match(r'^\d{4}$',p[1]) else '',cc=cc,p=p[4]))
# ---- arabian: candidate lists
aB=json.load(open(S+'ar5/newB10.json')); aname={b['id']:b['name'] for b in aB}
namekey={}
for mf in ('me_map.txt','me2_map.txt'):
    for l in open(S+mf):
        if '|' in l: k,p=l.strip().split('|',1); namekey[p]=k
rows=[r+['']*(7-len(r)) for r in csv.reader(open(S+'ar5/cand10.tsv'),delimiter='\t') if r and not r[0].startswith('#')]
for h,n,r,c,g,p,y in rows:
    R.append(dict(n=n,b=aname[h],k='a',g=g,r=float(r),c=int(c),y=y,cc='',p=p,key=namekey.get(p)))
for b in aB:   # Arabiyat picks have no list data
    if b['id']!='arabiyat': continue
    seen=set()
    for g in ('men','women'):
        for f in b[g]:
            if f['n'] in seen: continue
            seen.add(f['n']); m=re.match(r'([\d.]+) \(([\d,]+)\)',f['d'])
            R.append(dict(n=f['n'],b=b['name'],k='a',g='u' if 'unisex' in f['c'] else 'm',r=float(m[1]),c=int(m[2].replace(',','')),y='',cc='',p=None,key=f['img']))
# dedupe by (brand, path or name), keep the higher count
U={}
for x in R:
    k2=(x['b'],x['p'] or x['n'])
    if k2 not in U or x['c']>U[k2]['c']: U[k2]=x
R=[x for x in U.values() if x['c']>=10]
for x in R:
    x['s']=round(adj(x['r'],x['c']),3)
    x['img']=x.pop('key',None) or (key(x['p']) if x['p'] else None)
R.sort(key=lambda x:(-x['s'],-x['c']))
json.dump(R,open(S+'rank/R.json','w'),ensure_ascii=False)
print(len(R),'ranked;',sum(x['k']=='d' for x in R),'designer',sum(x['k']=='a' for x in R),'arabian')
print('genders',{g:sum(x['g']==g for x in R) for g in 'mfu?'})
for x in R[:15]: print(x['n'],'|',x['b'],x['r'],x['c'],x['g'],x['s'])
