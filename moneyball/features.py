from typing import List, Union

Number = Union[int, float]


def metric_rank(
    value: Number, all_values: List[Number], max_as_top: bool = True
) -> int:
    """
    Gets the ranking of value across all_values. In the case there's a tie, the preferred (better) rank will be given.

    Parameter
    ---------
    value: Number
        The value to evaluate rank.

    all_values: List[Number]
        The set of values to compare against input value.

    max_as_top: bool, default True
        Option to specify if max/min number is considered as the top rank.

    Return
    ------
    rank: int
        The rank of the value, ranging from (1-len(all_values))

    """
    # Sorting appropriately
    all_values = sorted(all_values, reverse=max_as_top)

    try:
        rank = all_values.index(value) + 1
    except ValueError:
        raise ValueError(f"Specified value {value} is not in the all_values list.")

    return rank
