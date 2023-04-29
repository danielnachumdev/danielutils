from ...danielutils.MetaClasses.AtomicClassMeta import AtomicClassMeta
from ...danielutils import threadify
import time


class A():
    @staticmethod
    def my_print(*args):
        print(*args)


class B(A, metaclass=AtomicClassMeta):
    pass


@threadify
def thread_main1(thread_id: int):
    for _ in range(5):
        A.my_print(thread_id)


@threadify
def thread_main2(thread_id: int):
    for _ in range(5):
        B.my_print(thread_id)


def main():
    for i in range(2):
        thread_main1(i)

    time.sleep(1)
    for i in range(2):
        thread_main2(i)


if __name__ == "__main__":
    main()
# TODO make this into a test
