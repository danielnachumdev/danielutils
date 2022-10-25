from danielutils import *
from danielutils.Exceptions import *
# from typing import *
# print(isoftype(Callable[[], bool], type(Callable)))
# v = Callable[[int], bool]
# print(str(v.__dir__).split("of")[1].strip(" >"))
# v = type(Callable[[], bool])
# print((v.__parameters__))
# print(dir(v))

# def foo(a: int) -> int:
#     pass

# from builtins import function
d: tdict[tlist[int], int] = tdict(int, tlist[int])


def inner(key, value):
    d[key] = value
    return True


TestFactory(inner, verbose=True).add_tests([
    Test((1, [1]), outputs=True),
    Test((1.0, [1]), exception=TypeError),
    Test(("5", [1]), exception=TypeError),
    Test((1, [1]), outputs=True),
    Test((1, [1.0]), exception=TypeError),
])()
