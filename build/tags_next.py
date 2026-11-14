"""List the next scents to tag, and check tags.tsv.
Usage: python3 build/tags_next.py [N]   (default 40)"""
import sys,re,os
S=os.path.dirname(os.path.abspath(__file__))+'/'
nz=lambda t:re.sub(r'[^a-z0-9]','',t.lower())
Q=[l.rstrip('\n').split('\t') for l in open(S+'tags_queue.tsv',encoding='utf-8') if not l.startswith('#') and l.strip()]
qk={(q[0],nz(q[1])) for q in Q}
done=set();bad=[]
for i,l in enumerate(open(S+'tags.tsv',encoding='utf-8'),1):
    if l.startswith('#') or l.startswith('house\t') or not l.strip(): continue
    f=l.rstrip('\n').split('\t')
    if len(f)<10: bad.append((i,'needs 10 tab-separated columns'));continue
    if (f[0],nz(f[1])) not in qk: bad.append((i,f'no such scent: {f[0]} | {f[1]}'))
    if not f[2].strip(): bad.append((i,'accords empty'))
    for x in f[3:9]:
        if x.strip() and not (x.strip().isdigit() and 0<=int(x)<=100): bad.append((i,f'bad number {x!r}'))
    done.add((f[0],nz(f[1])))
todo=[q for q in Q if (q[0],nz(q[1])) not in done]
n=int(sys.argv[1]) if len(sys.argv)>1 else 40
print(f'{len(done)} tagged, {len(todo)} to go')
for b in bad: print('PROBLEM line %d: %s'%b)
for q in todo[:n]: print('\t'.join(q))
