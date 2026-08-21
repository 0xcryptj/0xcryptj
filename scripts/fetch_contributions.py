#!/usr/bin/env python3
"""
Fetch a GitHub user's public contribution calendar (no token required)
by scraping the same HTML fragment GitHub's own profile page uses,
and write derived stats to data/contributions.json.
"""
import json
import os
import sys
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_PROFILE_USER", "0xcryptj")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


import re

COUNT_RE = re.compile(r"([\d,]+)\s+contributions?", re.IGNORECASE)


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "profile-readme-bot"}, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day[data-date]")

    # Tooltip text ("5 contributions on August 3rd." / "No contributions on ...")
    # is a separate <tool-tip for="cell-id"> element, not an attribute on the cell.
    tooltip_by_target = {}
    for tip in soup.select("tool-tip[for]"):
        tooltip_by_target[tip.get("for")] = tip.get_text(strip=True)

    days = []
    for cell in cells:
        date = cell.get("data-date")
        if date is None:
            continue
        level = int(cell.get("data-level", 0))

        cell_id = cell.get("id")
        tooltip_text = tooltip_by_target.get(cell_id, "")
        if tooltip_text.lower().startswith("no contributions"):
            count = 0
        else:
            match = COUNT_RE.search(tooltip_text)
            count = int(match.group(1).replace(",", "")) if match else 0

        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda d: d["date"])
    return days


def derive_stats(days):
    if not days:
        return {}

    total = sum(d["count"] for d in days)
    best_day = max(days, key=lambda d: d["count"]) if days else None

    # current streak: walk backwards from most recent day
    current_streak = 0
    for d in reversed(days):
        if d["count"] > 0:
            current_streak += 1
        else:
            break

    # longest streak
    longest_streak = 0
    running = 0
    for d in days:
        if d["count"] > 0:
            running += 1
            longest_streak = max(longest_streak, running)
        else:
            running = 0

    # monthly totals for the last 12 months present
    monthly = {}
    for d in days:
        month_key = d["date"][:7]  # YYYY-MM
        monthly[month_key] = monthly.get(month_key, 0) + d["count"]

    return {
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly,
    }


def main():
    days = fetch_days()
    if not days:
        print("No contribution cells parsed — GitHub markup may have changed.", file=sys.stderr)
        sys.exit(1)

    stats = derive_stats(days)
    payload = {
        "username": USERNAME,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "days": days,
        "stats": stats,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {len(days)} days, {stats.get('total_contributions', 0)} total contributions -> {OUT_PATH}")


if __name__ == "__main__":
    main()
