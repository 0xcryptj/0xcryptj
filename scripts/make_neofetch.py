#!/usr/bin/env python3
"""
Neofetch box: the classic key:value system-info layout, but styled as a
clean bordered card (small-caps accent label, no macOS window chrome,
no fake title bar) to match the rest of the profile kit.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import CARD_BG, BORDER, TEXT, MUTED, ACCENT, FONT, RADIUS

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "neofetch.svg")

ROWS = [
    ("now", "building AgentSec + Forager"),
    ("focus", "cybersecurity, embedded systems, web3"),
    ("stack", "python, next.js/react, supabase, linux"),
    ("into", "3D printing, retro gaming, homelab"),
]

WIDTH = 490
PAD = 24
LINE_H = 30
TOP_PAD = 54
STAGGER = 0.1


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg():
    height = TOP_PAD + len(ROWS) * LINE_H + 20
    key_col_w = max(len(k) for k, _ in ROWS) * 8 + 14

    rows_svg = []
    for i, (key, value) in enumerate(ROWS):
        y = TOP_PAD + i * LINE_H
        delay = i * STAGGER
        rows_svg.append(
            f'<g class="fade-row" style="animation-delay:{delay:.2f}s">'
            f'<text x="{PAD}" y="{y}" font-family="{FONT}" font-size="14" fill="{ACCENT}" font-weight="600">{esc(key)}</text>'
            f'<text x="{PAD + key_col_w}" y="{y}" font-family="{FONT}" font-size="14" fill="{TEXT}">{esc(value)}</text>'
            f'</g>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}"
     viewBox="0 0 {WIDTH} {height}">
  <style>
    .fade-row {{
      opacity: 0;
      transform: translateX(-8px);
      animation: fadeSlide 0.4s ease-out forwards;
    }}
    @keyframes fadeSlide {{
      to {{ opacity: 1; transform: translateX(0); }}
    }}
  </style>
  <rect width="100%" height="100%" rx="{RADIUS}" fill="{CARD_BG}" stroke="{BORDER}" />
  <text x="{PAD}" y="30" font-family="{FONT}" font-size="11" letter-spacing="2" fill="{ACCENT}">NEOFETCH</text>
  <line x1="{PAD}" y1="40" x2="{WIDTH - PAD}" y2="40" stroke="{BORDER}" stroke-width="1" />
  {''.join(rows_svg)}
</svg>'''
    return svg


def main():
    svg = build_svg()
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
