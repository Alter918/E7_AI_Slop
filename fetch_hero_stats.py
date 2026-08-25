#!/usr/bin/env python3
"""
Epic Seven Hero Win Rate Data Fetcher

Fetches hero win rate data from the Epic Seven API (epic7.onstove.com)
and outputs a sorted list by usage (pick) rate in descending order.

Output files:
  - hero_stats_sorted.txt : Sorted hero list
"""

import json
import urllib.request
import sys

BASE_URL = "https://e7api.onstove.com/gameApi/getPopularHero"
HEADERS = {
    "Content-Type": "application/json;charset=UTF-8",
    "Caller-Id": "WEB_STOVE_EPIC7",
    "Caller-Detail": "WEB_STOVE_EPIC7",
}

DEFAULT_SEASON = "pvp_rta_ss20"
DEFAULT_GRADE = "champion"
DEFAULT_LANG = "en"
PAGES_TO_FETCH = 10


def fetch_heroes(season_code, grade_code, lang):
    all_heroes = []
    for page in range(1, PAGES_TO_FETCH + 1):
        url = (
            f"{BASE_URL}?season_code={season_code}"
            f"&grade_code={grade_code}&current_page={page}&lang={lang}"
        )
        req = urllib.request.Request(url, method="POST", headers=HEADERS)
        resp = urllib.request.urlopen(req)
        data = json.loads(resp.read())
        body = data.get("value", {}).get("result_body", [])
        if not body:
            break
        for h in body:
            if h.get("pick_rate", 0) > 0 and not h["hero_code"].startswith("m"):
                name = h.get("hero_names", {}).get(h["hero_code"], h["hero_code"])
                all_heroes.append({
                    "name": name,
                    "hero_code": h["hero_code"],
                    "win_rate": h["win_rate"],
                    "pick_rate": h["pick_rate"],
                    "ban_rate": h.get("ban_rate", 0),
                })
    return all_heroes


def format_table(heroes):
    lines = []
    header = f"{'Rank':<6}{'Hero Name':<40}{'Usage Rate':>11}{'Win Rate':>10}{'Ban Rate':>10}"
    sep = "-" * len(header)
    lines.append(header)
    lines.append(sep)
    for i, h in enumerate(heroes, 1):
        lines.append(
            f"{i:<6}{h['name']:<40}{h['pick_rate']:>10.2f}%{h['win_rate']:>9.2f}%{h['ban_rate']:>9.2f}%"
        )
    return "\n".join(lines)


def main():
    season = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SEASON
    grade = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_GRADE

    print(f"Fetching hero data (season={season}, grade={grade})...")
    heroes = fetch_heroes(season, grade, DEFAULT_LANG)

    if not heroes:
        print("No hero data found. Check season/grade codes.")
        sys.exit(1)

    heroes.sort(key=lambda x: x["pick_rate"], reverse=True)

    table = format_table(heroes)
    print(table)

    outfile = "hero_stats_sorted.txt"
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(f"Epic Seven Hero Stats - Sorted by Usage (Pick) Rate\n")
        f.write(f"Season: {season} | Tier: {grade}\n")
        f.write(f"Total heroes: {len(heroes)}\n\n")
        f.write(table + "\n")
    print(f"\nResults saved to {outfile}")


if __name__ == "__main__":
    main()
