from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as sl

from moneyball.constants import (
    MIN_YEAR,
    MAX_YEAR,
    MLB_BASE_URL,
    PLAYER_TYPE_PATH,
)
from moneyball.features import metric_rank
from moneyball.plots import radar_rank_plot, bar_rank_plot

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

    all_team_table, stats_avg = mlb_scrape(player_type=player_type, year=season)

    # App page title/source
    sl.title(f"MLB Team {player_type} Analysis for {season} Season")
    sl.markdown(
        """**Data Source:** [Baseball-reference.com](https://www.baseball-reference.com/)"""
    )

    # Show dataframe
    sl.dataframe(all_team_table)

    team_select = sl.selectbox("Select Team:", [""] + list(all_team_table["Tm"]))

    # Proceed once team is selected
    if not team_select:
        sl.warning("No option is selected")

    else:
        team_stats = all_team_table[all_team_table.Tm == team_select].to_dict(
            "records"
        )[0]
        all_team_stats = all_team_table.to_dict("list")

        if player_type == "Batting":
            # Rank Dependency
            # ---------------
            # Overall Rank: R/G
            # Hitting Rank: BA
            # Power Rank: HR
            # On Base Rank: OBP
            # Stealing Base Rank: Speed on base (SB and CS)
            # Efficiency Rank: Rate of non-HR runs scored out of run scoring opportunities

            overall_rank = metric_rank(
                team_stats["R/G"],
                all_team_stats["R/G"],
            )
            hit_rank = metric_rank(
                team_stats["BA"],
                all_team_stats["BA"],
            )
            power_rank = metric_rank(
                team_stats["HR"],
                all_team_stats["HR"],
            )
            ob_rank = metric_rank(
                team_stats["OBP"],
                all_team_stats["OBP"],
            )
            steal_rank = metric_rank(
                team_stats["SB"] - team_stats["CS"],
                np.array(all_team_stats["SB"]) - np.array(all_team_stats["CS"]),
            )
            temp_arr = np.array(all_team_stats["R"]) - np.array(all_team_stats["HR"])
            efficiency_rank = metric_rank(
                (team_stats["R"] - team_stats["HR"])
                / (team_stats["R"] - team_stats["HR"] + team_stats["LOB"]),
                temp_arr / (temp_arr + np.array(all_team_stats["LOB"])),
            )

            rankings = {
                "overall": overall_rank,
                "metrics": [
                    "Batting",
                    "On Base",
                    "Base Stealing",
                    "Efficiency",
                    "Power",
                ],
                "metric_rankings": [
                    hit_rank,
                    ob_rank,
                    steal_rank,
                    efficiency_rank,
                    power_rank,
                ],
            }

            # Plots - setup
            plt.figure(figsize=(9, 3))

            # Radar Plot - Breakdown rankings
            radar_rank_plot(
                metric_names=rankings["metrics"],
                metric_ranks=rankings["metric_rankings"],
                title="Team Ranking per Offense Category",
                color=(0.5019607843137255, 0.6941176470588235, 0.8274509803921568, 1.0),
            )

            # Bar Plot - Overall ranking
            bar_rank_plot(
                metric="R/G",
                team=team_select,
                data=all_team_table,
                rank_by_top=True,
                title=f"Overall Ranking: {overall_rank}",
                color=(0.5529411764705883, 0.8274509803921568, 0.7803921568627451, 1.0),
            )

            sl.pyplot()

        # TODO: Add legend of what variables for each metric are used


if __name__ == "__main__":
    display()
