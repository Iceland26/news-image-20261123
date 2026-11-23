#!/usr/bin/env python3
"""THE DAILY GLOBE - Monday 23 November 2026 in one image.

Pure stdlib (zlib + struct). Draws a 1024x1024 broadsheet front page
with a hand-made 5x7 bitmap font scaled up, and writes entry.png.
Deterministic: fixed palette, fixed geometry, no time, no randomness.
"""
import os
import struct
import zlib

W, H = 1024, 1024
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
NAVY = (0, 51, 102)
RED = (204, 0, 0)
BLUE = (0, 102, 204)
GOLD = (255, 204, 0)
GREY = (90, 90, 90)
LIGHT = (238, 240, 244)
PAPER = (252, 250, 244)

# 5x7 bitmap font, uppercase only (broadsheet style). Each glyph is
# 7 rows of 5 bits, written as strings of '#' / '.'.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '+': ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '~': ("00000", "00000", "01001", "10110", "00000", "00000", "00000"),
    '*': ("00000", "10101", "01110", "10101", "00000", "00000", "00000"),
    '•': ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            for xx in range(max(0, x), min(self.w, x + w)):
                self.px[base:base + 3] = bytes(c)
                base += 3

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d <= r * r:
                    self.set(xx, yy, c)
                elif not fill and abs(d - r * r) <= r * 2:
                    self.set(xx, yy, c)

    def triangle(self, pts, c):
        (x0, y0), (x1, y1), (x2, y2) = pts
        ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                       ((x1, y1), (x2, y2)),
                                       ((x2, y2), (x0, y0))):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by) or yy == ymax and yy == max(ay, by):
                    xs.append(ax + (yy - ay) * (bx - ax) / (by - ay))
            if len(xs) >= 2:
                self.rect(int(min(xs)), yy, int(max(xs)) - int(min(xs)) + 1, 1, c)

    def text(self, x, y, s, scale, c):
        """Draw uppercase text; returns width in px."""
        s = s.upper()
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for row in range(7):
                for col in range(5):
                    if g[row][col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, c)
            cx += 6 * scale
        return cx - x - scale

    def text_w(self, s, scale):
        return (len(s.upper()) * 6 - 1) * scale

    def text_center(self, cx, y, s, scale, c):
        self.text(cx - self.text_w(s, scale) // 2, y, s, scale, c)

    def wrap(self, s, scale, maxw):
        """Greedy word wrap, returns list of lines."""
        words, lines, cur = s.upper().split(), [], ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if self.text_w(trial, scale) <= maxw or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


def chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def save_png(cv, path):
    raw = b"".join(b"\x00" + bytes(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
                   for y in range(cv.h))
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 6))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---- pictograms (basic shapes only) ----

def pic_globe(cv, x, y, s):
    # cracked globe: blue circle, green land blobs, black crack
    cv.circle(x + s // 2, y + s // 2, s // 2, BLUE)
    cv.circle(x + s // 2, y + s // 2, s // 2 - 4, (40, 140, 220))
    cv.rect(x + s // 4, y + s // 4, s // 4, s // 5, (40, 180, 90))
    cv.rect(x + s // 2, y + s // 2, s // 4, s // 4, (40, 180, 90))
    cv.rect(x + s // 5, y + s * 2 // 3, s // 5, s // 6, (40, 180, 90))
    cv.line(x + s // 3, y + s // 6, x + s // 2, y + s // 2, BLACK, 5)
    cv.line(x + s // 2, y + s // 2, x + s * 2 // 3, y + s * 3 // 4, BLACK, 5)
    cv.line(x + s // 2, y + s // 2, x + s * 3 // 4, y + s // 3, BLACK, 4)


def pic_house(cv, x, y, s):
    cv.triangle([(x, y + s // 2), (x + s // 2, y), (x + s, y + s // 2)], RED)
    cv.rect(x + s // 8, y + s // 2, s * 3 // 4, s // 2, NAVY)
    cv.rect(x + s * 3 // 8, y + s * 2 // 3, s // 4, s // 3, GOLD)
    cv.line(x + s // 6, y + s // 6, x + s // 3, y + s // 3, GOLD, 4)
    cv.line(x + s * 5 // 6, y + s // 6, x + s * 2 // 3, y + s // 3, GOLD, 4)


def pic_chart(cv, x, y, s):
    cv.vline(x + 4, y, s, BLACK, 4)
    cv.hline(x + 4, y + s - 4, s, BLACK, 4)
    pts = [(x + 8, y + s // 4), (x + s // 3, y + s // 3),
           (x + s // 2, y + s // 2), (x + s * 2 // 3, y + s * 2 // 3),
           (x + s - 6, y + s - 10)]
    for a, b in zip(pts, pts[1:]):
        cv.line(a[0], a[1], b[0], b[1], RED, 5)
    cv.line(x + s - 6, y + s - 10, x + s - 6, y + s - 26, RED, 5)
    cv.line(x + s - 6, y + s - 10, x + s - 22, y + s - 10, RED, 5)


def pic_ship(cv, x, y, s):
    cv.triangle([(x, y + s // 2), (x + s, y + s // 2), (x + s * 4 // 5, y + s)],
                NAVY)
    cv.rect(x + s // 4, y + s // 6, s // 8, s // 3, BLACK)
    cv.rect(x + s // 2, y + s // 4, s // 8, s // 4, BLACK)
    cv.line(x, y + s - 4, x + s // 3, y + s - 12, BLUE, 4)
    cv.line(x + s // 3, y + s - 4, x + s * 2 // 3, y + s - 12, BLUE, 4)
    cv.line(x + s * 2 // 3, y + s - 4, x + s, y + s - 12, BLUE, 4)


def pic_podium(cv, x, y, s):
    cv.rect(x + s // 3, y + s // 2, s // 3, s // 2, NAVY)
    cv.rect(x, y + s * 2 // 3, s // 3, s // 3, BLUE)
    cv.rect(x + s * 2 // 3, y + s * 3 // 4, s // 3, s // 4, GREY)
    cv.text(x + s // 3 + 2, y + s // 8, "258", 2, RED)


def pic_refinery(cv, x, y, s):
    cv.rect(x + s // 6, y + s // 3, s // 5, s * 2 // 3, NAVY)
    cv.rect(x + s // 2, y + s // 2, s // 5, s // 2, NAVY)
    cv.rect(x + s * 3 // 4, y + s // 4, s // 8, s * 3 // 4, GREY)
    cv.triangle([(x + s // 4, y + s // 3), (x + s // 3, y),
                 (x + s * 5 // 12, y + s // 3)], GOLD)
    cv.triangle([(x + s // 4, y + s // 3), (x + s // 3, y + s // 6),
                 (x + s * 5 // 12, y + s // 3)], RED)


def pic_cuffs(cv, x, y, s):
    cv.circle(x + s // 4, y + s // 2, s // 4, GREY)
    cv.circle(x + s // 4, y + s // 2, s // 6, WHITE)
    cv.circle(x + s * 3 // 4, y + s // 2, s // 4, GREY)
    cv.circle(x + s * 3 // 4, y + s // 2, s // 6, WHITE)
    cv.line(x + s // 4, y + s // 2, x + s * 3 // 4, y + s // 2, BLACK, 5)


def pic_export(cv, x, y, s):
    cv.rect(x + s // 6, y + s // 2, s * 2 // 3, s // 2, BLUE)
    cv.text(x + s // 6 + 2, y + s // 2 + 6, "$1T", 2, WHITE)
    cv.line(x + s // 6, y + s // 2, x + s // 2, y + s // 6, RED, 6)
    cv.line(x + s // 2, y + s // 6, x + s - 4, y + s // 6, RED, 6)
    cv.line(x + s - 4, y + s // 6, x + s - 4, y + s // 4, RED, 6)


PICS = {"globe": pic_globe, "house": pic_house, "chart": pic_chart,
        "ship": pic_ship, "podium": pic_podium, "refinery": pic_refinery,
        "cuffs": pic_cuffs, "export": pic_export}

# ---- stories: (headline, deck, pictogram) ----
# Headlines <= 36 chars (one line at scale 4); decks <= 98 chars (2 lines).
STORIES = [
    ("STRIKE KILLS 10 NEAR KYIV",
     "Boy, 7, pulled alive from rubble after 14 hours in Dymer.",
     "house"),
    ("AI SELL-OFF ROCKS MARKETS",
     "Nikkei down 5.06%, S&P 500 down 3.7%.", "chart"),
    ("RUSSIAN WARSHIP SUNK OFF LIBYA",
     "Corvette Merkury hit by sea drones at Benghazi; cargo ship MV Angara also struck.",
     "ship"),
    ("DEMOCRATS WIN 258 HOUSE SEATS",
     "Largest US House majority in over 30 years.", "podium"),
    ("HOUTHIS CLAIM SAUDI REFINERY STRIKE",
     "Iran says it downed a US drone over the Strait of Hormuz.", "refinery"),
    ("FBI MOST-WANTED BOSS CAPTURED",
     "El Chapo Isidro seized in Sinaloa, Mexico.", "cuffs"),
    ("SOUTH KOREA EXPORTS TOP $1 TRILLION",
     "First time ever, driven by AI chip demand.", "export"),
]


def strip(cv, x, y, w, h, head, deck, pic):
    """One full-width story strip: pictogram left, headline + 2-line deck."""
    cv.rect(x, y, w, h, WHITE)
    cv.rect(x, y, 6, h, RED)
    cv.rect(x, y, w, 2, BLACK)
    cv.rect(x, y + h - 2, w, 2, BLACK)
    cv.rect(x, y, 2, h, BLACK)
    cv.rect(x + w - 2, y, 2, h, BLACK)
    PICS[pic](cv, x + 14, y + 14, 56)
    tx = x + 84
    cv.text(tx, y + 10, head, 4, NAVY)
    for i, ln in enumerate(cv.wrap(deck, 3, w - 100)[:2]):
        cv.text(tx, y + 40 + i * 21, ln, 3, BLACK)


def build():
    cv = Canvas(W, H, PAPER)
    # ---- masthead ----
    cv.rect(0, 0, W, 112, WHITE)
    cv.text_center(W // 2, 10, "THE DAILY GLOBE", 9, NAVY)
    cv.text_center(W // 2, 78, "MONDAY 23 NOVEMBER 2026", 4, RED)
    cv.rect(0, 112, W, 6, RED)
    cv.rect(0, 118, W, 2, NAVY)
    # ---- hero ----
    hx, hy, hw, hh = 24, 126, 976, 216
    cv.rect(hx, hy, hw, hh, WHITE)
    cv.rect(hx, hy, hw, 2, BLACK)
    cv.rect(hx, hy + hh - 2, hw, 2, BLACK)
    cv.rect(hx, hy, 2, hh, BLACK)
    cv.rect(hx + hw - 2, hy, 2, hh, BLACK)
    cv.text(hx + 20, hy + 12, "CLIMATE  •  FIRST COP FAILURE SINCE 2009", 2, RED)
    for i, ln in enumerate(["COP31 COLLAPSES", "IN TURKEY"]):
        cv.text(hx + 20, hy + 36 + i * 50, ln, 6, NAVY)
    deck = ("NO DEAL IN ANTALYA: EU AND ABOUT 130 NATIONS REJECT TEXT "
            "WITH NO MENTION OF FOSSIL FUELS.")
    ty = hy + 142
    for ln in cv.wrap(deck, 3, 600)[:3]:
        cv.text(hx + 20, ty, ln, 3, BLACK)
        ty += 22
    pic_globe(cv, hx + 680, hy + 24, 160)
    cv.text_center(hx + 760, hy + 190, "NO DEAL", 3, RED)
    # ---- 7 story strips ----
    sy = 352
    for i, (hd, dk, pc) in enumerate(STORIES):
        strip(cv, 24, sy + i * 90, 976, 84, hd, dk, pc)
    # ---- footer strip, 14px text ----
    fy = 976
    cv.rect(0, fy, W, 48, NAVY)
    cv.text_center(W // 2, fy + 8,
                   "ALSO: MARQUEZ WINS 8TH MOTOGP TITLE", 2, WHITE)
    cv.text_center(W // 2, fy + 28,
                   "CALIFORNIA SUES OPENAI  •  EBOLA TOLL UNDERCOUNTED IN DR CONGO",
                   2, GOLD)
    return cv


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "./output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    save_png(build(), path)
    print("wrote", path)


if __name__ == "__main__":
    main()
