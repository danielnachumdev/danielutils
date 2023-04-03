from typing import Sequence, Union, Any
from collections.abc import Callable
from .Decorators import validate_explicit
from .Colors import ColoredText
from .Classes import DisablePytestDiscovery
from .Functions import isoneof
from .IO import read_file, write_to_file, file_exists
from pathlib import Path
import re


class Test(DisablePytestDiscovery):
    @staticmethod
    def passed(text: str):
        pass_text = ColoredText.green("PASSED")
        print(f"{pass_text}: {text}")

    @staticmethod
    def failed(text: str):
        failed_text = ColoredText.red("FAILED")
        print(f"{failed_text}: {text}")

    def __init__(self, inputs: Union[Sequence, Any], outputs: Union[Sequence, Any] = None, exception=None):
        if outputs is None and exception is None:
            raise ValueError(
                "Cannot create a test where which doesn't return anything and not raises any exception")
        if outputs and exception:
            raise ValueError("cant check both return value and exception")

        self.inputs = inputs if isinstance(inputs, Sequence) else (inputs,)
        self.outputs = None
        if outputs is not None:
            self.outputs = outputs if isoneof(
                outputs, [list, tuple]) else (outputs,)
        self.exceptions = None
        if exception is not None:
            self.exceptions = exception.__qualname__

    def acquire_result(self, func: Callable) -> bool:
        return func(*self.inputs)

    def is_passing(self, func: Callable) -> bool:
        output = func(*self.inputs)
        if not isoneof(output, [list, tuple]):
            output = (output,)
        return output == self.outputs

    def test(self, func: Callable, verbose: bool = False, test_number: int = 0) -> bool:
        has_passed = False
        try:
            msg = None
            res = self.acquire_result(func)
            if not isoneof(res, [list, tuple]):
                res = (res,)
            has_passed = res == self.outputs
            msg = f"{test_number}: {func.__qualname__}{self.inputs} => {res} := {self.outputs}"
        except Exception as e:
            if type(e).__qualname__ == self.exceptions:
                passed_test = True
            msg = f"{test_number}: {func.__qualname__}{self.inputs} => {type(e).__qualname__}"
            if passed_test:
                msg += f" := {self.exceptions}"
            else:
                msg += f"{e.args} := {self.exceptions}"
        finally:
            if has_passed:
                if verbose:
                    Test.passed(msg)
            else:
                Test.failed(msg)
            return has_passed


# @pytest.mark.filterwarnings("ignore:api v1")
class TestFactory(DisablePytestDiscovery):
    @validate_explicit(None, Callable, bool)
    def __init__(self, func: Callable, verbose: bool = False):
        self.func = func
        self.tests: list[Test] = []
        self.verbose = verbose

    @validate_explicit(None, Test)
    def add_test(self, test: Test):
        self.tests.append(test)
        return self

    def add_tests(self, tests: Sequence[Test]):
        self.tests.extend(tests)
        return self

    def __call__(self) -> bool:
        name = f"{self.func.__module__}.{self.func.__qualname__}"
        print(f"Testing {name}...\n")
        count: int = 0
        pass_count: int = 0
        for i, test in enumerate(self.tests):
            if test.test(self.func, self.verbose, i):
                pass_count += 1
            count += 1
        print()
        print(f"PASSED {pass_count} / {count}".center(20, " ").center(40, "="))
        return pass_count == count

    def execute(self) -> bool:
        return self()


@validate_explicit(str, str, bool)
def create_test_file(path: str, output_folder: str = None, overwrite: bool = False):
    filename = Path(path).stem
    output_path = f"./test_{filename.lower()}.py"
    if output_folder is not None:
        output_path = f"{output_folder}/test_{filename.lower()}.py"
    if output_folder is not None and file_exists(output_path) and not overwrite:
        return

    lines = read_file(path)
    allowed = ["def", "class", "@property"]

    def is_ok(line: str):
        for allow in allowed:
            if line.strip().startswith(allow):
                return True
        return False
    lines = filter(is_ok, lines)

    in_file_parts = []
    import_path = ".".join([part for part in Path(path).parts])[:-3]
    res = [
        "from danielutils import TestFactory, Test\n",
        f"from {import_path} import *\n",
        "\n\n"
    ]
    indents = 0
    is_property: bool = False
    for line in lines:
        matches = re.search(r"^( {4})+", line)
        if matches is not None:
            indents = matches.regs[0][1]//4
        else:
            indents = 0
        if indents == 0 and len(in_file_parts) > 0:
            in_file_parts.pop()

        if "@property" in line:
            is_property = True
            continue

        if line.strip().startswith("class"):
            class_name = re.findall(r"class (\b\w+\b)", line)
            if class_name:
                in_file_parts.append(class_name[0])
            continue
        if indents != len(in_file_parts):
            continue

        name = re.findall(r"def (.+?)\(", line.strip())
        if not name or "#" in line or line.startswith("def __"):
            continue
        name = name[0]
        res.append(f"def test_{name}():\n")
        func_name = ".".join(v for v in in_file_parts+[name])

        if is_property:
            params = "*args,**kwargs"
            res.append(
                f"\tdef inner({params}): return {filename}({params}).{name}\n")
            func_name = "inner"
            is_property = False
        res.append(
            f"\tassert TestFactory({func_name}).add_tests([\n\t\n\t])()\n\n\n")
    if len(res) > 3:
        write_to_file(output_path, res)


__all__ = [
    "Test",
    "TestFactory",
    "create_test_file"
]
# def test_func(functor, inputs, outputs) -> None:
#     if not callable(functor):
#         raise TypeError("functor must return true for callable(functor)")

#     if len(inputs) != len(outputs):
#         raise ValueError("Amount of inputs and outputs is different")

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
