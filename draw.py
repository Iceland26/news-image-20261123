#!/usr/bin/env python3
"""Build-time renderer for The Daily Globe front page (news-image-20261123).

Renders at 2048x2048 with Pillow, downscales to 1024x1024 with LANCZOS,
and saves the result as entry.png next to this file. Pillow is used only
at build time; the submitted program (main.py) is pure stdlib.
"""
from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2048  # render size; final is 1024

PAPER = (250, 247, 242)
INK = (26, 24, 21)
MUTED = (107, 101, 96)
ACCENT = (158, 27, 27)       # deep red, the single accent
RULE = (26, 24, 21)
LIGHT_RULE = (198, 190, 178)
NAVY = (31, 53, 82)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SERIF_BI = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, font, fill=INK, tracking=0):
    if tracking:
        widths = [draw.textlength(c, font=font) for c in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = cx - total / 2
        for c, w in zip(text, widths):
            draw.text((x, y), c, font=font, fill=fill)
            x += w + tracking
        return total
    w = draw.textlength(text, font=font)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return w


def left(draw, x, y, text, font, fill=INK, tracking=0):
    if tracking:
        for c in text:
            draw.text((x, y), c, font=font, fill=fill)
            x += draw.textlength(c, font=font) + tracking
        return x
    draw.text((x, y), text, font=font, fill=fill)
    return x + draw.textlength(text, font=font)


# ---------------------------------------------------------------- illustration
def illustration(img, x0, y0, x1, y1):
    d = ImageDraw.Draw(img)
    # sky
    d.rectangle([x0, y0, x1, y1], fill=(217, 226, 228))
    # distant Taurus mountains above Antalya
    d.polygon([(x0, y0 + 150), (x0 + 260, y0 + 40), (x0 + 520, y0 + 150)], fill=(168, 182, 186))
    d.polygon([(x0 + 380, y0 + 150), (x0 + 700, y0 + 20), (x0 + 1020, y0 + 150)], fill=(183, 196, 199))
    d.polygon([(x1 - 560, y0 + 150), (x1 - 260, y0 + 55), (x1, y0 + 150)], fill=(168, 182, 186))
    # sun disc, flat
    d.ellipse([x1 - 300, y0 + 42, x1 - 208, y0 + 134], fill=(233, 197, 116))

    bw = x1 - x0
    bx0, bx1 = x0 + int(bw * 0.16), x1 - int(bw * 0.16)
    by0, by1 = y0 + 88, y1 - 110
    # conference centre: clean modern slab with glass curtain wall
    d.rectangle([bx0, by0, bx1, by1], fill=(240, 241, 240))
    d.rectangle([bx0 - 26, by0 - 22, bx1 + 26, by0 + 4], fill=NAVY)  # roof slab
    cols, rows = 12, 2
    cw = (bx1 - bx0) / cols
    ch = (by1 - by0 - 54) / rows
    for r in range(rows):
        for c in range(cols):
            gx0 = bx0 + 14 + c * cw
            gy0 = by0 + 18 + r * ch
            tone = (127, 168, 184) if (r + c) % 3 else (104, 148, 168)
            if (r * cols + c) % 7 == 3:
                tone = (52, 66, 78)  # a few dark, emptied rooms
            d.rectangle([gx0, gy0, gx0 + cw - 10, gy0 + ch - 10], fill=tone)
    # entrance band with summit wordmark
    d.rectangle([bx0, by1 - 40, bx1, by1], fill=NAVY)
    f_sign = F(SANS_B, 30)
    centered(d, (bx0 + bx1) / 2, by1 - 35, "C O P 3 1   ·   A N T A L Y A", f_sign, fill=(255, 255, 255))
    # flag poles
    for i, col in enumerate([(158, 27, 27), (38, 84, 160), (240, 200, 60), (46, 125, 80)]):
        px = bx0 + 60 + i * 64
        d.line([px, by0 - 22, px, by0 - 84], fill=(90, 90, 90), width=4)
        d.rectangle([px, by0 - 84, px + 40, by0 - 58], fill=col)
    # plaza
    d.rectangle([x0, y1 - 110, x1, y1], fill=(206, 193, 168))
    # delegates seated behind the long negotiation table: heads and
    # shoulders only, drawn first so the table front covers their bases
    tx0, tx1 = x0 + int(bw * 0.30), x1 - int(bw * 0.30)
    ty0, ty1 = y1 - 64, y1 - 12
    for i in range(6):
        hx = tx0 + 70 + i * ((tx1 - tx0 - 140) // 5)
        d.ellipse([hx - 13, ty0 - 40, hx + 13, ty0 - 14], fill=(24, 24, 27))
        d.pieslice([hx - 21, ty0 - 26, hx + 21, ty0 + 20], 180, 360, fill=(24, 24, 27))
    # long negotiation table, front view
    d.polygon([(tx0 + 60, ty0), (tx1 - 60, ty0), (tx1, ty1), (tx0, ty1)], fill=(43, 43, 46))
    d.rectangle([tx0 + 60, ty0 - 6, tx1 - 60, ty0 + 2], fill=(70, 70, 74))
    # scattered papers on the table
    for i in range(6):
        px = tx0 + 110 + i * ((tx1 - tx0 - 220) // 5)
        d.rectangle([px, ty0 + 16, px + 34, ty0 + 30], fill=(245, 244, 240))
    # one delegate walking away, briefcase in hand
    wx, wy = x1 - int(bw * 0.13), y1 - 110
    d.ellipse([wx - 11, wy - 110, wx + 11, wy - 88], fill=(24, 24, 27))
    d.polygon([(wx - 13, wy - 90), (wx + 13, wy - 90), (wx + 9, wy - 32), (wx - 9, wy - 32)], fill=(24, 24, 27))
    d.line([wx - 7, wy - 32, wx - 14, wy], fill=(24, 24, 27), width=8)
    d.line([wx + 7, wy - 32, wx + 16, wy], fill=(24, 24, 27), width=8)
    d.line([wx + 12, wy - 76, wx + 30, wy - 50], fill=(24, 24, 27), width=7)
    d.rectangle([wx + 22, wy - 54, wx + 56, wy - 24], fill=(96, 64, 40))
    # frame
    d.rectangle([x0, y0, x1, y1], outline=(120, 118, 110), width=2)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (S, S), PAPER)
    d = ImageDraw.Draw(img)
    M = 88            # margin
    R = S - M         # right edge
    CX = S // 2

    # ---- top folio line
    f_folio = F(SANS_B, 30)
    left(d, M, 52, "INDEPENDENT SINCE 1885", f_folio, MUTED, tracking=2)
    centered(d, CX, 52, "WORLD EDITION", f_folio, MUTED, tracking=2)
    w = d.textlength("LATE CITY FINAL", font=f_folio) + 2 * 15
    left(d, R - w, 52, "LATE CITY FINAL", f_folio, MUTED, tracking=2)
    d.line([M, 96, R, 96], fill=RULE, width=3)

    # ---- masthead
    centered(d, CX, 112, "The Daily Globe", F(DISPLAY, 148))
    d.line([M, 292, R, 292], fill=RULE, width=7)
    d.line([M, 306, R, 306], fill=RULE, width=2)
    f_date = F(SANS_B, 30)
    left(d, M, 322, "ANTALYA  ·  LONDON  ·  NEW YORK", f_date, INK)
    centered(d, CX, 322, "Monday, 23 November 2026", F(SERIF_BI, 34))
    w = d.textlength("VOL. CXLI — No. 328", font=f_date)
    left(d, R - w, 322, "VOL. CXLI — No. 328", f_date, INK)
    d.line([M, 372, R, 372], fill=RULE, width=3)

    # ---- lead story
    y = 396
    left(d, M, y, "CLIMATE SUMMIT  ·  ANTALYA, TURKEY", F(SANS_B, 30), ACCENT, tracking=3)
    y += 52
    centered(d, CX, y, "COP31 Collapses in Turkey", F(SERIF_B, 118))
    y += 148
    f_dek = F(SERIF_I, 43)
    for ln in wrap(d, "No deal in Antalya as the EU and some 130 countries reject a final "
                      "text with no mention of fossil fuels — the first COP failure since 2009.",
                   f_dek, R - M):
        centered(d, CX, y, ln, f_dek, (58, 54, 50))
        y += 56
    y += 14
    illustration(img, M, y, R, y + 300)
    d = ImageDraw.Draw(img)
    y += 312
    f_cap = F(SANS, 30)
    centered(d, CX, y, "The negotiation table in Antalya, where delegates failed to agree a text.  ·  ILLUSTRATION FOR THE DAILY GLOBE",
             f_cap, MUTED)
    y += 48
    f_body = F(SERIF, 37)
    for ln in wrap(d, "The summit ended without an agreement after the European Union and around "
                      "130 countries refused to sign a closing text that made no mention of fossil "
                      "fuels — the first time a COP has collapsed without a deal since 2009.",
                   f_body, R - M):
        d.text((M, y), ln, font=f_body, fill=INK)
        y += 50
    y += 18
    d.line([M, y, R, y], fill=RULE, width=3)
    y += 22

    # ---- secondary grid
    def story(x, ytop, wdt, kicker, headline, summary, hsize=47, ssize=33, hlines_max=2):
        left(d, x, ytop, kicker, F(SANS_B, 30), ACCENT, tracking=2)
        yy = ytop + 48
        f_h = F(SERIF_B, hsize)
        for ln in wrap(d, headline, f_h, wdt)[:hlines_max]:
            d.text((x, yy), ln, font=f_h, fill=INK)
            yy += int(hsize * 1.08)
        yy += 4
        f_s = F(SERIF, ssize)
        for ln in wrap(d, summary, f_s, wdt):
            d.text((x, yy), ln, font=f_s, fill=(58, 54, 50))
            yy += int(ssize * 1.22)
        return yy

    colw = (R - M - 56) // 2
    x2 = M + colw + 56
    row1 = y
    b1 = story(M, row1, colw, "UKRAINE", "Strike Kills 10 Near Kyiv",
               "A seven-year-old girl survives 14 hours buried in the rubble in Dymer.")
    b2 = story(x2, row1, colw, "MARKETS", "AI Sell-Off Rocks Markets",
               "The Nikkei plunges 5.06% and the S&P 500 falls 3.7% as investors flee AI stocks.")
    row2 = max(b1, b2) + 16
    d.line([M, row2 - 14, R, row2 - 14], fill=LIGHT_RULE, width=2)
    d.line([CX, row1 + 2, CX, row2 - 26], fill=LIGHT_RULE, width=2)
    b1 = story(M, row2, colw, "MEDITERRANEAN", "Russian Warship Sunk Off Libya",
               "A sea drone hits the corvette Merkury in Benghazi; the cargo ship MV Angara is also hit.")
    b2 = story(x2, row2, colw, "WASHINGTON", "Democrats Win 258 House Seats",
               "The party takes the largest U.S. House majority in more than 30 years.")
    row3 = max(b1, b2) + 16
    d.line([M, row3 - 14, R, row3 - 14], fill=LIGHT_RULE, width=2)
    d.line([CX, row2 + 2, CX, row3 - 26], fill=LIGHT_RULE, width=2)

    col3 = (R - M - 2 * 44) // 3
    xs = [M, M + col3 + 44, M + 2 * (col3 + 44)]
    story(xs[0], row3, col3, "MIDDLE EAST", "Houthis Claim Saudi Refinery Strike",
          "Iran says it downed a U.S. drone over the Strait of Hormuz.", hsize=41, ssize=31)
    story(xs[1], row3, col3, "MEXICO", "FBI Most-Wanted Boss Captured",
          "El Chapo Isidro is arrested in Sinaloa, Mexico.", hsize=41, ssize=31)
    story(xs[2], row3, col3, "SOUTH KOREA", "Exports Top $1 Trillion",
          "A first ever, driven by AI chip demand.", hsize=41, ssize=31)
    for vx in (xs[1] - 22, xs[2] - 22):
        d.line([vx, row3 + 2, vx, row3 + 200], fill=LIGHT_RULE, width=2)

    # ---- footer band
    fy = 1752
    d.rectangle([M, fy, R, 1992], fill=(24, 23, 21))
    left(d, M + 36, fy + 24, "ALSO IN THE NEWS", F(SANS_B, 30), (233, 120, 110), tracking=3)
    items = [
        "Marquez wins his 8th MotoGP title",
        "California sues OpenAI",
        "Ebola toll undercounted in DR Congo",
    ]
    f_item = F(SERIF_B, 35)
    iy = fy + 72
    for it in items:
        centered(d, CX, iy, it, f_item, (250, 247, 242))
        iy += 48
    # colophon
    centered(d, CX, 2006, "THE DAILY GLOBE  ·  MONDAY, 23 NOVEMBER 2026  ·  WORLD EDITION",
             F(SANS, 30), MUTED, tracking=2)

    out = img.resize((1024, 1024), Image.LANCZOS)
    path = os.path.join(HERE, "entry.png")
    out.save(path, optimize=True)
    print("saved", path, os.path.getsize(path))


if __name__ == "__main__":
    build()
