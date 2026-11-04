# Monthly refresh

How to refresh the ratings on https://faraz-yarkhan.github.io/Fragrances/ . A scheduled Claude task follows these steps on the 1st of each month; a person can follow them too.

## Data files (in `build/`)
- `d10/raw/b1.txt` to `b6.txt` hold the designer and niche houses. Each house starts with a `## <id>` line, followed by one line per scent: `Name | year | rating | count | path`. Here `path` is the Parfumo image path, e.g. `a2/a28d94-sauvage-eau-de-toilette-dior`.
- `d10/genders.py` holds the designer gender labels: a default per brand plus F/U/M/Q overrides. A new scent takes the brand default unless you add it to a list.
- `ar5/cand10.tsv` holds the Arabian houses, tab-separated: `house  name  rating  count  gender(m/f/u/?)  path  year`.
- `ar5/newB10.json` and `rank/houses_extra.py` hold the Arabian house names, notes and sources. New houses are added in `houses_extra.py`.

## Steps
1. For each house, open its Parfumo brand list sorted by popularity, e.g. `https://www.parfumo.com/Perfumes/<brand>`. If WebFetch refuses a URL, run a WebSearch so the exact URL appears in the results, then fetch it. Read every scent from the list with its rating, its rating count and its thumbnail URL (`media.parfumo.com/perfumes/<path>_1200.jpg`). Fetch page 2 (`?current_page=2`) where the house had more than 20 scents.
2. Update matching lines, matched by `path`, with the new rating and count. Add new scents with 10 or more ratings. Never delete a line just because one fetch didn't show it.
3. For gender labels on new scents, use Fragrantica: its search-result titles say "for women", "for men" or "for women and men". **Don't trust Parfumo's individual scent pages.** They are often corrupted, with fake notes, wrong years and wrong genders. Use `?` when a label is unconfirmed.
4. Run `python3 build/run.py "<Month YYYY>"`. This ranks the scents, downloads missing photos, writes `build/CHANGES.md`, rebuilds the pages and `index.html`, and checks the scripts' syntax.
5. Run `python3 build/smoke.py`. Every line must say OK.
6. Look over `build/CHANGES.md`. A rating jump of more than 0.5 on a scent with hundreds of ratings is almost certainly a misread, so re-check it.
7. Commit and push to `main`. GitHub Pages republishes within about a minute.
8. Optionally, republish the private Claude artifacts: `build/fragrance-shortlist.html` to https://claude.ai/artifact/XqKN8b4nbday2quHyj8wmi and `build/arabian-houses.html` to https://claude.ai/artifact/1fF2ky1j8tFFDcFwx1nSC3.

## Scoring
Score = (count × rating + 100 × 7.8) / (count + 100). Men's tabs show men's, unisex and unconfirmed scents; women's tabs show women's and unisex.
