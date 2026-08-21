#!/usr/bin/env python3
"""
Projects card: a small-caps label, then a stack of project rows —
name, one-line description, and small tag pills. Same card language
as identity-card.svg for visual consistency.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from theme import CARD_BG, BORDER, TEXT, MUTED, ACCENT, FONT, RADIUS, PILL_RADIUS

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "projects-card.svg")

PROJECTS = [
    {
        "name": "AgentSec",
        "desc": "Security audit tool correlating 10 scanners against OWASP, CWE, NIST",
        "tags": ["Python", "OWASP", "CWE", "NIST"],
    },
    {
        "name": "Forager",
        "desc": "Non-custodial multi-chain dApp for burning dust tokens",
        "tags": ["Solana", "Sui", "Stellar", "EVM"],
    },
]

WIDTH = 835
PAD = 24
ROW_GAP = 14
STAGGER = 0.1


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg():
    y = 52
    blocks = []
    tiny_pill_h = 22
    char_w = 6.2

    for pi, proj in enumerate(PROJECTS):
        delay = pi * STAGGER
        name_y = y
        desc_y = y + 22
        pills_y = y + 34

        pills_svg = []
        x = PAD
        for tag in proj["tags"]:
            w = len(tag) * char_w + 18
            pills_svg.append(
                f'<rect x="{x:.1f}" y="{pills_y}" width="{w:.1f}" height="{tiny_pill_h}" '
                f'rx="{PILL_RADIUS}" fill="none" stroke="{MUTED}" stroke-opacity="0.6" />'
                f'<text x="{x + w/2:.1f}" y="{pills_y + tiny_pill_h/2 + 4}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="11" fill="{MUTED}">{esc(tag)}</text>'
            )
            x += w + 8

        blocks.append(
            f'<g class="fade" style="animation-delay:{delay:.2f}s">'
            f'<text x="{PAD}" y="{name_y}" font-family="{FONT}" font-size="17" font-weight="700" '
            f'fill="{ACCENT}">{esc(proj["name"])}</text>'
            f'<text x="{PAD}" y="{desc_y}" font-family="{FONT}" font-size="12.5" '
            f'fill="{TEXT}">{esc(proj["desc"])}</text>'
            f'{"".join(pills_svg)}'
            f'</g>'
        )
        y += 34 + tiny_pill_h + ROW_GAP + 20

    height = y + PAD - ROW_GAP

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}"
     viewBox="0 0 {WIDTH} {height}">
  <style>
    .fade {{ opacity: 0; transform: translateY(6px); animation: fadeIn 0.45s ease-out forwards; }}
    @keyframes fadeIn {{ to {{ opacity: 1; transform: translateY(0); }} }}
  </style>
  <rect width="100%" height="100%" rx="{RADIUS}" fill="{CARD_BG}" stroke="{BORDER}" />
  <text x="{PAD}" y="28" font-family="{FONT}" font-size="11" letter-spacing="2" fill="{ACCENT}">BUILDING</text>
  {''.join(blocks)}
</svg>'''
    return svg


def main():
    svg = build_svg()
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
