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

- **Report canvas:** Power BI-style layout — slicer bar, KPI cards, cross-filtering
  visuals (avg score by zone, CG priority donut, top 10 bars) and the ranking
  table as a detail visual. Clicking a bar or donut segment filters the page;
  clicking it again clears.
- **Toggles:** Engagement bonus (default on) and Diversity bonus (default off),
  matching the workbook's Dashboard-sheet toggles.
- **Filters:** Zone, CG Priority, and free-text search.
- **Table:** Dashboard-sheet ordering (CG priority group, then Total Priority
  Score), sortable columns, plus the workbook's pure RANK.EQ priority rank.
- **Breakdown:** click any row for the full per-college computation
  (salary/NIRF/NAAC/NBA indices, brand perception sub-scores, weights, bonuses).
- **Catalogue view:** a second tab that turns the ranking into a business-ready
  catalogue — priority tiers (defaults: Invest 70+, Engage 55–70, Selective
  40–55, Monitor <40, with the cutoffs editable live in the toolbar so the
  business can set them in the room; the matrices' high/low split follows the
  Tier 2 cutoff) grouped by zone, an opportunity matrix (score × engagement), a
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

## Team-shared additions (Supabase)

Out of the box, colleges added through the UI stay in each person's browser.
To make additions shared and live for the whole team:

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

With SHARED configured, the slicer bar shows "↻ shared with team" (click it to
refresh), everyone sees the same added colleges, and edits/removals sync
through the table. The anon key is public by design and safe to embed; access
is governed by the RLS policies in the SQL file (anyone with the page URL can
read/write — right for an internal tool; switch the policies to
`authenticated` if you later add Supabase Auth). If the database is
unreachable the page still renders the baseline 67 colleges and offers a
retry.

Deploy by serving the file anywhere (e.g. GitHub Pages) or opening it directly
in a browser.
