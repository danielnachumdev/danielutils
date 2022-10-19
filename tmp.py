from danielutils import *
from danielutils.Classes.TypedBuiltins import tlist
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
d = tdict(int, int)
d[1] = 1
print(d)
