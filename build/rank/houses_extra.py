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
 'bujairami':dict(id='bujairami',name='Bujairami',tag='Australia (Sydney) · Inspired-by house',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/bujairami'],['Fragrantica: Bujairami','https://www.fragrantica.com/designers/Bujairami.html'],['Fragrantica: Adam Bujairami','https://www.fragrantica.com/noses/Adam_Bujairami.html']],
   note="<b>Not Middle Eastern:</b> Bujairami is a Sydney house founded by Adam Bujairami, who learned perfumery in Dubai. It makes Arabian-style 'inspired-by' scents: Hectic, for example, is a take on LV Imagination. Parfumo lists over 1,200 Bujairami scents, but most are new with only a handful of ratings, so this list is its 20 most popular. Several gender labels aren't confirmed.",men=[],women=[]),
 'velixir':dict(id='velixir',name='Velixir Parfums',tag='Indonesia · Inspired-by house',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/velixir'],['Fragrantica: Velixir','https://www.fragrantica.com/designers/Velixir.html']],
   note="<b>Not Middle Eastern:</b> Velixir is an Indonesian brand started in 2025 by two brothers. It makes 'inspired-by' scents, such as Icarus (a take on Blue Talisman) and Persephone (LV California Dreams). Everything is very new, and only 12 of its 24 scents have 10 or more ratings, so treat the scores with caution. A few reviewers question whether its online buzz is genuine; I couldn't confirm that either way.",men=[],women=[]),
 'jomilano':dict(id='jomilano',name='Jo Milano Paris (Game of Spades)',tag='USA / France · Inspired-by house',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/Jo_Milano'],['Fragrantica: Jo Milano Paris','https://www.fragrantica.com/designers/Jo-Milano-Paris.html'],['US trademarks: Jo Milano Paris Inc','https://trademark.justia.com/owners/jo-milano-paris-inc-2833079']],
   note="<b>Not Middle Eastern:</b> Game of Spades is a line by Jo Milano Paris. The company holding its trademarks is registered in the US, though some retailers say the scents are made in France. Most are 'inspired-by' scents: reviewers compare Fullhouse to LV Imagination, and No Limit and Boston to other niche hits. Parfumo lists 84 Jo Milano scents, but only 14 have 10 or more ratings. The unisex labels come from Fragrantica.",men=[],women=[]),
 'atralia':dict(id='atralia',name='Atralia',tag='UAE · Newer house',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/atralia'],['Fragrantica: Atralia','https://www.fragrantica.com/designers/Atralia.html'],['Fraganzi: Atralia (gender labels)','https://fraganzi.com/en/collections/arabian-perfumes-atralia']],
   note="<b>Small numbers:</b> Atralia is a UAE house that Fragrantica lists as new; one retailer says it was founded in 1996, but I couldn't confirm that. Only 9 of its 31 Parfumo scents have 10 or more ratings, the most being 48. Gender labels come from retailer listings (Fraganzi, Amazon), not Fragrantica, so treat them as a guide.",men=[],women=[]),
 'maisonasrar':dict(id='maisonasrar',name='Maison Asrar',tag='UAE · Gulf Orchid',
   src=[['Parfumo brand list','https://www.parfumo.com/Perfumes/maison-asrar'],['Fragrantica: Maison Asrar','https://www.fragrantica.com/designers/MAISON-ASRAR.html'],['Sotdunes: Maison Asrar guide','https://www.sotdunes.co.uk/blogs/news/maison-asrar-uk-guide']],
   note="<b>Gulf Orchid's newer label:</b> Maison Asrar is marketed by Gulf Orchid Fragrances in the UAE. Most of its range is from 2025–26, and reviewers compare many scents to niche hits: Legacy to Blue Talisman, Vanguard to Absolu Aventus, Majesty to Tygar. Only its 20 most popular scents could be read from Parfumo. Several gender labels aren't confirmed.",men=[],women=[]),
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
    if 'bujairami' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('fa')+1,NEW['bujairami'])
    if 'velixir' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('mykonos')+1,NEW['velixir'])
    if 'jomilano' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('velixir')+1,NEW['jomilano'])
    if 'atralia' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('riiffs')+1,NEW['atralia'])
    if 'maisonasrar' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('haramain')+1,NEW['maisonasrar'])
    return B

def fix_d(B):
    if 'margiela' not in [b['id'] for b in B]:
        B.insert([b['id'] for b in B].index('lelabo')+1,json.load(open(S+'rank/margiela_house.json')))
    if 'hugoboss' not in [b['id'] for b in B]:
        B.append(json.load(open(S+'rank/hugoboss_house.json')))
    return B
