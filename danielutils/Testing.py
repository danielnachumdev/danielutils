from typing import Sequence, Callable, Union, Any
from .Decorators import validate
from .Colors import ColoredText


def passed(text: str):
    pass_text = ColoredText.green("PASSED")
    print(f"{pass_text}: {text}")


def failed(text: str):
    failed_text = ColoredText.red("FAILED")
    print(f"{failed_text}: {text}")


class Test:
    def __init__(self, inputs: Union[Sequence, Any], outputs: Union[Sequence, Any], exceptions=None):
        self.inputs = inputs if isinstance(inputs, Sequence) else (inputs,)
        self.outputs = outputs if isinstance(outputs, Sequence) else (outputs,)
        self.exceptions = None
        if exceptions:
            self.exceptions = exceptions.__qualname__


class TestFactory:
    @validate(None, Callable)
    def __init__(self, func: Callable):
        self.func = func
        self.tests: list[Test] = []

    def add_test(self, test: Test):
        self.tests.append(test)

    def add_tests(self, tests: Sequence[Test]):
        self.tests.extend(tests)

    def __call__(self) -> bool:
        name = f"{self.func.__module__}.{self.func.__qualname__}"
        print(f"Testing {name}...\n")
        count: int = 0
        pass_count: int = 0
        for test in self.tests:
            count += 1
            try:
                passed_test = False
                res = self.func(* test.inputs)
                if not isinstance(res, tuple):
                    res = (res,)
                msg = f"{count}: {test.inputs} => {res}, expected {test.outputs}"
                if res == test.outputs:
                    passed_test = True
            except Exception as e:
                msg = f"{count}: {test.inputs} => {type(e).__qualname__}, expected {test.exceptions}"
                if type(e).__qualname__ == test.exceptions:
                    passed_test = True
            finally:
                if passed_test:
                    pass_count += 1
                    passed(msg)
                else:
                    failed(msg)
        print()
        print(f"PASSED {pass_count} / {count}".center(20, " ").center(40, "="))
        return pass_count == count


__all__ = [
    "Test",
    "TestFactory"
]
# def test_func(functor, inputs, outputs) -> None:
#     if not callable(functor):
#         raise TypeError("functor must return true for callable(functor)")

#     if len(inputs) != len(outputs):
#         raise ValueError("Amount of inputs and outputs is diffrent")

#     for input, output in zip(inputs, outputs):
#         res = functor(*input[0], **input[1])

# class Tester:
#     @validate(None, Callable, Sequence, Sequence)
#     def __init__(self, func, inputs, outputs):
#         self.func = func
#         self.inputs = inputs
#         self.outputs = outputs

#     def test():
#         pass
