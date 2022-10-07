import time


def measure(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    end = time.time()
    return end-start


def sleep(secs: float):
    time.sleep(secs)


__all__ = [
    "measure",
    "sleep"
]
