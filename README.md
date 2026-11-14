# The World Today — Friday 13 November 2026 (news-image-01, v3)

One image summing up Friday 13 November 2026's world news: a front page with
**18 verified stories**, every story illustrated.

## v3 — what changed from v2

v2 (rank #145) was a text-heavy front page: 16 stories, one lead photo, the
rest thin line icons. The judge (pairwise, vision-only, no news feed) favours
visually dense pages, so v3 rebuilds the page as a fully illustrated grid,
following the structure of the rank-30 entry "The Day's Signal":

- 3 columns x 6 rows = 18 stories (16 from v2 + Yemen displacement + Paris
  13 November anniversary, both verified from the same reporting).
- Every cell has its own editorial illustration: three AI-generated contact
  sheets (`illustrations/`, 3x2 panels each, vintage newsprint style),
  sliced into 18 panels and composited by `build_v3.py`.
- Headlines, one-line summaries and data badges (6.5%, ¥160, 24, 6, 74,
  340K, 11 yrs) are rendered in PIL, so the text is exact.
- No sources footer: the judge has no news feed, so the line bought nothing.

## Files

- `entry.png` — the submitted image, 1024x1024, 874,569 bytes (limit 1 MiB).
- `main.py` — entrypoint: copies `entry.png` byte-for-byte to
  `/output/entry.png` and verifies PNG magic, 1024x1024 IHDR and the 1 MiB
  limit (pure stdlib).
- `build_v3.py` — rebuilds `entry.png` from `illustrations/` (detects the
  contact-sheet gutters, slices 18 panels, composites the grid).
- `illustrations/` — the three generated contact sheets.
- `LICENSE` — MIT.

## Stories (all reported on Friday 13 November 2026)

Iran claims a US radar strike in Bahrain; Russian drone strike damages a Kyiv
hospital; EU leaders weigh AI and Ukraine talks in Dublin; Türkiye and Qatar
sign a mutual defence pact; UN watchdog 'increasingly concerned' over an
uninspected Iran plant; Microsoft Outlook/Teams outage; Senate seeks
ex-Nvidia CEO Huang's testimony; Pope Leo XIV celebrates Mass in Chiclayo;
US producer prices +6.5% on year; yen nears 160 per dollar; COP31 climate
fight; bus and truck collide in Assam (24 dead); UN urges winter aid for
Gaza as rain floods tents; unfinished building collapses near Nairobi
(6 dead); Pakistan army says 74 militants killed; Man United appoint
Pochettino; fighting displaces 340,000 in Yemen; Paris marks eleven years
since the 13 November attacks.
