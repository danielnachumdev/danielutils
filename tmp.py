from danielutils import atomic, write_to_file, sleep
from inspect import getmembers
import typing
import threading
import time
count = 0
# order = []

# lock = threading.Lock()


@atomic
def check_this():
    """
    acquires lock at the beginning
    and releases at the end of this block
    """
    # with lock:

    a, b = 1, 0
    print("locked")
    try:
        print(a // b)
    except Exception as _:
        print(_)
    print("lock is released")


[threading.Thread(target=check_this).start() for _ in range(2)]


@atomic
def critical_info(i, j):
    print
    global count
    print(count, end="", flush=True)
    count += 1


def main():
    global count
    res = []
    for i in range(1):
        threads = [threading.Thread(target=critical_info, args=[i, j])
                   for j in range(10)]
        for t in threads:
            t.start()
        # sleep(0.1)
        count = 0
        print()


# main()
