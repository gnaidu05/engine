# engine
campus engine

## College Priority Dashboard

`index.html` is a self-contained dashboard for the early-careers hiring team.
It reproduces the scoring model from `In_Demand.xlsx` exactly — all data and
formula logic are embedded in the file; no backend or external calls.

- **Toggles:** Engagement bonus (default on) and Diversity bonus (default off),
  matching the workbook's Dashboard-sheet toggles.
- **Filters:** Zone, CG Priority, and free-text search.
- **Table:** Dashboard-sheet ordering (CG priority group, then Total Priority
  Score), sortable columns, plus the workbook's pure RANK.EQ priority rank.
- **Breakdown:** click any row for the full per-college computation
  (salary/NIRF/NAAC/NBA indices, brand perception sub-scores, weights, bonuses).

Deploy by serving the file anywhere (e.g. GitHub Pages) or opening it directly
in a browser.
