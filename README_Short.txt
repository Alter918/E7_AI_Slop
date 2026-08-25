Epic Seven Hero Stats Fetcher
=============================

Fetches RTA hero statistics from the Epic Seven API (epic7.onstove.com)
and outputs them sorted by usage (pick) rate in descending order.

Requirements:
  - Python 3.6+
  - No external packages required (uses only stdlib)

Usage:
  python3 fetch_hero_stats.py [season_code] [grade_code]

Examples:
  python3 fetch_hero_stats.py
  python3 fetch_hero_stats.py pvp_rta_ss20 champion
  python3 fetch_hero_stats.py pvp_rta_ss21 master

Defaults:
  season_code = pvp_rta_ss20  (2026 Summer)
  grade_code  = champion

Available season codes:
  pvp_rta_ss21 - 2026 Fall (current, may have limited data)
  pvp_rta_ss20 - 2026 Summer
  pvp_rta_ss19 - 2026 Spring
  pvp_rta_ss18 - 2025 Fall
  pvp_rta_ss17 - 2025 Summer
  ...older seasons available back to ss1

Available grade codes:
  all, bronze, silver, gold, master, champion, legend

Output:
  hero_stats_sorted.txt - Sorted hero list with pick rate, win rate, and ban rate.

Data source: https://epic7.onstove.com/en/gg/herorecord
API endpoint: https://e7api.onstove.com/gameApi/getPopularHero
