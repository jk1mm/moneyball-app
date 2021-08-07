from datetime import datetime

# MLB available seasons for data scraping
MIN_YEAR = 2000
MAX_YEAR = (
    datetime.today().year if datetime.today().month >= 4 else datetime.today().year - 1
)  # Current year only if regular season is ongoing/finished
