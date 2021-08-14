import matplotlib.pyplot as plt
from typing import List


def radar_plot(metric_names: List[str], metric_ranks: List[int]):

    if len(metric_names) == len(metric_ranks):
        num_metric = len(metric_names)
    elif len(metric_names) < 3 or len(metric_ranks) < 3:
        raise ValueError("At least 3 metrics are required for radar plots")
    else:
        raise ValueError("The number of ranks and metric names must be equal")

    # Add end point to metric ranks
    metric_ranks += [metric_ranks[0]]
