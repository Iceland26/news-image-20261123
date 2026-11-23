# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)

**Bounty:** https://make.fun/bounty/news-image-20261123

## The Daily Globe — Monday, 23 November 2026

A clean, modern broadsheet front page in a single 1024×1024 image: off-white
paper, black ink, one deep-red accent, an elegant serif masthead, and a flat
vector illustration of the Antalya conference hall and its long negotiation
table.

The lead story is the collapse of COP31 in Turkey — no deal in Antalya after
the EU and some 130 countries rejected a final text with no mention of fossil
fuels, the first COP failure since 2009. Around it, a tidy grid of seven
further stories: a strike kills 10 near Kyiv (a seven-year-old survives 14
hours in the rubble in Dymer); an AI sell-off rocks markets (Nikkei −5.06%,
S&P 500 −3.7%); a Russian warship is sunk off Libya (the corvette Merkury and
the cargo ship MV Angara hit); Democrats win 258 House seats, the largest
U.S. House majority in 30+ years; the Houthis claim a Saudi refinery strike
while Iran claims it downed a U.S. drone over the Strait of Hormuz; the FBI
most-wanted boss El Chapo Isidro is arrested in Sinaloa, Mexico; and South
Korea's exports top $1 trillion for the first time, driven by AI chip demand.
An "Also in the News" footer adds: Marquez wins his 8th MotoGP title,
California sues OpenAI, and the Ebola toll is undercounted in DR Congo.

## How it works

- `draw.py` — build-time renderer (Pillow). Draws the page at 2048×2048 with
  serif and sans type, then downscales to 1024×1024 with LANCZOS and saves
  `entry.png`. Pillow is used only at build time.
- `main.py` — the submitted program. Pure Python 3.13 standard library, no
  third-party imports: it copies the bundled `entry.png` asset to
  `/output/entry.png`, creating the output directory if needed. The output is
  deterministic — byte-for-byte the bundled asset, 1024×1024, under the
  1,048,576-byte limit.

## Run it

```sh
python3 main.py   # writes /output/entry.png
```
