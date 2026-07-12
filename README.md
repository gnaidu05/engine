# engine
campus engine

## College Priority Dashboard

`index.html` is a self-contained dashboard for the early-careers hiring team.
The score definitions and weightages were taken from the team's reference
worksheet (`In_Demand.xlsx`); the dashboard implements that framework as its
own product logic — all data and logic are embedded in the file, no backend
or external calls, and the worksheet is not referenced anywhere in the UI.

Two accidental artifacts of the original worksheet were deliberately
corrected in this implementation: the Brand Perception Index is the proper
weighted composite of its six sub-factors for every college (the sheet's
ranking column accidentally pulled the Talent Quality sub-score, skipped the
first college entirely, and used median instead of average salary for one
row). Everything else — indices, adjusted weights, bonuses, CG priority,
location resolution, ranking — follows the framework exactly.

The page is organised as a three-step workflow:
**1 · Add College** (data entry with live auto-computed preview and the list of
added colleges), **2 · Dashboard** (the report canvas plus every lever —
bonus toggles, zone chips, salary range, CG filter, search, tier cutoffs and
the economical threshold), **3 · Catalogue** (the business-ready output that
reflects everything chosen on the Dashboard tab).

- **Report canvas:** Power BI-style layout — slicer bar, KPI cards, cross-filtering
  visuals (avg score by zone, CG priority donut, top 10 bars) and the ranking
  table as a detail visual. Clicking a bar or donut segment filters the page;
  clicking it again clears.
- **Toggles:** Engagement bonus (default on) and Diversity bonus (default off),
  matching the workbook's Dashboard-sheet toggles.
- **Filters:** multi-select Zone chips (pick any combination of zones), a
  median-salary range in ₹ lakhs, CG Priority, and free-text search — all
  applied across the dashboard and the catalogue.
- **Table:** Dashboard-sheet ordering (CG priority group, then Total Priority
  Score), sortable columns, plus the workbook's pure RANK.EQ priority rank.
- **Breakdown:** click any row for the full per-college computation
  (salary/NIRF/NAAC/NBA indices, brand perception sub-scores, weights, bonuses).
- **Catalogue view:** a second tab that turns the ranking into a business-ready
  catalogue — priority tiers (defaults: Invest 70+, Engage 55–70, Selective
  40–55, Monitor <40, with the cutoffs editable live in the toolbar so the
  business can set them in the room; the matrices' high/low split follows the
  Tier 2 cutoff and the value matrix's "economical" median-salary threshold is
  likewise editable) grouped by zone, an opportunity matrix (score × engagement), a
  value matrix (score × median salary), and tag-rich college cards. Follows
  the same slicers and bonus toggles, can hide test colleges, and has a
  Print / Save-PDF layout for handing to the business.
- **Add college:** enter just the raw data (name, location, NIRF ranks, NAAC,
  NBA, salaries, engagement, diversity, CG priority) and the city/state/zone,
  every index, brand perception, scores and ranks auto-populate live using the
  workbook's own logic — exactly as if a row were appended to the College list
  sheet (including the salary/NBA maxima rescaling). Added colleges can be
  edited or removed. By default they persist per-browser via localStorage;
  see below to share them across the whole team.
- **NIRF auto-fill:** typing a college name in the form surfaces matching
  institutes from an embedded directory of the official nirfindia.org
  engineering rankings (ranks 1-100 plus the 101-150/151-200/201-300 bands,
  for 2023-2025) as clickable chips; picking one fills the three NIRF rank
  fields. The directory is bundled into the page (no runtime external calls)
  and is refreshed from the official site by the "Update NIRF directory"
  workflow (Actions tab), which runs scripts/build_nirf_directory.py and
  commits the result — run it whenever NIRF publishes a new year.
- **Edit existing colleges:** the Add College tab carries a searchable
  directory of every college — baseline and added — with View / Edit actions
  (plus Remove for added and "Reset to original" for edited baseline
  colleges). Baseline edits are overrides keyed by the college name (the
  name itself is locked — it is the identity), badge the college as
  "edited", and re-score it live including the salary/NBA maxima rescaling.

## Team-shared additions (Supabase)

Out of the box, all changes made through the UI (added colleges and edits to
baseline colleges) stay in each person's browser. To make everything shared
and live for the whole team:

1. Create (or reuse) a [Supabase](https://supabase.com) project.
2. In the project's SQL editor, run `supabase/shared_colleges.sql` from this
   repo — it creates the `shared_colleges` table with row-level security.
3. In `index.html`, find the `SHARED` config near the top of the last script
   block and fill in your project URL and public anon key:

   ```js
   const SHARED = {
     url: "https://YOURPROJECT.supabase.co",
     anonKey: "YOUR_PUBLIC_ANON_KEY",
     table: "shared_colleges",
   };
   ```

4. Commit and push to `main` — the site republishes automatically.

With SHARED configured, the Add College tab shows "↻ shared with team" (click
it to refresh) and everything syncs through one table: added colleges are
rows with kind='added', baseline-college edits are rows with kind='edited'
(matched by name), and removals/resets delete the row. The anon key is public by design and safe to embed; access
is governed by the RLS policies in the SQL file (anyone with the page URL can
read/write — right for an internal tool; switch the policies to
`authenticated` if you later add Supabase Auth). If the database is
unreachable the page still renders the baseline 67 colleges and offers a
retry.

Deploy by serving the file anywhere (e.g. GitHub Pages) or opening it directly
in a browser.
