from danielutils.Exceptions import ValidationTypeError
from danielutils import TestFactory, Test, validate
from typing import Sequence, Union, Any


@validate(int, int)
def add(x, y):
    return x+y


tester = TestFactory(add)
tester.add_tests([
    Test((1, 2), 3),
    Test((3, 2), 3,),
    Test((1, 2), 3),
    Test((1, 2.0), 3),
    Test((1, 2.5), 3, ValidationTypeError),
])
tester()
