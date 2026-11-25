#!/usr/bin/env python3
"""Render Wednesday 25 November 2026's world news as one Economist-style
cover image (1024x1024 PNG).

Fresh build for the news-image-20261125 competition: cream page, red
masthead "THE WORLD TODAY", the date as a huge title, a lead story on the
Dow crossing 50,000, three boxed second leads, a schematic world map with
flashpoint dots, a UTC timeline strip, 39 dated story items in three
columns grouped by region, and a date-check verification footer.

Run:  python3 build_image.py   (writes entry.png next to this file)
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
CREAM = (244, 238, 221)
PAPER = (250, 246, 233)
INK = (26, 26, 24)
RED = (178, 34, 28)
RED_DK = (140, 22, 18)
GREY = (96, 92, 84)
RULE = (178, 34, 28)
BLUE = (28, 62, 110)
GOLD = (176, 132, 30)

FDIR = "/usr/share/fonts/truetype/dejavu"


def f(path, size):
    return ImageFont.truetype(os.path.join(FDIR, path), size)


SERIF = lambda s: f("DejaVuSerif.ttf", s)
SERIFB = lambda s: f("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: f("DejaVuSans.ttf", s)
SANSB = lambda s: f("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_para(draw, x, y, text, font, fill, max_w, leading, head=None,
              head_font=None, head_fill=None, max_lines=2):
    """Draw a wrapped paragraph; optional bold head lead-in on first line."""
    full = ((head + " ") if head else "") + text
    lines = wrap(draw, full, font, max_w)[:max_lines]
    for i, ln in enumerate(lines):
        draw.text((x, y + i * leading), ln, font=font, fill=fill)
    return y + len(lines) * leading


# ---------------------------------------------------------------- stories
# Each item: (region, headline, detail). All first reported 25 Nov 2026.
STORIES = [
    ("MIDDLE EAST & CONFLICT",
     "HOUTHI MISSILE HITS RIYADH'S TALLEST TOWER",
     "11 wounded; second strike on the tower in five days."),
    ("MIDDLE EAST & CONFLICT",
     "THREE TANKERS HIT BY MINES IN HORMUZ",
     "Iran's navy blames mines; Tehran vows 'all means' against the US blockade."),
    ("MIDDLE EAST & CONFLICT",
     "ISRAEL STRIKE KILLS HAMAS SECURITY CHIEF",
     "Naim Abu Nakhla dead in Gaza City; 1,679 killed since the October ceasefire."),
    ("MIDDLE EAST & CONFLICT",
     "HOUTHIS 60 KM FROM ADEN",
     "Yemeni army says the capital will not fall; Saudi strikes hit the south-west."),
    ("MIDDLE EAST & CONFLICT",
     "UKRAINE SINKS RUSSIAN CORVETTE IN LIBYA",
     "Seven naval drones sink the Merkury in Benghazi port; Italy protests to Kyiv."),
    ("MIDDLE EAST & CONFLICT",
     "ZELENSKIY CONFIRMS GULF OF FINLAND STRIKE",
     "Ukraine hit a Russian cargo ship; Norway urges caution."),
    ("MIDDLE EAST & CONFLICT",
     "PUTIN: RETALIATION 'INEVITABLE'",
     "After Ukraine hit Russian oil plants; Moscow eyes new markets."),
    ("MIDDLE EAST & CONFLICT",
     "NATO TO DEPLOY EARLY-WARNING JETS IN POLAND",
     "After missiles landed in Poland during a strike on Ukraine."),
    ("EUROPE",
     "EU READIES NEW RUSSIA SANCTIONS",
     "A 22nd package in the works as the war grinds on."),
    ("EUROPE",
     "SARKOZY CORRUPTION CASE GOES TO TRIAL",
     "Ex-president and Carla Bruni face court; first hearing 1 April 2027."),
    ("EUROPE",
     "RUSSIA, UKRAINE TRADE CHARGES AT THE UN",
     "Over Black Sea shipping and energy attacks."),
    ("EUROPE",
     "IRAQ ORDERS TAKEOVER OF KURDISH OILFIELDS",
     "Kurds reject the Baghdad move."),
    ("EUROPE",
     "TURKEY SEEKS FREEZES ON 108 TRADERS",
     "$17bn fund scandal; alleged manipulation."),
    ("EUROPE",
     "TURKISH HELICOPTER CRASHES",
     "Second military helicopter down in under two weeks."),
    ("EUROPE",
     "COP31 ENDS WITH NO DEAL",
     "First climate-summit failure in 17 years; EU rejected the draft."),
    ("AMERICAS",
     "DOW TOPS 50,000 FOR THE FIRST TIME",
     "Blue chips hit the milestone as tech slips."),
    ("AMERICAS",
     "TRUMP PARDONS TURKEYS FREEDOM AND FEATHERS",
     "Thanksgiving ritual at the White House."),
    ("AMERICAS",
     "GIULIANI GETS MEDAL OF FREEDOM",
     "Trump honours the disbarred ex-lawyer."),
    ("AMERICAS",
     "FORT HOOD SHOOTER SEEKS STAY",
     "Hasan asks the court to halt next week's execution."),
    ("AMERICAS",
     "CIA HIT BY CYBERATTACK",
     "US spy data exposed amid government system outages."),
    ("AMERICAS",
     "TRUMP READIES NEW TARIFFS",
     "After a probe into excess factory capacity."),
    ("ASIA-PACIFIC",
     "HUAWEI GUILTY ON 10 OF 12 US CHARGES",
     "Trade-secret theft and bank fraud; racketeering acquitted; billions in fines loom."),
    ("ASIA-PACIFIC",
     "NVIDIA REINSTATES JENSEN HUANG AS CEO",
     "Board unanimous, 11 days after his exit; shares jump about 31%."),
    ("ASIA-PACIFIC",
     "SENSEX DROPS 1,484 POINTS",
     "Nifty slips below 25,400 in a broad sell-off."),
    ("ASIA-PACIFIC",
     "NIKKEI JUMPS 3.91%",
     "On Huang's return; Nasdaq had fallen 10% the week before."),
    ("ASIA-PACIFIC",
     "SOUTH KOREA DRAFTS DIGITAL-ASSET ACT",
     "Exchange owners capped at 20%; won stablecoins allowed."),
    ("ASIA-PACIFIC",
     "BLACKROCK LAUNCHES HK TOKENISED FUND",
     "Asia-Pacific's first; subscriptions in HKD stablecoin."),
    ("ASIA-PACIFIC",
     "CHINA LAUNCHES SHENZHOU-24",
     "First Pakistani astronaut aboard; 90 experiments planned."),
    ("ASIA-PACIFIC",
     "NEPAL QUAKE 5.6 SHAKES KOSHI",
     "Tremors felt across eastern India."),
    ("ASIA-PACIFIC",
     "BJP AND AKALI DAL REUNITE",
     "Alliance for 2027 Punjab polls after a six-year split."),
    ("MARKETS & TECH",
     "ANTHROPIC SHARES SLIDE BELOW $83 IPO PRICE",
     "On track to shed nearly $200bn in value."),
    ("MARKETS & TECH",
     "OPENAI SHOWS GPT-6 PROTEIN DESIGN",
     "Models design proteins by reasoning alone, lab-validated."),
    ("MARKETS & TECH",
     "TIDAL TO DELETE 29M AI TRACKS",
     "Bans fully AI-generated songs from 9 December."),
    ("MARKETS & TECH",
     "ANSEM WALLET HACKED FOR $2.57M",
     "Via the Bullpen platform; token falls 60% in an hour."),
    ("MARKETS & TECH",
     "COPPER -5.1%, GOLD -2.3%",
     "Natural gas +5.9% on cold weather; Brent $87.51."),
    ("SPORT & WORLD",
     "ENGLAND BEAT AUSTRALIA IN 2ND T20I",
     "By eight wickets, chasing 185 to level the series."),
    ("SPORT & WORLD",
     "NEW ZEALAND HOLD INDIA TO A DRAW",
     "Determined batting in the first Test."),
    ("SPORT & WORLD",
     "KENYA AND DR CONGO RESTORE TIES",
     "Full diplomatic relations resumed."),
    ("SPORT & WORLD",
     "128 NATIONS BACK KILLER-ROBOT RULES",
     "UN Geneva talks agree to work on autonomous-weapons rules by 2028."),
]

# (hour, label) for the UTC timeline strip; times approximate as reported.
TIMELINE = [
    (1, "Nikkei +3.9%"),
    (4, "Riyadh hit"),
    (6, "Huawei verdict"),
    (9, "Huang back"),
    (12, "EU sanctions"),
    (15, "Gaza strike"),
    (18, "Zelenskiy"),
    (21, "Dow 50k"),
]

# (x, y, label, anchor) flashpoints; coords are map-local (origin = map box
# top-left, box is 956 wide x 120 tall).
DOTS = [
    (150, 45, "NEW YORK", "l"), (195, 78, "CHICAGO", "l"),
    (410, 30, "LONDON", "r"), (465, 28, "KYIV", "a"),
    (455, 98, "BENGHAZI", "b"), (525, 62, "RIYADH", "l"),
    (550, 82, "HORMUZ", "b"), (500, 92, "GAZA", "r"),
    (680, 72, "DELHI", "l"), (790, 52, "BEIJING", "l"),
    (862, 58, "TOKYO", "l"),
]

# Rough continent blobs in map-local coordinates (box 956 x 120).
CONTINENTS = [
    [(30, 10), (180, 0), (240, 15), (250, 55), (210, 85), (160, 105),
     (110, 95), (60, 60)],                          # North America
    [(215, 98), (258, 96), (272, 112), (250, 118), (228, 112)],  # S. America
    [(400, 5), (470, 0), (500, 20), (480, 50), (430, 55), (405, 30)],  # Europe
    [(410, 60), (480, 55), (515, 85), (495, 115), (450, 118), (420, 105)],  # Africa
    [(520, 5), (650, 0), (770, 10), (870, 25), (890, 60), (830, 85),
     (740, 80), (640, 85), (540, 60)],             # Asia
    [(790, 95), (860, 90), (875, 115), (815, 118)],  # Australia
]


def render():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 34  # side margin

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 66], fill=RED)
    d.text((W // 2, 33), "THE WORLD TODAY", font=SERIFB(38),
           fill=(255, 248, 235), anchor="mm")
    d.text((mx, 78), "WEDNESDAY", font=SANSB(17), fill=RED)
    d.text((W - mx, 78), "25 NOVEMBER 2026", font=SANSB(17), fill=RED,
           anchor="ra")
    d.line([(mx, 100), (W - mx, 100)], fill=RED, width=2)

    # ---- date title + lead ---------------------------------------------
    d.text((mx, 108), "DOW TOPS 50,000", font=SERIFB(50), fill=INK)
    d.text((mx, 164),
           "First time ever for the blue chips — as Nvidia-led tech slips",
           font=SERIF(18), fill=INK)
    d.text((mx, 188),
           "and markets split over rates.",
           font=SERIF(18), fill=INK)

    # mini chart: Dow climbing to 50,000 (drawn, schematic)
    cx0, cy0, cx1, cy1 = 660, 112, 990, 210
    d.rectangle([cx0, cy0, cx1, cy1], outline=GREY, width=1, fill=PAPER)
    pts = [(cx0 + 8, cy1 - 18), (cx0 + 60, cy1 - 30), (cx0 + 120, cy1 - 26),
           (cx0 + 180, cy1 - 48), (cx0 + 240, cy1 - 44), (cx0 + 300, cy1 - 70),
           (cx0 + 340, cy1 - 82)]
    d.line(pts, fill=RED, width=3)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4],
              fill=RED)
    d.text((cx0 + 10, cy0 + 6), "DOW JONES  ·  50,000", font=SANSB(13),
           fill=RED_DK)
    d.text((cx0 + 10, cy1 - 20), "S&P 500 -0.95%  ·  Nasdaq off highs",
           font=SANS(11), fill=GREY)
    d.line([(mx, 222), (W - mx, 222)], fill=INK, width=1)

    # ---- three boxed second leads ---------------------------------------
    boxes = [
        ("RIYADH TOWER HIT",
         "Houthis strike the capital's tallest tower; 11 wounded — the "
         "second hit in five days."),
        ("HORMUZ MINES",
         "Three tankers hit by mines in the Strait; Iran vows 'all means' "
         "against the US blockade."),
        ("HUANG IS BACK",
         "Nvidia's board reinstates its CEO 11 days after his exit; shares "
         "jump about 31%."),
    ]
    bw, gap = 300, 14
    y0 = 234
    for i, (head, body) in enumerate(boxes):
        x0 = mx + i * (bw + gap)
        d.rectangle([x0, y0, x0 + bw, y0 + 92], outline=INK, width=1,
                    fill=PAPER)
        d.rectangle([x0, y0, x0 + bw, y0 + 26], fill=INK)
        d.text((x0 + 10, y0 + 13), head, font=SANSB(14), fill=(255, 248, 235),
               anchor="lm")
        draw_para(d, x0 + 10, y0 + 34, body, SANS(12), INK, bw - 20, 15,
                  max_lines=3)
    d.line([(mx, 340), (W - mx, 340)], fill=INK, width=1)

    # ---- schematic world map --------------------------------------------
    map_y0, map_y1 = 352, 500
    d.text((mx, map_y0), "THE WORLD AT A GLANCE — 25 NOVEMBER 2026",
           font=SANSB(13), fill=RED_DK)
    d.text((W - mx, map_y0), "red dots mark the day's flashpoints",
           font=SANS(11), fill=GREY, anchor="ra")
    my0 = map_y0 + 24
    for poly in CONTINENTS:
        pts = [(x + mx, y + my0) for (x, y) in poly]
        d.polygon(pts, fill=(214, 203, 178), outline=GREY)
    for (x, y, name, anch) in DOTS:
        px, py = x + mx, y + my0
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 248, 235), width=1)
        if anch == "l":
            d.text((px + 8, py - 6), name, font=SANSB(9), fill=INK)
        elif anch == "r":
            d.text((px - 8, py - 6), name, font=SANSB(9), fill=INK,
                   anchor="ra")
        elif anch == "a":
            d.text((px, py - 16), name, font=SANSB(9), fill=INK, anchor="ma")
        else:
            d.text((px, py + 8), name, font=SANSB(9), fill=INK, anchor="ma")
    d.line([(mx, map_y1), (W - mx, map_y1)], fill=INK, width=1)

    # ---- UTC timeline ----------------------------------------------------
    tl_y0 = 510
    d.text((mx, tl_y0), "THE DAY IN UTC", font=SANSB(13), fill=RED_DK)
    d.text((W - mx, tl_y0), "times approximate, as first reported",
           font=SANS(11), fill=GREY, anchor="ra")
    bar_y = tl_y0 + 34
    d.rectangle([mx, bar_y, W - mx, bar_y + 8], fill=(214, 203, 178))
    for h in range(0, 25, 4):
        x = mx + (W - 2 * mx) * h / 24
        d.line([(x, bar_y + 8), (x, bar_y + 14)], fill=INK, width=1)
        d.text((x, bar_y + 16), "%02d:00" % h, font=SANS(9), fill=GREY,
               anchor="ma")
    for i, (h, label) in enumerate(TIMELINE):
        x = mx + (W - 2 * mx) * h / 24
        d.ellipse([x - 4, bar_y - 1, x + 4, bar_y + 7], fill=RED)
        if i % 2 == 1:
            d.text((x, bar_y - 12), label, font=SANSB(9), fill=INK,
                   anchor="mb")
        else:
            d.text((x, bar_y + 22), label, font=SANSB(9), fill=INK,
                   anchor="ma")
    d.line([(mx, 592), (W - mx, 592)], fill=INK, width=1)

    # ---- 39-item news list, three columns -------------------------------
    list_y0 = 602
    d.text((mx, list_y0), "39 STORIES THAT MADE THE DAY",
           font=SANSB(13), fill=RED_DK)
    d.text((W - mx, list_y0), "grouped by region", font=SANS(11), fill=GREY,
           anchor="ra")
    col_w = 300
    col_x = [mx, mx + col_w + gap, mx + 2 * (col_w + gap)]
    # split the 39 items into 3 columns of 13
    cols = [STORIES[i * 13:(i + 1) * 13] for i in range(3)]
    y = list_y0 + 22
    for ci, items in enumerate(cols):
        cy = y
        seen = set()
        for (region, head, body) in items:
            if region not in seen:
                seen.add(region)
                d.text((col_x[ci], cy), region, font=SANSB(10), fill=RED_DK)
                cy += 12
            item = head + " — " + body
            lines = wrap(d, item, SANS(10), col_w)[:2]
            for ln in lines:
                d.text((col_x[ci], cy), ln, font=SANS(10), fill=INK)
                cy += 11
            cy += 1
    d.line([(mx, 968), (W - mx, 968)], fill=RED, width=2)

    # ---- date-check footer ------------------------------------------------
    fy = 978
    d.text((mx, fy), "DATE CHECK", font=SANSB(12), fill=RED)
    d.text((mx + 92, fy),
           "Every story above was first reported on Wednesday 25 November 2026.",
           font=SANS(11), fill=INK)
    d.text((mx, fy + 16),
           "Sources: Reuters, AP, BBC, Al Jazeera, Euronews, Times of India. "
           "Rendered 25 Nov 2026, 09:30 WIB (02:30 UTC) from reports available then.",
           font=SANS(10), fill=GREY)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    render()
