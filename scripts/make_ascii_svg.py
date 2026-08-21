#!/usr/bin/env python3
"""
Convert source-prepped.png into avi-ascii.svg: a monochrome ASCII portrait
that "prints" row by row via a left-to-right clip-path wipe, staggered
top to bottom, then freezes (no looping).
"""
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from theme import BG, FONT

RAMP = " .`:-=+*cs#%@"   # bright (sparse) -> dark (dense); leading space clears bg to nothing

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "portrait-source.png")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "portrait-ascii.svg")

GRID_W = 88    # character columns
GRID_H = 48    # character rows (matched to CHAR_H/CHAR_W ratio for a square source image)
CHAR_W = 6.2
CHAR_H = 11.5
FILL_COLOR = "#c9d1d9"   # light gray, monochrome only
ROW_DELAY_STEP = 0.055   # seconds between each row starting its wipe


def image_to_ascii_grid(path, cols, rows):
    img = Image.open(path).convert("L")
    img = img.resize((cols, rows), Image.LANCZOS)
    arr = np.array(img)

    ramp_len = len(RAMP)
    # bright pixel (255) -> index 0 (space), dark pixel (0) -> last glyph
    indices = ((255 - arr).astype(np.float32) / 255.0 * (ramp_len - 1)).round().astype(int)
    chars = np.vectorize(lambda i: RAMP[i])(indices)
    return chars  # shape (rows, cols) of single characters


def build_svg(chars):
    rows, cols = chars.shape
    width = cols * CHAR_W
    height = rows * CHAR_H

    row_elements = []
    for r in range(rows):
        line = "".join(chars[r])
        # Escape XML-sensitive characters that can appear in the ramp (none currently, but stay safe)
        line = (line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        y = (r + 1) * CHAR_H - 2
        delay = r * ROW_DELAY_STEP
        row_elements.append(
            f'<g class="row" style="animation-delay:{delay:.3f}s">'
            f'<text x="0" y="{y:.1f}" xml:space="preserve">{line}</text>'
            f'</g>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}"
     viewBox="0 0 {width:.0f} {height:.0f}">
  <style>
    text {{
      font-family: {FONT};
      font-size: {CHAR_H * 0.92:.1f}px;
      fill: {FILL_COLOR};
      white-space: pre;
      letter-spacing: -0.5px;
    }}
    .row {{
      clip-path: inset(0 100% 0 0);
      animation: wipe 0.35s steps(24) forwards;
    }}
    @keyframes wipe {{
      to {{ clip-path: inset(0 0 0 0); }}
    }}
  </style>
  <rect width="100%" height="100%" fill="{BG}" />
  {''.join(row_elements)}
</svg>'''
    return svg


def main():
    chars = image_to_ascii_grid(IN_PATH, GRID_W, GRID_H)
    svg = build_svg(chars)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH} ({GRID_W}x{GRID_H} chars)")


if __name__ == "__main__":
    main()
