# Scent tags (type, season, time of day)

Each scent on the pages shows three tags under its name: its **type** (main accords, e.g. "Citrus · Aromatic · Woody"), its **best seasons** and its **best time of day**. They come from `build/tags.tsv`. A scheduled Claude task fills this file in batches; a person can add rows too.

## The data
`build/tags.tsv`, tab-separated, one row per scent:

`house  name  accords  winter  spring  summer  autumn  day  night  source`

- `house` and `name` must match `build/tags_queue.tsv` exactly (copy them).
- `accords`: the top 2–3 main accords in order, comma-separated, e.g. `Citrus, Aromatic, Woody`. Use Fragrantica's main accords where you can find them (Fragrantica itself, or a site that mirrors its data such as fraganty.ai, matelier.homura.it.com or fragindex); Parfumo's "The scent is X-Y" line is a fallback.
- The six numbers are Fragrantica community votes as percentages (0–100). Season numbers are relative to the top season (the top one is usually 100). Leave them blank when you can't find votes; never make them up. Blank seasons or blank day/night are estimated on the page from the accords and marked "(est.)".
- `source`: where the data came from, briefly.

On the page, seasons scoring at least 70% of the top season are shown ("All year" if all four). Time of day is "Day" or "Evening" when one beats the other by 15 points or more, otherwise "Day or evening".

## A batch
1. `python3 build/tags_next.py 40` lists the next 40 untagged scents (top 5 per house first, then the rest by popularity) and any problems with existing rows.
2. For each scent, run a WebSearch such as `fraganty.ai <name> <house> winter spring summer fall day night`. The result snippets usually carry the season and day/night percentages and the main accords. Search results are enough; only fetch a page when a snippet is cut off. Make sure the result is the same scent and concentration (EDT vs EDP vs Parfum, and flankers like "Intense" or "Elixir" are different scents).
3. Append one row per scent to `build/tags.tsv`. If nothing reliable turns up, still add the row with accords if you know them from a source, and blank numbers; if not even accords can be found, add the row with accords `?` so the queue moves on (rows with `?` show no tags).
4. Run `python3 build/tags_next.py 0` (must show no PROBLEM lines), then `python3 build/run.py "$(cat build/UPDATED)"` (keeps the ratings month unchanged), then `python3 build/smoke.py` (every line OK).
5. `git pull --rebase`, commit and push to `main`.
