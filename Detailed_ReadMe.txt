Epic Seven Hero Stats Fetcher
=============================

Fetches RTA hero statistics from the Epic Seven API (epic7.onstove.com)
and outputs them sorted by usage (pick) rate in descending order.

Requirements:
  - Python 3.6+
  - curl (for manual API calls)
  - No external Python packages required (uses only stdlib)

Usage:
  python3 fetch_hero_stats.py [season_code] [grade_code]

Examples:
  python3 fetch_hero_stats.py
  python3 fetch_hero_stats.py pvp_rta_ss20 champion
  python3 fetch_hero_stats.py pvp_rta_ss21 master

Defaults:
  season_code = pvp_rta_ss20  (2026 Summer)
  grade_code  = champion


=========================================================
API Reference (Curl Commands)
=========================================================

Base API URL: https://e7api.onstove.com

All endpoints use HTTP POST. Parameters are passed as URL query
strings (not request body). The request body can be empty.

Required headers for all requests:
  Content-Type: application/json;charset=UTF-8
  Caller-Id:    WEB_STOVE_EPIC7
  Caller-Detail: WEB_STOVE_EPIC7

---------------------------------------------------------
1. Get Season List
---------------------------------------------------------
Returns all available RTA seasons.

  curl -s \
    'https://e7api.onstove.com/gameApi/getSeasonList' \
    -X POST \
    -H 'Content-Type: application/json;charset=UTF-8' \
    -H 'Caller-Id: WEB_STOVE_EPIC7' \
    -H 'Caller-Detail: WEB_STOVE_EPIC7'

Response fields per season:
  season_code  - Unique season identifier (e.g. "pvp_rta_ss20")
  name         - Season display name (e.g. "2026 Summer")
  startDate    - Season start date
  endDate      - Season end date
  is_now_season - 1 if currently active, 0 if ended

---------------------------------------------------------
2. Get Hero Popularity / Win Rate (Main Endpoint)
---------------------------------------------------------
Returns hero statistics for a given season and rank tier.
This is the primary endpoint used by the script.

  curl -s \
    'https://e7api.onstove.com/gameApi/getPopularHero?\
season_code=pvp_rta_ss20&\
grade_code=champion&\
current_page=1&\
lang=en' \
    -X POST \
    -H 'Content-Type: application/json;charset=UTF-8' \
    -H 'Caller-Id: WEB_STOVE_EPIC7' \
    -H 'Caller-Detail: WEB_STOVE_EPIC7'

Query parameters:
  season_code   - RTA season ID (e.g. "pvp_rta_ss20")
  grade_code    - Rank tier filter (e.g. "champion", "master", "legend")
  current_page  - Page number for pagination (starts at 1)
  lang          - Language code ("en", "ko", "ja", "zh-TW")

Response fields per hero:
  hero_code     - Unique hero ID (e.g. "c2124")
  hero_names    - Map of hero_code to display name
  pick_rate     - Usage/pick rate as a percentage (e.g. 36.7)
  win_rate      - Win rate as a percentage (e.g. 46.91)
  ban_rate      - Ban rate as a percentage (e.g. 14.3)
  use_rank      - Rank by pick rate (1 = most picked)
  seasonCode    - Season the data belongs to
  seasonTierCode - Tier the data belongs to
  regDate       - When the data was last updated
  with_heroes   - List of hero_codes that synergize well
  hard_heroes   - List of hero_codes that counter this hero
  equip         - Recommended equipment sets

Each page returns up to 100 heroes. Fetch subsequent pages
by incrementing current_page until the result_body array is empty.

Full example with jq to extract hero name + win rate:

  curl -s \
    'https://e7api.onstove.com/gameApi/getPopularHero?\
season_code=pvp_rta_ss20&\
grade_code=champion&\
current_page=1&\
lang=en' \
    -X POST \
    -H 'Content-Type: application/json;charset=UTF-8' \
    -H 'Caller-Id: WEB_STOVE_EPIC7' \
    -H 'Caller-Detail: WEB_STOVE_EPIC7' \
  | python3 -c "
import json,sys
data = json.load(sys.stdin)
for h in data['value']['result_body']:
    name = h['hero_names'][h['hero_code']]
    print(f\"{name}: {h['win_rate']}% win, {h['pick_rate']}% pick\")
"

---------------------------------------------------------
3. Get Individual Hero Analysis
---------------------------------------------------------
Returns detailed stats for a single hero across seasons.

  curl -s \
    'https://e7api.onstove.com/gameApi/getHeroAnalysis?\
hero_code=c2124&\
season_code=pvp_rta_ss20&\
grade_code=champion&\
lang=en' \
    -X POST \
    -H 'Content-Type: application/json;charset=UTF-8' \
    -H 'Caller-Id: WEB_STOVE_EPIC7' \
    -H 'Caller-Detail: WEB_STOVE_EPIC7'

Query parameters:
  hero_code    - The hero's unique ID (e.g. "c2124" for Boss Arunka)
  season_code  - RTA season ID
  grade_code   - Rank tier
  lang         - Language code

Response includes:
  win_rate      - Array of win rates per season
  pick_rate     - Array of pick rates per season
  ban_rate      - Array of ban rates per season

---------------------------------------------------------
4. Get Hero Master/Expert Rankings
---------------------------------------------------------
Returns the top-ranked players for a specific hero.

  curl -s \
    'https://e7api.onstove.com/gameApi/getHeroMasterAnalysis?\
hero_code=c2124&\
season_code=pvp_rta_ss20&\
lang=en' \
    -X POST \
    -H 'Content-Type: application/json;charset=UTF-8' \
    -H 'Caller-Id: WEB_STOVE_EPIC7' \
    -H 'Caller-Detail: WEB_STOVE_EPIC7'

Query parameters:
  hero_code    - The hero's unique ID
  season_code  - RTA season ID
  lang         - Language code


=========================================================
Notes
=========================================================

- The website is a Nuxt.js SPA. The data is NOT in the HTML;
  it is fetched client-side via the API documented above.
- Parameters must be passed as query strings (?key=value),
  not as POST body JSON. Sending body JSON returns empty results.
- The current season (pvp_rta_ss21, 2026 Fall) may have
  limited or no data if it just started.


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
