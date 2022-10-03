import traceback
from danielutils import atomic, write_to_file, sleep, atomic_print
from inspect import getmembers
import threading
from typing import Callable
THREAD_COUNT = 1
ITERATIONS = 1


def test(func: Callable):
    import inspect
    print(*inspect.stack(), sep="\n")
    # traceback.print_stack()

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@test
def thread_main(i, j):
    # atomic_print(i, j)
    print(i, j)


def main():
    for i in range(ITERATIONS):
        threads = [threading.Thread(target=thread_main, args=[i, j])
                   for j in range(THREAD_COUNT)]
        for t in threads:
            t.start()


if __name__ == '__main__':
    thread_main(1, 2)
    # main()
