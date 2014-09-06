"""Module for decorators."""

import time


def print_time(func):
    """Print function call time."""

    def wrapper(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("{}: {} s".format(func.__name__, end - start))

        return result

    return wrapper
