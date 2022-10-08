from danielutils import read_file, write_to_file
import re
from pathlib import Path


@validate(str)
def create_test_file(path: str):
    lines = read_file(path)
    lines = [line.strip() for line in lines if "def" in line]
    filename = Path(path).stem
    import_path = ".".join([part for part in Path(path).parts])[:-3]
    res = [
        "from danielutils import TestFactory, Test\n",
        f"from {import_path} import *\n"
    ]
    res.append("\n\n")
    for line in lines:
        name = re.findall(r"def (.+)\(", line)[0]
        res.append(
            f"def test_{name}():\n\tassert TestFactory({name}).add_tests([\n\t\n\t])()\n\n\n")
    write_to_file(f"./test_{filename.lower()}.py", res)
