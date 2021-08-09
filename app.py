from typing import Union

import pandas as pd
import streamlit as sl

from moneyball.constants import (
    MIN_YEAR,
    MAX_YEAR,
    MLB_BASE_URL,
    PLAYER_TYPE_PATH,
)

sl.set_page_config(
    page_title="Moneyball",
    layout="wide",
    initial_sidebar_state="auto",
)


# MLB data scraping team view
@sl.cache
def mlb_scrape(player_type: str, year: Union[str, int]):
    """
    Data scraping MLB data.

    Available data types
    --------------------
    - Team view

    Parameters
    ----------
    year: Union[str, int]
        The year of the season to scrape.

    player_type: str
        The type of player statistics to scrape.
        Available choices: ["Batting", "Starting Pitching", "Relief Pitching"]

    Returns
    -------
    stats_df, stats_avg: pd.DataFrame, dict
        Team statistics for specified player type, and average stats.
    """
    # Check player type validity
    if player_type not in PLAYER_TYPE_PATH:
        raise ValueError(f"Please choose from {list(PLAYER_TYPE_PATH.keys())}")

    stats_df = pd.read_html((MLB_BASE_URL + str(year) + PLAYER_TYPE_PATH[player_type]))[
        0
    ]

    # Average statistics
    stats_avg = stats_df[stats_df["Tm"] == "League Average"]

    # Delete unnecessary rows
    stats_df = stats_df[~stats_df["Tm"].isin(["Tm", "League Average"])]
    stats_df = stats_df.head(len(stats_df) - 1)  # Remove total
    stats_df = stats_df.fillna(0)

    # Convert all columns except Tm as numeric
    cols_num = stats_df.columns.drop("Tm")
    stats_df[cols_num] = stats_df[cols_num].apply(pd.to_numeric, errors="coerce")
    stats_avg = (
        stats_avg[cols_num].apply(pd.to_numeric, errors="coerce").to_dict("records")
    )

    return stats_df, stats_avg


# All application views
def display():

    # Sidebar configurations
    sl.sidebar.write("# Selections")
    season = sl.sidebar.selectbox(
        "Season:", list(reversed(range(MIN_YEAR, MAX_YEAR + 1)))
    )
    player_type = sl.sidebar.selectbox("Player Type:", PLAYER_TYPE_PATH.keys())

    team_stats, stats_avg = mlb_scrape(player_type=player_type, year=season)

    # App page title/source
    sl.title(f"MLB Team {player_type} Analysis for {season} Season")
    sl.markdown(
        """**Data Source:** [Baseball-reference.com](https://www.baseball-reference.com/)"""
    )

    # Show dataframe
    sl.dataframe(team_stats)

    team_select = sl.selectbox("Select Team:", [""] + list(team_stats["Tm"]))
    # stat_select = sl.selectbox("Select Stat:", [""] + team_stats.columns)

    # Proceed once team is selected
    if not team_select:
        sl.warning("No option is selected")
    else:
        None

    # TODO: Rankings per team
    # TODO: Proper design panelling


if __name__ == "__main__":
    display()
