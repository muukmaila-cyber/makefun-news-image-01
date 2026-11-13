#!/usr/bin/env python3
"""Build the news-image-01 front page (1024x1024 PNG, deterministic).

Design: front-page newspaper, rank-2 approach (clean programmatic layout,
16 verified real stories of Friday 13 November 2026, one AI-generated lead
photo, PIL-drawn icons, no other photos). Output: entry.png (<=1 MiB).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (250, 246, 237)      # cream paper
INK = (17, 17, 17)        # near-black
RED = (185, 28, 28)       # masthead red
GRAY = (90, 90, 90)
LIGHT_LINE = (200, 192, 178)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    """Greedy word wrap returning list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_icon(draw, cx, cy, kind, color):
    """Minimal line icon centred at (cx, cy), ~26px box."""
    s = 13
    c = color
    if kind == "MIDDLE EAST":  # dome
        draw.arc([cx - s, cy - s + 4, cx + s, cy + s + 4], 180, 360, fill=c, width=2)
        draw.line([cx - s, cy + 6, cx + s, cy + 6], fill=c, width=2)
        draw.line([cx, cy - s - 2, cx, cy - s + 4], fill=c, width=2)
    elif kind == "EUROPE":  # circle of stars -> ring + dots
        draw.ellipse([cx - s, cy - s, cx + s, cy + s], outline=c, width=2)
        for a in range(0, 360, 45):
            import math
            x = cx + int(9 * math.cos(math.radians(a)))
            y = cy + int(9 * math.sin(math.radians(a)))
            draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=c)
    elif kind == "NUCLEAR":  # atom
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=c)
        draw.ellipse([cx - s, cy - 6, cx + s, cy + 6], outline=c, width=2)
        draw.ellipse([cx - 6, cy - s, cx + 6, cy + s], outline=c, width=2)
    elif kind == "WORLDWIDE":  # globe
        draw.ellipse([cx - s, cy - s, cx + s, cy + s], outline=c, width=2)
        draw.line([cx - s, cy, cx + s, cy], fill=c, width=2)
        draw.line([cx, cy - s, cx, cy + s], fill=c, width=2)
    elif kind == "UNITED STATES":  # star
        import math
        pts = []
        for i in range(10):
            r = s if i % 2 == 0 else s * 0.45
            a = math.radians(-90 + i * 36)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        draw.polygon(pts, outline=c, width=2)
    elif kind == "AMERICAS":  # cross (church)
        draw.line([cx, cy - s, cx, cy + s], fill=c, width=3)
        draw.line([cx - 8, cy - 5, cx + 8, cy - 5], fill=c, width=3)
    elif kind == "MARKETS":  # rising chart
        draw.line([cx - s, cy + 8, cx - 4, cy + 1, cx + 4, cy - 4, cx + s, cy - s], fill=c, width=2)
        draw.line([cx + s - 6, cy - s, cx + s, cy - s], fill=c, width=2)
        draw.line([cx + s, cy - s, cx + s, cy - s + 6], fill=c, width=2)
    elif kind == "CLIMATE":  # leaf
        draw.ellipse([cx - s, cy - 6, cx + s, cy + 8], outline=c, width=2)
        draw.line([cx - s, cy + 6, cx + s, cy - 6], fill=c, width=2)
    elif kind == "ASIA":  # bus
        draw.rectangle([cx - s, cy - 8, cx + s, cy + 6], outline=c, width=2)
        draw.ellipse([cx - 8, cy + 6, cx - 3, cy + 11], fill=c)
        draw.ellipse([cx + 3, cy + 6, cx + 8, cy + 11], fill=c)
    elif kind == "AFRICA":  # mountain
        draw.polygon([(cx - s, cy + s), (cx, cy - s), (cx + s, cy + s)], outline=c, width=2)
    elif kind == "SOUTH ASIA":  # two peaks
        draw.polygon([(cx - s, cy + s), (cx - 3, cy - 4), (cx + 4, cy + s)], outline=c, width=2)
        draw.polygon([(cx - 2, cy + s), (cx + 6, cy - s), (cx + s, cy + s)], outline=c, width=2)
    elif kind == "SPORT":  # ball
        draw.ellipse([cx - s, cy - s, cx + s, cy + s], outline=c, width=2)
        draw.polygon([(cx, cy - 5), (cx + 5, cy), (cx, cy + 5), (cx - 5, cy)], outline=c, width=2)
    else:
        draw.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=c, width=2)

STORIES = [
    # (number, category, headline, summary)
    (2, "EUROPE", "Russian drones hit a Kyiv hospital; 2 killed in Odesa",
     "Firefighters battled the blaze as ambulances ferried the wounded"),
    (3, "EUROPE", "Europe seeks a seat at Ukraine peace talks",
     "The EU plus the UK, France, Germany, Italy and Poland agreed a team in Dublin"),
    (4, "MIDDLE EAST", "Türkiye and Qatar sign a mutual defence pact",
     "Signed in Istanbul"),
    (5, "NUCLEAR", "UN watchdog 'increasingly concerned' over uninspected Iran plant",
     "The Isfahan enrichment plant remains off-limits to inspectors"),
    (6, "WORLDWIDE", "Microsoft outage knocks out Outlook and Teams",
     "Down about 10 hours; hospitals and schools hit; Microsoft apologises"),
    (7, "UNITED STATES", "Senate summons ex-Nvidia CEO Huang and Lutnick",
     "Huang resigned as CEO this week; Nvidia shares fell 16%"),
    (8, "AMERICAS", "Pope Leo XIV holds homecoming Mass in Chiclayo, Peru",
     "He returns to the Peruvian diocese he once served as bishop"),
    (9, "UNITED STATES", "US wholesale prices jump 6.5% on the year",
     "The fastest annual rise in producer prices since 2022"),
    (10, "MARKETS", "Yen nears 160 per dollar as Fed hike bets rattle markets",
     "Currency markets rattled by bets on a Fed rate hike"),
    (11, "CLIMATE", "COP31: EU vows to fight for climate science",
     "Row over the timing of UN climate science reports"),
    (12, "ASIA", "Bus and truck collide in India's Assam — at least 24 dead",
     "The crash happened on a rural highway in the north-east"),
    (13, "MIDDLE EAST", "Gaza: UN urges winter aid as rain floods tents",
     "Displaced families wade through flooded tent camps"),
    (14, "AFRICA", "Kenya: unfinished building collapse near Nairobi, 6 dead",
     "Rescue workers search the rubble for survivors"),
    (15, "SOUTH ASIA", "Pakistan army says 74 militants killed in raids",
     "Raids near the Afghan border"),
    (16, "SPORT", "Man United appoint Pochettino as manager",
     "A new era begins at Old Trafford"),
]

LEAD_HEAD = "Iran says it struck a US radar site in Bahrain"
LEAD_SUM = ("Iran calls it retaliation for a US strike near Hormuz; the US says it "
            "downed 2 drones. A tanker hit a mine in the strait — Brent crude rose "
            "3.3% to $95.82.")

def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M = 24                      # margin
    CW = W - 2 * M              # content width = 976

    # ---- top bar ----
    f_top = font(SANS_B, 15)
    d.text((M, 14), "THE WORLD'S NEWS IN ONE PICTURE", font=f_top, fill=RED)
    right = "16 STORIES · FIVE CONTINENTS"
    d.text((W - M - d.textlength(right, font=f_top), 14), right, font=f_top, fill=GRAY)
    d.line([(M, 38), (W - M, 38)], fill=INK, width=2)

    # ---- masthead ----
    f_mast = font(SERIF_B, 74)
    mast = "THE WORLD TODAY"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 44), mast, font=f_mast, fill=INK)

    # ---- date bar ----
    d.rectangle([M, 124, W - M, 156], fill=RED)
    f_date = font(SANS_B, 23)
    date = "FRIDAY 13 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 130), date, font=f_date, fill=(255, 255, 255))

    # ---- lead story ----
    lead_y = 168
    lead_h = 216
    # label
    f_lab = font(SANS_B, 13)
    lab = "  LEAD STORY  "
    lw = d.textlength(lab, font=f_lab)
    d.rectangle([M, lead_y, M + lw, lead_y + 20], fill=INK)
    d.text((M, lead_y + 2), lab, font=f_lab, fill=(255, 255, 255))
    # headline (left, ~540 wide)
    f_lead = font(SANS_B, 38)
    lx, lw_head = M, 540
    lines = wrap(d, LEAD_HEAD, f_lead, lw_head)
    y = lead_y + 28
    for ln in lines:
        d.text((lx, y), ln, font=f_lead, fill=INK)
        y += 44
    # summary
    f_sum = font(SANS_R, 17)
    y += 4
    for ln in wrap(d, LEAD_SUM, f_sum, lw_head):
        d.text((lx, y), ln, font=f_sum, fill=(40, 40, 40))
        y += 22
    # lead photo (right)
    photo = Image.open("lead-radar-bahrain.png").convert("RGB")
    px, py, pw, ph = M + 556, lead_y, 420, 216
    # centre-crop to aspect
    tw, th = photo.size
    target = pw / ph
    if tw / th > target:
        nw = int(th * target)
        x0 = (tw - nw) // 2
        photo = photo.crop((x0, 0, x0 + nw, th))
    else:
        nh = int(tw / target)
        y0 = (th - nh) // 2
        photo = photo.crop((0, y0, tw, y0 + nh))
    photo = photo.resize((pw, ph), Image.LANCZOS)
    img.paste(photo, (px, py))
    d.rectangle([px, py, px + pw - 1, py + ph - 1], outline=INK, width=2)

    # ---- divider ----
    gy = lead_y + lead_h + 12
    d.line([(M, gy), (W - M, gy)], fill=INK, width=2)
    gy += 10

    # ---- grid: 3 cols x 5 rows ----
    cols, rows = 3, 5
    gap_x, gap_y = 16, 10
    cell_w = (CW - gap_x * (cols - 1)) // cols
    grid_bottom = 962
    cell_h = (grid_bottom - gy - gap_y * (rows - 1)) // rows
    f_num = font(SANS_B, 13)
    f_cat = font(SANS_B, 11)
    f_head = font(SANS_B, 15)
    f_body = font(SANS_R, 11)
    for i, (num, cat, head, summ) in enumerate(STORIES):
        r, c = divmod(i, cols)
        x0 = M + c * (cell_w + gap_x)
        y0 = gy + r * (cell_h + gap_y)
        # number badge
        d.ellipse([x0, y0, x0 + 22, y0 + 22], fill=RED)
        nt = str(num)
        d.text((x0 + 11 - d.textlength(nt, font=f_num) / 2, y0 + 3), nt, font=f_num, fill=(255, 255, 255))
        # category + icon
        d.text((x0 + 28, y0 + 4), cat, font=f_cat, fill=RED)
        draw_icon(d, x0 + cell_w - 14, y0 + 11, cat, (60, 60, 60))
        # headline
        hy = y0 + 26
        hl = wrap(d, head, f_head, cell_w)
        for ln in hl[:3]:
            d.text((x0, hy), ln, font=f_head, fill=INK)
            hy += 18
        # summary
        for ln in wrap(d, summ, f_body, cell_w)[:2]:
            d.text((x0, hy), ln, font=f_body, fill=(70, 70, 70))
            hy += 14

    # ---- footer ----
    fy = 970
    f_fin = font(SANS_B, 15)
    fin = "AND FINALLY: THE 1960 'DOOMSDAY' PAPER'S DATE ARRIVES — AND THE WORLD CARRIES ON"
    d.text(((W - d.textlength(fin, font=f_fin)) / 2, fy), fin, font=f_fin, fill=INK)
    f_src = font(SANS_R, 11)
    src = "Every story reported on Friday 13 November 2026 · Sources: BBC, Al Jazeera, Reuters, AP, The Guardian, France 24, DW"
    d.text(((W - d.textlength(src, font=f_src)) / 2, fy + 22), src, font=f_src, fill=GRAY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")

if __name__ == "__main__":
    main()
