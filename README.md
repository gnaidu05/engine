# engine
campus engine

## College Priority Dashboard

`index.html` is a self-contained dashboard for the early-careers hiring team.
It reproduces the scoring model from `In_Demand.xlsx` exactly — all data and
formula logic are embedded in the file; no backend or external calls.

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
- **Add college:** enter just the raw data (name, location, NIRF ranks, NAAC,
  NBA, salaries, engagement, diversity, CG priority) and the city/state/zone,
  every index, brand perception, scores and ranks auto-populate live using the
  workbook's own logic — exactly as if a row were appended to the College list
  sheet (including the salary/NBA maxima rescaling). Added colleges can be
  edited or removed and persist in the browser via localStorage.

Deploy by serving the file anywhere (e.g. GitHub Pages) or opening it directly
in a browser.
