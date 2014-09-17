"""Module for decorators."""

import time
import os


def print_time(func):
    """Print function call time."""

    def wrapper(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print("{}: {} s".format(func.__name__, end - start))

        return result

    return wrapper


def print_pid(func):
    """Print process ID."""

    def wrapper(*args, **kwargs):

        print("{}, PID: {} ({})".format(
            func.__name__, os.getpid(), os.getppid()))

        return func(*args, **kwargs)

    return wrapper
