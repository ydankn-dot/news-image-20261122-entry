#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

Fresh layout, written for news-image-20261122: masthead, a large lead
panel (burning cargo ship at sea) with a side column, two rows of story
cards, and a source footer. Output: entry.png, 1024x1024.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 22, 22)
RED = (178, 34, 28)
NAVY = (18, 42, 74)
SKY = (148, 178, 205)
SEA = (38, 68, 96)
SEA_DARK = (24, 46, 68)
ORANGE = (232, 116, 28)
GOLD = (214, 158, 44)
CARD = (255, 255, 255)
GREY = (88, 88, 88)
RULE = (180, 172, 156)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning list of lines fitting width px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def headline(draw, xy, text, fnt, width, fill=INK, leading=None):
    return para(draw, xy, text, fnt, width, fill=fill, leading=leading)


def card(draw, box, title, body, title_size=30, body_size=19,
         title_color=INK, accent=RED):
    """A white story card: coloured kicker bar, headline, body text."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=RULE, width=2)
    draw.rectangle([x0, y0, x1, y0 + 8], fill=accent)
    tf = font(SERIF_B, title_size)
    bf = font(SANS, body_size)
    y = headline(draw, (x0 + 16, y0 + 20), title, tf, x1 - x0 - 32)
    para(draw, (x0 + 16, y + 8), body, bf, x1 - x0 - 32)


def draw_ship_scene(draw, box):
    """Burning cargo ship on a grey sea at dusk, inside box.

    All geometry is relative to the box so the hull always stays
    above the caption strip at the bottom.
    """
    x0, y0, x1, y1 = box
    bh = y1 - y0
    cap = 34                      # caption strip height
    sea_top = y0 + int(bh * 0.42)
    draw.rectangle(box, fill=SKY)
    # low sun glow behind smoke
    draw.ellipse([x1 - 190, y0 + 12, x1 - 96, y0 + 106], fill=(238, 196, 120))
    # distant headland
    draw.polygon([(x0, sea_top), (x0 + 130, sea_top - 44),
                  (x0 + 260, sea_top)], fill=(96, 116, 128))
    # sea
    draw.rectangle([x0, sea_top, x1, y1 - cap], fill=SEA)
    for i, yy in enumerate(range(sea_top + 16, y1 - cap - 4, 24)):
        shade = SEA_DARK if i % 2 else (52, 88, 118)
        draw.line([(x0 + 12, yy), (x1 - 12, yy)], fill=shade, width=5)
    # ship hull: top edge hy, depth fits above the caption strip
    hy = sea_top + 34
    depth = (y1 - cap) - hy - 8
    hx0, hx1 = x0 + 52, x1 - 52
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 40, hy + depth),
                  (hx0 + 40, hy + depth)], fill=(30, 30, 34))
    draw.rectangle([hx0, hy - 6, hx1, hy + 2], fill=(178, 34, 28))
    # containers on deck
    ch = int(depth * 0.62)
    for i, cx in enumerate(range(hx0 + 28, hx1 - 108, 76)):
        col = (196, 84, 44) if i % 2 == 0 else (74, 110, 130)
        draw.rectangle([cx, hy - ch, cx + 64, hy - 8], fill=col,
                       outline=(20, 20, 20), width=2)
    # bridge tower
    bw = 62
    draw.rectangle([hx1 - 112, hy - ch - 42, hx1 - 50, hy - 8],
                   fill=(226, 224, 216), outline=(20, 20, 20), width=2)
    for wy in (hy - ch - 32, hy - ch - 12):
        draw.rectangle([hx1 - 103, wy, hx1 - 59, wy + 10], fill=(30, 42, 58))
    # funnel with flame
    draw.rectangle([hx0 + 92, hy - ch - 6, hx0 + 130, hy - 8],
                   fill=(52, 52, 52))
    draw.polygon([(hx0 + 96, hy - ch - 6), (hx0 + 108, hy - ch - 44),
                  (hx0 + 118, hy - ch - 20), (hx0 + 126, hy - ch - 6)],
                 fill=ORANGE)
    # smoke plumes drifting up-left
    for sx, sy, r in [(hx0 + 118, hy - ch - 52, 20),
                      (hx0 + 138, hy - ch - 76, 24),
                      (hx0 + 112, hy - ch - 92, 17)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(88, 88, 88))
    # caption strip
    draw.rectangle([x0, y1 - cap, x1, y1], fill=(22, 22, 22))
    cf = font(SANS_B, 17)
    draw.text((x0 + 14, y1 - cap + 7),
              "THE SPARTA II, STILL BURNING IN THE GULF OF FINLAND",
              font=cf, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # margin

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((m, 14), "THE WORLD IN ONE DAY", font=font(SERIF_B, 54),
           fill=(255, 255, 255))
    d.text((m, 76), "SUNDAY  22  NOVEMBER  2026",
           font=font(SANS_B, 26), fill=GOLD)
    d.text((W - m - 250, 84), "WORLD  •  SUNDAY EDITION",
           font=font(SANS, 18), fill=(200, 200, 200))
    d.line([(0, 122), (W, 122)], fill=RED, width=5)

    # ---- lead panel (left) ----
    lx0, ly0, lx1 = m, 138, 668
    ly1 = 560
    d.rectangle([lx0, ly0, lx1, ly1], fill=CARD, outline=RULE, width=2)
    d.rectangle([lx0, ly0, lx1, ly0 + 8], fill=RED)
    y = headline(d, (lx0 + 16, ly0 + 22),
                 "RUSSIAN CARGO SHIP BURNS OFF FINLAND",
                 font(SERIF_B, 40), lx1 - lx0 - 32, leading=46)
    y = para(d, (lx0 + 16, y + 6),
             "Drone strike in the Gulf of Finland leaves the Sparta II "
             "smouldering; 16 crew evacuated, vessel towed toward Kaliningrad.",
             font(SANS, 20), lx1 - lx0 - 32)
    draw_ship_scene(d, (lx0 + 16, 332, lx1 - 16, ly1 - 16))

    # ---- right column: COP31 + Indonesia ----
    rx0, rx1 = 684, W - m
    card(d, (rx0, 138, rx1, 348),
         "CLIMATE TALKS COLLAPSE",
         "COP31 ends with no agreement as the final draft is rejected; "
         "a fossil-fuel phase-out is blocked.",
         title_size=29, body_size=19, accent=NAVY)
    card(d, (rx0, 364, rx1, 560),
         "FACTORY FIRE IN INDONESIA",
         "Candy-factory blaze in Serang kills 3; 36 people still missing.",
         title_size=29, body_size=19, accent=ORANGE)

    # ---- middle row: three cards ----
    row_y0, row_y1 = 576, 786
    cw = (W - 2 * m - 32) // 3
    # (title, body, accent) triples
    cards = [
        ("BOAT CAPSIZES IN NIGERIA",
         "At least 24 dead after a boat carrying mourners overturns "
         "in Bayelsa State.", RED),
        ("BEPICOLOMBO REACHES MERCURY",
         "After an eight-year journey, the ESA-JAXA probe enters orbit "
         "around Mercury.", NAVY),
        ("MEXICO CAPTURES 'EL CHAPO ISIDRO'",
         "FBI most-wanted fugitive Fausto Isidro Meza Flores arrested "
         "by the military.", GOLD),
    ]
    for i, (t, b, acc) in enumerate(cards):
        x0 = m + i * (cw + 16)
        card(d, (x0, row_y0, x0 + cw, row_y1), t, b,
             title_size=26, body_size=19, accent=acc)

    # ---- bottom row: three short items ----
    by0, by1 = 802, 946
    items = [
        ("SEOUL MINISTER QUITS",
         "South Korea's education chief resigns in an AI-cheating row "
         "over the college entrance exam."),
        ("DEMOCRATS TAKE US HOUSE",
         "US House majority secured, 258 seats or more — the largest "
         "since 1992."),
        ("VERSTAPPEN WINS IN VEGAS",
         "Max Verstappen takes the Las Vegas Grand Prix, his third win "
         "there in four years."),
    ]
    for i, (t, b) in enumerate(items):
        x0 = m + i * (cw + 16)
        d.rectangle([x0, by0, x0 + cw, by1], fill=CARD, outline=RULE, width=2)
        d.rectangle([x0, by0, x0 + cw, by0 + 6], fill=INK)
        y = headline(d, (x0 + 14, by0 + 16), t, font(SERIF_B, 23),
                     cw - 28, leading=27)
        para(d, (x0 + 14, y + 6), b, font(SANS, 17), cw - 28)

    # ---- footer ----
    d.line([(m, 968), (W - m, 968)], fill=RULE, width=2)
    d.text((m, 978), "Sources: Reuters, Al Jazeera, AP, AFP  •  22 November 2026",
           font=font(SANS, 17), fill=GREY)
    foot_r = "make.fun news-image-20261122"
    d.text((W - m - d.textlength(foot_r, font=font(SANS, 17)), 978),
           foot_r, font=font(SANS, 17), fill=GREY)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
