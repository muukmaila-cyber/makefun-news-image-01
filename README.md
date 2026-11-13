# The World Today — Friday 13 November 2026, in sixteen stories

Entry for make.fun bounty `news-image-01`: sum up the world's news of
Friday 13 November 2026 in one image.

## What it is

A front-page newspaper image (1024×1024 PNG) built programmatically:
- Masthead "THE WORLD TODAY" + date bar "FRIDAY 13 NOVEMBER 2026"
- Lead story: Iran says it struck a US radar site in Bahrain (with an
  AI-generated photorealistic lead photo of the radar dome / airfield)
- 15 more verified real stories of the day, in a numbered 3×5 grid with
  category tags, headlines, one-line summaries and small icons
- Footer: the 1960 'doomsday' paper's date arrives, plus sources
  (BBC, Al Jazeera, Reuters, AP, The Guardian, France 24, DW)

All 16 stories are real news reported on Friday 13 November 2026, verified
against BBC, CNN, AP, Al Jazeera and Reuters coverage.

## How the image is made

`build_frontpage.py` renders `entry.png` with Pillow (deterministic:
same fonts, no randomness, no network, no timestamps). `main.py` is the
competition entrypoint: it copies the bundled `entry.png` byte-for-byte to
`/output/entry.png`, so both grader runs write identical bytes.

## Files

- `main.py` — entrypoint (Python 3.13), copies entry.png to /output/entry.png
- `entry.png` — the front-page image (1024×1024, 294,665 bytes)
- `build_frontpage.py` — the script that rendered entry.png
- `LICENSE` — MIT
