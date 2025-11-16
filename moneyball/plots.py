from math import pi
from typing import List

import matplotlib.pyplot as plt
import pandas as pd


def radar_rank_plot(
    metric_names: List[str],
    metric_ranks: List[int],
    title: str,
    radar_details: str,
    color,
    ax: plt.Axes | None = None,
):
    """Render a radar plot of ranking statistics on the provided axes."""

    metric_names = list(metric_names)
    metric_ranks = list(metric_ranks)

    if len(metric_names) == len(metric_ranks):
        num_metric = len(metric_names)
    elif len(metric_names) < 3 or len(metric_ranks) < 3:
        raise ValueError("At least 3 metrics are required for radar plots")
    else:
        raise ValueError("The number of ranks and metric names must be equal")

    if ax is None:
        fig = plt.figure(figsize=(6, 3))
        ax = fig.add_subplot(111, polar=True)
    else:
        fig = ax.figure
        ax.clear()
        if getattr(ax, "name", "") != "polar":
            raise TypeError("Provided axis must be a polar axis for radar plots")

    # Add end point to metric ranks
    extended_ranks = metric_ranks + [metric_ranks[0]]

    # Add angles
    angles = [n / float(num_metric) * 2 * pi for n in range(num_metric)]
    angles += angles[:1]

    # Spider plot setup
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Label setup
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metric_names, color="grey", size=6)
    ax.set_rlabel_position(0)
    ax.set_yticks([0, 10, 20])
    ax.set_yticklabels(["30", "20", "10"], color="grey", size=7)
    ax.set_ylim(0, 30)

    # Plot/fill
    reverse_ranks = [31 - rank for rank in extended_ranks]
    ax.plot(angles, reverse_ranks, color=color, linewidth=2, linestyle="solid")
    ax.fill(angles, reverse_ranks, color=color, alpha=0.45)

    # Plot title
    ax.set_title(title, size=9, color=color, y=1.1)

    # Add legend for ranking logic
    fig.text(
        0.1455,
        0.04,
        radar_details,
        fontsize=5.5,
        transform=fig.transFigure,
        ha="left",
        va="top",
    )

    return ax


def bar_rank_plot(
    metric: str,
    team: str,
    data: pd.DataFrame,
    rank_by_top: bool,
    title: str,
    color: tuple,
    ax: plt.Axes | None = None,
):
    """Display a sorted bar ranking for a given metric on the provided axes."""

    if metric not in data.columns:
        raise ValueError(f"Choose an available metric: {data.columns}")
    if team not in list(data.index):
        raise ValueError(f"Choose an available team: {list(data.index)}")

    if ax is None:
        fig, ax = plt.subplots()
    else:
        ax.clear()

    # Extract data and sort appropriately
    sorted_data = data[[metric]].sort_values(by=metric, ascending=rank_by_top).copy()
    team_list = list(sorted_data.index)

    if rank_by_top:
        sorted_data["rank"] = range(len(sorted_data), 0, -1)
    else:
        sorted_data["rank"] = range(1, len(sorted_data) + 1)

    # Index of team
    tm_index = team_list.index(team)

    # Bar colors
    bar_colors = [(*color, 0.3)] * len(sorted_data)
    bar_colors[tm_index] = (*color, 1.0)

    # Labels and bars
    x_positions = range(len(sorted_data))
    ax.bar(
        x_positions,
        sorted_data[metric].values,
        color=bar_colors,
    )

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(team_list, rotation=90, color="lightgrey", size=5)
    ax.get_xticklabels()[tm_index].set_color("#202020")
    ax.set_yticks([])
    ax.set_ylabel(
        f"Overall Metric: {metric}",
        color="grey",
        size=7,
    )

    ax.set_title(title, size=9, color=color, y=1.1)

    return ax
