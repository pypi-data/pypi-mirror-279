import timeit
from typing import Callable, List


def time_function_by_tries(func: Callable, *args, tries: int, **kwargs) -> List[float]:
    """
    Time the execution of a function by the number of tries.

    Args:
        func: function
        *args: positional arguments
        tries: int, number of tries
        **kwargs: keyword arguments

    Returns:
        list of float, the times of each function execution
    """
    return timeit.repeat(lambda: func(*args, **kwargs), number=1, repeat=tries)


def time_function_by_duration(
    func: Callable, *args, duration: float, **kwargs
) -> List[float]:
    """
    Time the execution of a function by duration.

    Args:
        func: function
        *args: positional arguments
        duration: float, duration in seconds
        **kwargs: keyword arguments

    Returns:
        list of float, the times of each function execution
    """
    times = []
    start_time = timeit.default_timer()
    while timeit.default_timer() - start_time < duration:
        times.append(timeit.timeit(lambda: func(*args, **kwargs), number=1))
    return times
