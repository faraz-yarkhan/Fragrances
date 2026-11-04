"""Rebuild the fragrance pages from the data files in this folder.

Usage:  python3 build/run.py ["Month YYYY"]
Steps:  rank list -> fetch missing bottle photos -> change report -> pages -> index.html
"""
import json,os,sys,subprocess,io,base64,shutil,urllib.request,datetime
B=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(B)
def run(*a): subprocess.run(a,cwd=B,check=True)
upd=sys.argv[1] if len(sys.argv)>1 else datetime.date.today().strftime('%B %Y')
open(os.path.join(B,'UPDATED'),'w').write(upd+'\n')
old=json.load(open(os.path.join(B,'rank/R.json')))
# 1. ranked list
run('python3','rank/build_r.py')
R=json.load(open(os.path.join(B,'rank/R.json')))
# 2. thumbnails for anything without a photo
from PIL import Image
P=json.load(open(os.path.join(B,'rank/RPH.json')))
have=set(P)
for f in ('fragrance-shortlist.html.bak','arabian-houses.html.bak'):
    s=open(os.path.join(B,'rank',f)).read();i=s.find('const PH=');j=s.find('};\n',i)+1;have|=set(json.loads(s[i+9:j]))
miss=[x for x in R if x.get('img') and x['img'] not in have and x.get('p')]
fail=[]
for x in miss:
    try:
        req=urllib.request.Request(f"https://media.parfumo.com/perfumes/{x['p']}_1200.jpg?width=320&aspect_ratio=1:1",headers={'User-Agent':'fragrance-shortlists-build'})
        im=Image.open(io.BytesIO(urllib.request.urlopen(req,timeout=30).read())).convert('RGB');im.thumbnail((120,120))
        b=io.BytesIO();im.save(b,'WEBP',quality=72);P[x['img']]='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    except Exception as e: fail.append(f"{x['b']} – {x['n']}")
json.dump(P,open(os.path.join(B,'rank/RPH.json'),'w'))
# 3. change report
k=lambda x:(x['b'],x.get('p') or x['n'])
O={k(x):x for x in old}; N={k(x):x for x in R}
new=[x for kk,x in N.items() if kk not in O]; gone=[x for kk,x in O.items() if kk not in N]
moved=sorted([(N[kk]['r']-O[kk]['r'],N[kk]) for kk in N if kk in O and abs(N[kk]['r']-O[kk]['r'])>=0.2],key=lambda t:-abs(t[0]))
L=[f"# Refresh {upd}",f"{len(R)} scents ranked (was {len(old)}).","",f"## New ({len(new)})"]
L+=[f"- {x['b']}: {x['n']} — {x['r']} ({x['c']:,})" for x in sorted(new,key=lambda x:-x['c'])]
L+=["",f"## Rating moved 0.2 or more ({len(moved)})"]+[f"- {x['b']}: {x['n']} {d:+.1f} → {x['r']} ({x['c']:,})" for d,x in moved]
L+=["",f"## Dropped ({len(gone)})"]+[f"- {x['b']}: {x['n']}" for x in gone]
L+=["",f"## Photos that failed to download ({len(fail)})"]+[f"- {f}" for f in fail]
open(os.path.join(B,'CHANGES.md'),'w').write('\n'.join(L)+'\n')
# 4. pages
run('python3','rank/patch3.py'); run('python3','ar5/combine.py')
shutil.copy(os.path.join(B,'share/fragrance-shortlists.html'),os.path.join(ROOT,'index.html'))
# 5. syntax check
for f in ('fragrance-shortlist.html','arabian-houses.html','share/fragrance-shortlists.html'):
    s=open(os.path.join(B,f)).read();i=s.rfind('<script>');j=s.rfind('</script>')
    open('/tmp/_chk.js','w').write(s[i+8:j]);subprocess.run(['node','--check','/tmp/_chk.js'],check=True)
print('done:',upd,'|',len(R),'ranked |',len(new),'new |',len(moved),'moved |',len(fail),'photo failures')
