from typing import Union, List, Optional


import numpy as np
import pandas as pd
import streamlit as sl


from moneyball.constants import (
    MIN_YEAR,
    MAX_YEAR,
    MLB_BASE_URL,
    METRIC_PATH,
    BATTING_DESC,
    SP_DESC,
    RP_DESC,
    DEF_DESC,
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
def mlb_scrape(
    metric_type: str, year: Union[str, int], pct_cols: Optional[List[str]] = None
):
    """
    Data scraping MLB data.

    Available data types
    --------------------
    - Team view

    Parameters
    ----------
    year: Union[str, int]
        The year of the season to scrape.

    metric_type: str
        The type of metric statistics to scrape.
        Available choices: ["Batting", "Starting Pitching", "Relief Pitching"]

    pct_cols: Optional[List[str]], default None
        Columns that have '%' embedded to the numeric values.

    Returns
    -------
    stats_df, stats_avg: pd.DataFrame, dict
        Team statistics for specified metric type, and average stats.
    """
    # Check metric type validity
    if metric_type not in METRIC_PATH:
        raise ValueError(f"Please choose from {list(METRIC_PATH.keys())}")

    stats_df = pd.read_html((MLB_BASE_URL + str(year) + METRIC_PATH[metric_type]))[0]

    # Average statistics
    stats_avg = stats_df[stats_df["Tm"] == "League Average"]

    # Delete unnecessary rows
    stats_df = stats_df[~stats_df["Tm"].isin(["Tm", "League Average"])]
    stats_df = stats_df.head(len(stats_df) - 1)  # Remove total
    stats_df = stats_df.fillna(0)

    # Convert all columns except Tm as numeric
    cols_num = stats_df.columns.drop("Tm")
    if pct_cols:
        for pct in pct_cols:
            stats_df[pct] = list(map(lambda x: x[:-1], stats_df[pct].values))
    stats_df[cols_num] = stats_df[cols_num].apply(pd.to_numeric, errors="coerce")
    stats_avg = (
        stats_avg[cols_num].apply(pd.to_numeric, errors="coerce").to_dict("records")
    )

    # Keep team as index
    stats_df = stats_df.set_index("Tm")

    return stats_df, stats_avg


# All application views
def display():

    # Sidebar configurations
    sl.sidebar.write("# Major League Baseball")
    season = sl.sidebar.selectbox(
        "Season:", list(reversed(range(MIN_YEAR, MAX_YEAR + 1)))
    )
    metric_type = sl.sidebar.selectbox("Metric:", METRIC_PATH.keys())

    if metric_type == "Starting Pitching":
        all_team_table, stats_avg = mlb_scrape(
            metric_type=metric_type, year=season, pct_cols=["QS%"]
        )
    elif metric_type == "Relief Pitching":
        all_team_table, stats_avg = mlb_scrape(
            metric_type=metric_type, year=season, pct_cols=["SV%", "IS%"]
        )
    else:
        all_team_table, stats_avg = mlb_scrape(metric_type=metric_type, year=season)

    # App page title/source
    sl.title(f"MLB Team {metric_type} Analysis for {season} Season")
    sl.markdown(
        """**Data Source:** [Baseball-reference.com](https://www.baseball-reference.com/)"""
    )

    # Show dataframe
    sl.dataframe(all_team_table)

    team_select = sl.selectbox("Select Team:", [""] + list(all_team_table.index))

    # Proceed once team is selected
    if not team_select:
        sl.warning("No option is selected")

    else:
        team_stats = all_team_table[all_team_table.index == team_select].to_dict(
            "records"
        )[0]
        all_team_stats = all_team_table.to_dict("list")

        # Setup figure
        

        if metric_type == "Batting":
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
                    "Hitting",
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

            # Radar Plot - Breakdown rankings
            radar_rank_plot(
                metric_names=rankings["metrics"],
                metric_ranks=rankings["metric_rankings"],
                title="Team Ranking per Offense Category",
                color=(0.5019607843137255, 0.6941176470588235, 0.8274509803921568, 1.0),
                radar_details=BATTING_DESC,
            )

            # Bar Plot - Overall ranking
            bar_rank_plot(
                metric="R/G",
                team=team_select,
                data=all_team_table,
                rank_by_top=True,
                title=f"Overall Ranking: {overall_rank}",
                color=(0.5529411764705883, 0.8274509803921568, 0.7803921568627451),
            )

        if metric_type == "Starting Pitching":
            # Rank Dependency
            # ---------------
            # Overall Rank: GmScA
            # Quality Start Rank: QS%
            # Winning Rank: Wgs + Wlst - Lsv
            # Efficiency Rank: IP/GS
            # Stamina Rank: 1*(80-99) + 1.5*(100-119) + 2*(≥120)

            overall_rank = metric_rank(team_stats["GmScA"], all_team_stats["GmScA"])
            qs_rank = metric_rank(team_stats["QS%"], all_team_stats["QS%"])
            winning_rank = metric_rank(
                team_stats["Wgs"] + team_stats["Wlst"] - team_stats["Lsv"],
                np.array(all_team_stats["Wgs"])
                + np.array(all_team_stats["Wlst"])
                - np.array(all_team_stats["Lsv"]),
            )
            stamina_rank = metric_rank(
                team_stats["80-99"]
                + 1.5 * team_stats["100-119"]
                + 2 * team_stats["≥120"],
                np.array(all_team_stats["80-99"])
                + 1.5 * np.array(all_team_stats["100-119"])
                + 2 * np.array(all_team_stats["≥120"]),
            )
            efficiency_rank = metric_rank(
                team_stats["IP/GS"],
                all_team_stats["IP/GS"],
            )

            rankings = {
                "overall": overall_rank,
                "metrics": [
                    "Winning",
                    "Efficiency",
                    "Quality Start",
                    "Stamina",
                ],
                "metric_rankings": [
                    winning_rank,
                    efficiency_rank,
                    qs_rank,
                    stamina_rank,
                ],
            }

            # Radar Plot - Breakdown rankings
            radar_rank_plot(
                metric_names=rankings["metrics"],
                metric_ranks=rankings["metric_rankings"],
                title="Team Ranking per Starting Pitching Category",
                color=(0.5019607843137255, 0.6941176470588235, 0.8274509803921568, 1.0),
                radar_details=SP_DESC,
            )

            # Bar Plot - Overall ranking
            bar_rank_plot(
                metric="GmScA",
                team=team_select,
                data=all_team_table,
                rank_by_top=True,
                title=f"Overall Ranking: {overall_rank}",
                color=(0.5529411764705883, 0.8274509803921568, 0.7803921568627451),
            )

        if metric_type == "Relief Pitching":
            # Rank Dependency
            # ---------------
            # Overall Rank: IS%
            # Saves: SV
            # Holds: Hold
            # Save pct: SV%
            # Win pct: Wgr, Lgr
            # Leverage pressure: aLI

            overall_rank = metric_rank(
                team_stats["IS%"], all_team_stats["IS%"], max_as_top=False
            )
            save_count_rank = metric_rank(team_stats["SV"], all_team_stats["SV"])
            hold_count_rank = metric_rank(team_stats["Hold"], all_team_stats["Hold"])
            save_pct_rank = metric_rank(team_stats["SV%"], all_team_stats["SV%"])
            win_pct_rank = metric_rank(
                team_stats["Wgr"] / (team_stats["Wgr"] + team_stats["Lgr"]),
                np.array(all_team_stats["Wgr"])
                / (np.array(all_team_stats["Wgr"]) + np.array(all_team_stats["Lgr"])),
            )
            lvg_pressure_rank = metric_rank(team_stats["aLI"], all_team_stats["aLI"])

            rankings = {
                "overall": overall_rank,
                "metrics": [
                    "Saves",
                    "Holds",
                    "Clean Closes",
                    "Game Pressure",
                    "Win %",
                ],
                "metric_rankings": [
                    save_count_rank,
                    hold_count_rank,
                    save_pct_rank,
                    lvg_pressure_rank,
                    win_pct_rank,
                ],
            }

            # Radar Plot - Breakdown rankings
            radar_rank_plot(
                metric_names=rankings["metrics"],
                metric_ranks=rankings["metric_rankings"],
                title="Team Ranking per Relief Pitching Category",
                color=(0.5019607843137255, 0.6941176470588235, 0.8274509803921568, 1.0),
                radar_details=RP_DESC,
            )

            # Bar Plot - Overall ranking
            bar_rank_plot(
                metric="IS%",
                team=team_select,
                data=all_team_table,
                rank_by_top=False,
                title=f"Overall Ranking: {overall_rank}",
                color=(0.5529411764705883, 0.8274509803921568, 0.7803921568627451),
            )

        if metric_type == "Fielding":
            # Rank Dependency
            # ---------------
            # Overall Rank: Rtot/yr
            # Defensive Efficiency Rank: DefEff
            # Fielding Pct Rank: Fld%
            # Double Plays Rank: DP
            # Defensive Runs Saved Rank: Rdrs/yr
            # Good Plays Rank: Rgood

            overall_rank = metric_rank(team_stats["Rtot/yr"], all_team_stats["Rtot/yr"])
            def_eff_rank = metric_rank(team_stats["DefEff"], all_team_stats["DefEff"])
            fielding_rank = metric_rank(team_stats["Fld%"], all_team_stats["Fld%"])
            dp_rank = metric_rank(team_stats["DP"], all_team_stats["DP"])
            drs_rank = metric_rank(team_stats["Rdrs/yr"], all_team_stats["Rdrs/yr"])
            good_plays_rank = metric_rank(team_stats["Rgood"], all_team_stats["Rgood"])

            rankings = {
                "overall": overall_rank,
                "metrics": [
                    "Defensive Efficiency",
                    "DRS",
                    "Fld%",
                    "Good Plays",
                    "DP",
                ],
                "metric_rankings": [
                    def_eff_rank,
                    drs_rank,
                    fielding_rank,
                    good_plays_rank,
                    dp_rank,
                ],
            }

            # Radar Plot - Breakdown rankings
            radar_rank_plot(
                metric_names=rankings["metrics"],
                metric_ranks=rankings["metric_rankings"],
                title="Team Ranking per Fielding Category",
                color=(0.5019607843137255, 0.6941176470588235, 0.8274509803921568, 1.0),
                radar_details=DEF_DESC,
            )

            # Bar Plot - Overall ranking
            bar_rank_plot(
                metric="Rtot/yr",
                team=team_select,
                data=all_team_table,
                rank_by_top=True,
                title=f"Overall Ranking: {overall_rank}",
                color=(0.5529411764705883, 0.8274509803921568, 0.7803921568627451),
            )

        # Display plots
        sl.pyplot()


if __name__ == "__main__":
    display()

# TODO: Change plot theme
