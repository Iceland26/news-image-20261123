#!/usr/bin/env python3
"""news-image-20261123 entry program.

Pure Python 3.13 standard library. Copies the pre-rendered front-page
image (entry.png, produced at build time by draw.py) to /output/entry.png.
The output is deterministic: it is byte-for-byte the bundled asset.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = os.path.join(HERE, "entry.png")
OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(ASSET, OUT_PATH)


if __name__ == "__main__":
    main()
