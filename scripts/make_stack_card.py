#!/usr/bin/env python3
"""Stack card: same card language, just a wrapped row of tech pills."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import CARD_BG, BORDER, ACCENT, FONT, RADIUS, PILL_RADIUS

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "stack-card.svg")

STACK = ["Python", "Next.js", "React", "Supabase", "Docker", "Linux", "ESP32", "C++"]

WIDTH = 835
PAD = 24
PILL_H = 28
PILL_GAP = 8
ROW_GAP = 10
STAGGER = 0.05


def build_svg():
    char_w = 7.0
    x = PAD
    y = 50
    max_x = WIDTH - PAD

    pills = []
    for i, tag in enumerate(STACK):
        w = len(tag) * char_w + 22
        if x + w > max_x:
            x = PAD
            y += PILL_H + ROW_GAP
        delay = i * STAGGER
        pills.append(
            f'<g class="pill" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{PILL_H}" rx="{PILL_RADIUS}" '
            f'fill="none" stroke="{ACCENT}" stroke-opacity="0.5" />'
            f'<text x="{x + w/2:.1f}" y="{y + PILL_H/2 + 4}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="12.5" fill="{ACCENT}">{tag}</text>'
            f'</g>'
        )
        x += w + PILL_GAP

    height = y + PILL_H + PAD

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}"
     viewBox="0 0 {WIDTH} {height}">
  <style>
    .pill {{ opacity: 0; transform: translateY(4px); animation: pillIn 0.3s ease-out forwards; }}
    @keyframes pillIn {{ to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect width="100%" height="100%" rx="{RADIUS}" fill="{CARD_BG}" stroke="{BORDER}" />
  <text x="{PAD}" y="28" font-family="{FONT}" font-size="11" letter-spacing="2" fill="{ACCENT}">STACK</text>
  {''.join(pills)}
</svg>'''
    return svg


def main():
    svg = build_svg()
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
