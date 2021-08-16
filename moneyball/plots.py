from math import pi
from typing import List

import matplotlib.pyplot as plt


def radar_plot(metric_names: List[str], metric_ranks: List[int]):

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

    # Plot setup
    ax = plt.subplot(111, polar=True)
    # Draw one axe per variable + add labels
    plt.xticks(angles[:-1], metric_names, color="grey", size=8)

    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([10, 20, 30], ["10", "20", "30"], color="grey", size=7)
    plt.ylim(0, 40)

    # Plot data
    ax.plot(angles, metric_ranks, linewidth=1, linestyle="solid")

    # Fill area
    ax.fill(angles, metric_ranks, "b", alpha=0.5)

    # Show the graph
    return plt
