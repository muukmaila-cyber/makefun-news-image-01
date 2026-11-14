#!/usr/bin/env python3
"""Build news-image-01 v3: 18-story fully illustrated front page (1024x1024).
Slices 3 contact sheets (1920x1280, 3x2 panels) into 18 panels, then
composites a rank-30-style grid: masthead + 3x6 cells, each cell = tag +
headline + summary + full illustration strip (band crop) + data badge.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
ILL = os.path.join(BASE, "illustrations")
PANELS = os.path.join(BASE, "panels")
os.makedirs(PANELS, exist_ok=True)

SHEETS = [
    "media-generation-sheet1-0-e0f28008-c00a-46c3-babe-0997ed98450e.png",
    "media-generation-sheet2-0-c6e99cce-7b41-4f34-9b8d-5e2166aa0bea.png",
    "media-generation-sheet3-0-f5baf718-041a-4002-87a2-4c31747a5be2.png",
]

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_OB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"

CREAM = (247, 243, 232)
INK = (26, 26, 26)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GRAY = (90, 86, 78)
RULE = (60, 55, 45)


def find_gutters(im):
    """Find white gutter bands: columns/rows bright for ~the full span."""
    import numpy as np
    a = np.asarray(im.convert("L"), dtype=float)
    H, W = a.shape
    col_frac = (a > 225).mean(axis=0)   # per column, fraction of bright rows
    row_frac = (a > 225).mean(axis=1)   # per row, fraction of bright cols

    def centers(frac, lo, hi, thresh=0.90):
        vals = [i for i, v in enumerate(frac) if v > thresh]
        out, start = [], None
        for i, v in enumerate(vals):
            if start is None:
                start = v
            if i + 1 >= len(vals) or vals[i + 1] != v + 1:
                c = (start + v) // 2
                if lo < c < hi:
                    out.append(c)
                start = None
        # merge centers closer than 60px (one gutter can split into two runs)
        merged = []
        for c in out:
            if merged and c - merged[-1] < 60:
                merged[-1] = (merged[-1] + c) // 2
            else:
                merged.append(c)
        return merged

    xc = centers(col_frac, 50, W - 50)
    yc = centers(row_frac, 50, H - 50)
    return xc, yc


def slice_sheet(path, start_idx):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    xc, yc = find_gutters(im)
    # expect 2 vertical splits (3 cols) and 1 horizontal split (2 rows)
    assert len(xc) == 2 and len(yc) == 1, f"{path}: gutters xc={xc} yc={yc}"
    xs = [0] + xc + [W]
    ys = [0] + yc + [H]
    n = start_idx
    for r in range(2):
        for c in range(3):
            # trim 6px inside each panel to drop the beige frame edge
            box = (xs[c] + 6, ys[r] + 6, xs[c + 1] - 6, ys[r + 1] - 6)
            panel = im.crop(box)
            panel.save(os.path.join(PANELS, f"p{n:02d}.png"))
            n += 1
    return n


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    # (tag, headline, summary, badge or None)
    ("BAHRAIN", "Iran claims radar strike", "US says 2 drones downed; Brent +3.3%", None),
    ("KYIV \u00b7 UKRAINE", "Russian drone strike damages hospital", "Firefighters battle blaze; 2 killed in Odesa", None),
    ("DUBLIN", "EU leaders weigh AI and Ukraine talks", "Europe seeks seat at the peace table", None),
    ("T\u00dcRKIYE + QATAR", "Mutual defence pact signed", "Ankara and Doha deepen ties", None),
    ("NUCLEAR", "UN watchdog \u2018increasingly concerned\u2019", "Uninspected Iran plant off-limits", None),
    ("MICROSOFT 365", "Outlook and Teams hit", "Outage enters a second day", None),
    ("NVIDIA FALLOUT", "Senate seeks Huang testimony", "CEO resigned after affair reports", None),
    ("CHICLAYO \u00b7 PERU", "Pope Leo celebrates Mass", "Returns to his former diocese", None),
    ("US ECONOMY", "Producer prices +6.5% on year", "Fastest annual rise since 2022", "6.5%"),
    ("YEN", "Yen nears 160 per dollar", "Fed hike bets rattle markets", "\u00a5160"),
    ("COP31", "EU vows to fight for climate science", "Row over UN report timing", None),
    ("ASSAM \u00b7 INDIA", "Bus and truck collide", "At least 24 dead on highway", "24"),
    ("GAZA", "UN urges winter aid as rain floods tents", "Families wade through tent camps", None),
    ("NAIROBI \u00b7 KENYA", "Unfinished building collapses", "6 dead, rescuers search rubble", "6"),
    ("PAKISTAN", "Army says 74 militants killed", "Raids near the Afghan border", "74"),
    ("MANCHESTER", "Man United appoint Pochettino", "A new era begins at Old Trafford", None),
    ("YEMEN", "Fighting displaces 340,000", "Families flee to desert camps", "340K"),
    ("PARIS", "Eleven years since 13 November", "City remembers the attacks", "11 yrs"),
]


def build():
    idx = 1
    for s in SHEETS:
        idx = slice_sheet(os.path.join(ILL, s), idx)
    print(f"sliced {idx-1} panels")

    W = H = 1024
    page = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(page)
    f_top = ImageFont.truetype(SANS_B, 15)
    f_mast = ImageFont.truetype(SERIF_B, 62)
    f_date = ImageFont.truetype(SANS_B, 17)
    f_tag = ImageFont.truetype(SANS_B, 12)
    f_head = ImageFont.truetype(SANS_B, 16)
    f_sum = ImageFont.truetype(SANS, 11)
    f_foot = ImageFont.truetype(SANS_B, 11)
    f_badge = ImageFont.truetype(SANS_B, 17)

    # top strip
    d.text((16, 10), "THE WORLD'S NEWS IN ONE PICTURE", font=f_top, fill=RED)
    r = d.textlength("18 STORIES \u00b7 FIVE CONTINENTS", font=f_top)
    d.text((W - 16 - r, 10), "18 STORIES \u00b7 FIVE CONTINENTS", font=f_top, fill=GRAY)
    d.line([(16, 32), (W - 16, 32)], fill=INK, width=2)
    # masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 36), title, font=f_mast, fill=INK)
    # red date bar
    d.rectangle([16, 104, W - 16, 132], fill=RED)
    dt = "FRIDAY 13 NOVEMBER 2026"
    dw = d.textlength(dt, font=f_date)
    d.text(((W - dw) / 2, 109), dt, font=f_date, fill=(255, 255, 255))

    # grid
    mx, gutter = 16, 8
    gx0, gy0 = mx, 142
    gw = W - 2 * mx
    cell_w = (gw - 2 * gutter) // 3
    grid_h = 1024 - gy0 - 26  # footer space
    cell_h = (grid_h - 5 * gutter) // 6
    text_h = 64
    ill_h = cell_h - text_h - 2
    # per-panel vertical focus (band center as fraction of panel height)
    FOCUS = [0.55, 0.50, 0.50, 0.30, 0.50, 0.50,
             0.58, 0.48, 0.50, 0.62, 0.50, 0.55,
             0.50, 0.50, 0.55, 0.50, 0.55, 0.55]

    for i, (tag, head, summ, badge) in enumerate(STORIES):
        r_, c_ = divmod(i, 3)
        x0 = gx0 + c_ * (cell_w + gutter)
        y0 = gy0 + r_ * (cell_h + gutter)
        panel = Image.open(os.path.join(PANELS, f"p{i+1:02d}.png"))
        pw, ph = panel.size
        # band crop: horizontal slice around the panel's focus height
        band_h = int(pw * ill_h / cell_w)
        y_c = int(ph * FOCUS[i] - band_h / 2)
        y_c = max(0, min(ph - band_h, y_c))
        strip = panel.crop((0, y_c, pw, y_c + band_h)).resize((cell_w, ill_h), Image.LANCZOS)
        # text block
        d.text((x0, y0), tag, font=f_tag, fill=RED)
        lines = wrap(d, head, f_head, cell_w)[:2]
        ly = y0 + 15
        for ln in lines:
            d.text((x0, ly), ln, font=f_head, fill=INK)
            ly += 18
        d.text((x0, ly), summ, font=f_sum, fill=GRAY)
        # illustration strip
        page.paste(strip, (x0, y0 + text_h + 2))
        # data badge on the strip corner
        if badge:
            bw = d.textlength(badge, font=f_badge) + 14
            bx0, by0 = x0 + cell_w - bw - 4, y0 + text_h + 6
            d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + 24], radius=4,
                                fill=RED, outline=(255, 255, 255), width=1)
            d.text((bx0 + 7, by0 + 3), badge, font=f_badge, fill=(255, 255, 255))
        # thin cell rule under
        d.line([(x0, y0 + cell_h - 1), (x0 + cell_w, y0 + cell_h - 1)], fill=(210, 204, 190), width=1)

    # footer
    fy = 1024 - 20
    d.line([(16, fy - 4), (W - 16, fy - 4)], fill=INK, width=1)
    ft = "EDITORIAL ILLUSTRATION \u00b7 SELECTED REPORTS \u00b7 FRIDAY 13 NOVEMBER 2026"
    fw = d.textlength(ft, font=f_foot)
    d.text(((W - fw) / 2, fy + 2), ft, font=f_foot, fill=GRAY)

    out = os.path.join(BASE, "entry.png")
    page.save(out, optimize=True)
    print("saved", out, page.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
