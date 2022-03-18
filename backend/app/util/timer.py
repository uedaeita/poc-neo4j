from contextlib import contextmanager
from timeit import default_timer


@contextmanager
def elapsed_timer():
    start = default_timer()

    def elapser() -> float:
        return round(default_timer() - start, 4)

    yield lambda: elapser()
    end = default_timer()

    def elapser() -> float:  # noqa: F811
        return round(end - start, 4)
