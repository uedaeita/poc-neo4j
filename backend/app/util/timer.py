from contextlib import contextmanager
from timeit import default_timer


@contextmanager
def elapsed_timer():
    start = default_timer()

    def elapser() -> float:
        return round_diff(default_timer(), start)

    yield lambda: elapser()
    end = default_timer()

    def elapser() -> float:  # noqa: F811
        return round_diff(end, start)


def round_diff(end_time: float, start_time: float) -> float:
    return round(end_time - start_time, 4)
