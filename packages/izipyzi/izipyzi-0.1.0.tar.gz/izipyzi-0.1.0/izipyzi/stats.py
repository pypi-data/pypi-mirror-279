import numpy as np
from typing import List


def calculate_statistics(numbers: List[float]) -> dict[str, float]:
    """
    Calculate the mean and 95% confidence interval of a list of numbers.

    Args:
        times: list of float

    Returns:

    """
    mean = np.mean(numbers)
    confidence_interval = np.percentile(numbers, [2.5, 97.5])
    return {"mean": mean, "confidence_interval": confidence_interval}
