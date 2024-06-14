"""This module defines decorators.
"""
import logging
import time

from utilities import dictutils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def timing(screen=False, verbose=False):
    """For a decorated method, write two log statements recording (a) when the method was called
    and optionally its input arguments (if verbose==True), and (b) when the method finished and
    the total duration in seconds. If optional parameter "screen" is True, output is directed to
    stdout instead of the log.

    :param screen: if True, direct output to stdout and not to the log; defaults to False
    :param verbose: if True, record input args and kwargs;; defaults to False
    :return: the result of the decorated method
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            func_class = func.__qualname__
            func_module = func.__module__
            func_name = func.__name__

            if func_class:
                logged_name = f"Class method {func_module}.{func_class}.{func_name}"
            else:
                logged_name = f"Method {func_module}.{func_name}"

            started_at = f"started at {time.strftime('%H:%M:%S')}."

            if verbose:
                started_at += (
                    f"\n\t\t{func_name} input arguments:"
                    f"\n\t\t{dictutils.get_string(locals())}."
                )

            # Here we call the decorated method.
            # --------------------------------------------------------
            #
            clock_start = time.time()
            result = func(*args, **kwargs)
            clock_end = time.time()
            #
            # --------------------------------------------------------

            finished_at = f"finished at {time.strftime('%H:%M:%S')}"
            with_duration = f"with duration {(clock_end - clock_start):.3f} seconds"

            msg = f"Timing log for {logged_name}:"
            msg += f"\n\t{logged_name} {started_at}"
            msg += f"\n\t{logged_name} {finished_at} {with_duration}."

            if screen:
                print(msg)
            else:
                logger.info(msg)

            return result

        return wrapper

    return decorator
