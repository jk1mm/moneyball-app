from datetime import datetime


# Webscrape URL's
MLB_BASE_URL = "https://www.baseball-reference.com/leagues/MLB/"
PLAYER_TYPE_PATH = {
    "Batting": "-standard-batting.shtml",
    "Starting Pitching": "-starter-pitching.shtml",
    "Relief Pitching": "-reliever-pitching.shtml",
}

# MLB available seasons for data scraping
MIN_YEAR = 2000
MAX_YEAR = (
    datetime.today().year if datetime.today().month >= 4 else datetime.today().year - 1
)  # Current year only if regular season is ongoing/finished
