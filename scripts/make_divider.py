#!/usr/bin/env python3
"""Thin horizontal gradient divider, reused between README sections."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import ACCENT

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "divider.svg")

WIDTH = 835
HEIGHT = 2


def main():
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{ACCENT}" stop-opacity="0" />
      <stop offset="50%" stop-color="{ACCENT}" stop-opacity="0.6" />
      <stop offset="100%" stop-color="{ACCENT}" stop-opacity="0" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#g)" />
</svg>'''
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
