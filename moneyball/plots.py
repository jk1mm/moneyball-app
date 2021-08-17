from math import pi
from typing import List

import matplotlib.pyplot as plt
import pandas as pd

TEAM_COLUMN = "Tm"


def radar_rank_plot(
    metric_names: List[str], metric_ranks: List[int], title: str, color
):
    """
    Radar plot to show ranking statistics
    """

    if len(metric_names) == len(metric_ranks):
        num_metric = len(metric_names)
    elif len(metric_names) < 3 or len(metric_ranks) < 3:
        raise ValueError("At least 3 metrics are required for radar plots")
    else:
        raise ValueError("The number of ranks and metric names must be equal")

    # Add end point to metric ranks
    metric_ranks += [metric_ranks[0]]

    # Add angles
    angles = [n / float(num_metric) * 2 * pi for n in range(num_metric)]
    angles += angles[:1]

    # Spider plot setup
    ax = plt.subplot(1, 2, 1, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Label setup
    plt.xticks(angles[:-1], metric_names, color="grey", size=6)
    ax.set_rlabel_position(0)
    plt.yticks([0, 10, 20], ["30", "20", "10"], color="grey", size=7)
    plt.ylim(0, 30)

    # Plot/fill
    reverse_ranks = [31 - rank for rank in metric_ranks]
    ax.plot(angles, reverse_ranks, color=color, linewidth=2, linestyle="solid")
    ax.fill(angles, reverse_ranks, color=color, alpha=0.45)

    # Plot title
    plt.title(title, size=9, color=color, y=1.1)


def bar_rank_plot(
    metric: str, team: str, data: pd.DataFrame, rank_by_top: bool, title: str, color
):
    """
    Display sorted bar ranking for a given metric
    """

    if metric not in data.columns:
        raise ValueError(f"Choose an available metric: {data.columns}")
    if team not in list(data[TEAM_COLUMN]):
        raise ValueError(f"Choose an available team: {list(data[TEAM_COLUMN])}")

    # Extract data and sort appropriately
    data = data[[TEAM_COLUMN, metric]].sort_values(by=[metric], ascending=rank_by_top)
    if rank_by_top:
        data["rank"] = range(30, 0, -1)
    else:
        data["rank"] = range(1, 31)
    team_list = list(data[TEAM_COLUMN])

    # Plot setup
    plt.subplot(1, 2, 2, polar=False)

    # Labels
    plt.bar(TEAM_COLUMN, metric, data=data, color=color)
    plt.xticks(range(len(team_list)), team_list, rotation=90, color="grey", size=6)
    plt.yticks([], [], color="grey", size=7)
    plt.ylabel(
        f"Overall Metric: {metric}",
        color="grey",
        size=7,
    )

    # Plot title
    plt.title(title, size=9, color=color, y=1.1)
