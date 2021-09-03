from datetime import datetime


# Webscrape URL's
MLB_BASE_URL = "https://www.baseball-reference.com/leagues/majors/"
METRIC_PATH = {
    "Batting": "-standard-batting.shtml",
    "Starting Pitching": "-starter-pitching.shtml",
    "Relief Pitching": "-reliever-pitching.shtml",
}

# MLB available seasons for data scraping
MIN_YEAR = 2000
MAX_YEAR = (
    datetime.today().year if datetime.today().month >= 4 else datetime.today().year - 1
)  # Current year only if regular season is ongoing/finished


# Team statistics descriptions
BATTING_DESC = """
Batting: BA
Power: HR
On Base: OBP
Base Stealing: SB, CS
Efficiency: LOB, R
"""

SP_DESC = """
Quality Start Rank: QS%
Winning Rank: Wgs, Wlst, Lsv
Efficiency Rank: IP/GS
Stamina Rank: 80-99, 100-119, ≥120
"""

RP_DESC = """
Save Rank: SV
Holds Rank: Hold
Clean Closes Rank: SV%
Game Pressure Rank: aLI
Win Pct Rank: Wgr, Lgr
"""
