#!/usr/bin/env python3
"""
Render data/contributions.json into an animated SVG contribution heatmap:
53 columns (weeks) x 7 rows (days), diagonal slide-in reveal, GitHub-ish
green ramp with a neon top level. Pure SVG/CSS keyframes -- no JS.
"""
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from theme import CARD_BG, BORDER, MUTED, ACCENT, FONT, RADIUS

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 12          # box size
GAP = 3             # spacing between boxes
BOX_RADIUS = 2
LEFT_PAD = 24        # room for nothing fancy, just margin
TOP_PAD = 48
LEGEND_H = 20
FOOTER_H = 30


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def weeks_from_days(days):
    """Bucket days into 53 columns of 7 (Sun-Sat), most recent last."""
    # Pad the front so the first column starts on a Sunday.
    first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
    lead_gap = (first_date.weekday() + 1) % 7  # python Mon=0 -> convert to Sun=0
    padded = [None] * lead_gap + days

    weeks = []
    for i in range(0, len(padded), 7):
        week = padded[i:i + 7]
        while len(week) < 7:
            week.append(None)
        weeks.append(week)
    return weeks


def build_svg(payload):
    days = payload["days"]
    stats = payload.get("stats", {})
    weeks = weeks_from_days(days)
    n_weeks = len(weeks)

    width = LEFT_PAD * 2 + n_weeks * (CELL + GAP)
    height = TOP_PAD + 7 * (CELL + GAP) + LEGEND_H + FOOTER_H

    boxes = []
    delay_step = 0.006  # stagger per diagonal index, keeps total reveal short
    max_level = max((d["level"] for d in days if d), default=0) or 1

    for wi, week in enumerate(weeks):
        for di, day in enumerate(week):
            if day is None:
                continue
            level = min(day["level"], 5)
            color = PALETTE[level]
            x = LEFT_PAD + wi * (CELL + GAP)
            y = TOP_PAD + di * (CELL + GAP)
            diag = wi + di
            delay = diag * delay_step
            title = f"{day['count']} contributions on {day['date']}" if day["count"] else f"No contributions on {day['date']}"
            boxes.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{BOX_RADIUS}" ry="{BOX_RADIUS}" fill="{color}" '
                f'style="animation-delay:{delay:.3f}s"><title>{title}</title></rect>'
            )

    legend_y = TOP_PAD + 7 * (CELL + GAP) + 4
    legend_x = width - LEFT_PAD - (len(PALETTE) * (CELL + GAP)) - 60
    legend_boxes = []
    for i, color in enumerate(PALETTE):
        lx = legend_x + 40 + i * (CELL + GAP)
        legend_boxes.append(
            f'<rect x="{lx}" y="{legend_y}" width="{CELL - 2}" height="{CELL - 2}" '
            f'rx="{BOX_RADIUS}" ry="{BOX_RADIUS}" fill="{color}" />'
        )

    total = stats.get("total_contributions", 0)
    streak = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    if streak > 0:
        footer_text = f"{total:,} contributions in the last year · {streak}d streak"
    elif longest > 0:
        footer_text = f"{total:,} contributions in the last year · best streak {longest}d"
    else:
        footer_text = f"{total:,} contributions in the last year"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"
     viewBox="0 0 {width} {height}" font-family="{FONT}">
  <style>
    .cell {{
      opacity: 0;
      transform: translate(-6px, -6px);
      animation: reveal 0.5s ease-out forwards;
    }}
    @keyframes reveal {{
      to {{ opacity: 1; transform: translate(0, 0); }}
    }}
    .legend-label {{ fill: {MUTED}; font-size: 11px; }}
    .footer {{ fill: {MUTED}; font-size: 12px; }}
  </style>
  <rect width="100%" height="100%" rx="{RADIUS}" fill="{CARD_BG}" stroke="{BORDER}" />
  <text x="{LEFT_PAD}" y="28" font-size="11" letter-spacing="2" fill="{ACCENT}">ACTIVITY</text>
  {''.join(boxes)}
  <text x="{legend_x}" y="{legend_y + CELL - 2}" class="legend-label">Less</text>
  {''.join(legend_boxes)}
  <text x="{legend_x + 40 + len(PALETTE) * (CELL + GAP) + 6}" y="{legend_y + CELL - 2}" class="legend-label">More</text>
  <text x="{LEFT_PAD}" y="{height - 10}" class="footer">{footer_text}</text>
</svg>'''
    return svg


def main():
    payload = load_data()
    svg = build_svg(payload)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
