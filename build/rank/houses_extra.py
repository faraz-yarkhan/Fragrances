import json
import os; S=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
FT='https://www.fragrantica.com/'
NEW={
 'ibraq':dict(id='ibraq',name='Ibraheem Al Qurashi (Ibraq)',tag='Saudi · Since 1929',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/ibraheem-al-qurashi'],['Scent Verdict: Ibrahim Al-Qurashi','https://scentverdict.com/brand/ibrahim-al-qurashi'],['Fragrance Hub: French Tobacco','https://www.fragrancehub.co.uk/products/french-tobacco-edp-100ml-by-ibraheem-al-qurashi-ibraq']],
   note="<b>Tobacco specialists:</b> Ibraheem Al Qurashi, sold as Ibraq, is a Saudi house founded in Makkah in 1929. Its tobacco and Diamond lines take most of the ratings, but most scents have under 70, so the order could shift. Many gender labels aren't confirmed; the unisex ones come from Scent Verdict.",men=[],women=[]),
 'zimaya':dict(id='zimaya',name='Zimaya',tag='UAE · Afnan sister brand',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/zimaya'],['Scent Verdict: Zimaya','https://scentverdict.com/brand/zimaya'],['Fragrantica (gender labels)',FT]],
   note="<b>Afnan's sister brand:</b> Zimaya was launched in 2023 by Afnan's founder, Imran Fazlani. Sharaf Blend has far more ratings than anything else here. Only Zimaya's 20 most popular scents could be read from Parfumo. Kmart Australia stocks Zimaya Zukhruf Black.",men=[],women=[]),
 'dkhan':dict(id='dkhan',name='Dkhan',tag='Kuwait · Unrated',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/dkhan']],
   note="<b>Too new to rank:</b> Dkhan is a Kuwaiti house. Parfumo knows 16 of its scents, but only three have a rating, each from a single person, so nothing is ranked here. The range includes Kehl, Mashaer, Tabgh, Malaky, Aneeq, Leel, 1370, 3MQ, 3SHQ and 3BAQ (mostly in Intense versions), plus Hanin, Asassi, Musk Fruit and Musk Dkhan. Type any of them in the search box and use Look up.",men=[],women=[]),
}
def fix(B):
    ids=[b['id'] for b in B]
    if 'riiffs' not in ids:
        B.insert(ids.index('swiss')+1,json.load(open(S+'rank/riiffs_house.json')))
    a=next(b for b in B if b['id']=='assaf')
    if 'ibraq' not in [b['id'] for b in B]:
        h=dict(NEW['ibraq'])
        for g in ('men','women'):
            keep=[]
            for f in a[g]:
                if f['n'].startswith('Ibraq '): f=dict(f);f['n']=f['n'][6:];h[g]=h[g]+[f]
                else: keep.append(f)
            a[g]=keep
        a['name']='Assaf / Laverne'
        a['note']="<b>Grouped like the store:</b> Assaf and Laverne share a row. Ezz Al Oud isn't on Parfumo, so it isn't covered. Ibraq now has its own row."
        a['src']=[s for s in a['src'] if 'Ibraq' not in s[0] and 'French Tobacco' not in s[0]]
        B.insert([b['id'] for b in B].index('assaf'),h)
    if 'zimaya' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('afnan')+1,NEW['zimaya'])
    if 'dkhan' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('almajed')+1,NEW['dkhan'])
    return B
