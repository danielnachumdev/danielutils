import sys
import os
import pkgutil
from pathlib import Path
from collections import defaultdict
from ..files_and_folders import is_directory, file_exists
from ..decorators import memo
from ..data_structures import Graph, MultiNode


def get_imports_helper(path: str):
    if not file_exists(path):
        raise ValueError(f"Can't find file {path}")

    with open(path, "r", encoding="utf-8") as f:
        return [line for line in f.readlines() if "import" in line and not line.strip().startswith("#")]


def resolve_relative(base_path: str, statement: str) -> str:
    res = base_path
    splits = statement.split(".")
    for s in splits:
        if s == "":
            res = str(Path(res).parent)
        else:
            res = os.path.join(res, s)
            break
    if not is_directory(res):
        res = f"{res}.py"
    return res


@memo
def get_all_modules():
    all_modules = set()

    # Get built-in modules
    builtin_modules = set(o.strip("_") for o in sys.builtin_module_names)

    # Get modules from the Python Standard Library
    stdlib_modules = set()
    for module in pkgutil.iter_modules():
        if not module.ispkg and module.module_finder.path.startswith(sys.prefix):  # type:ignore
            stdlib_modules.add(module.name)

    # Combine built-in modules and modules from the Python Standard Library
    all_modules.update(builtin_modules)
    all_modules.update(stdlib_modules)

    all_modules.update({
        "platform", 'os', 'pathlib', 'subprocess', "inspect", "types"
    })
    return all_modules


def resolve_absolute(statement: str) -> str:
    if statement in get_all_modules():
        return statement
    if "." in statement:
        statement = statement.split(".")[0]
        return resolve_absolute(statement)
    return statement


def resolve_path(base_path, statement) -> str:
    if "from" in statement:
        statement = statement.split("from")[1].strip()
        statement = statement.split("import")[0].strip()
        if statement.startswith("."):
            return resolve_relative(base_path, statement)
    else:
        statement = statement.split("import")[1].strip()
    return resolve_absolute(statement)


def normalize_path(path: str) -> str:
    if is_directory(path):
        path = os.path.join(path, '__init__.py')
    return path


def get_imports(path: str) -> dict:
    res = defaultdict(set)
    i = 0
    path = normalize_path(path)
    queue = [path]
    while i < len(queue):
        cur = queue[i]
        cur = str(Path(cur).absolute())
        imports = list(resolve_path(cur, imp) for imp in get_imports_helper(cur))
        for sub_path in imports:
            if sub_path in res:
                continue

            if not (file_exists(sub_path) or is_directory(sub_path)):
                res[cur].add(sub_path)
            else:
                if sub_path not in res:
                    sub_path = normalize_path(sub_path)
                    queue.append(sub_path)
                    res[cur].add(sub_path)
        i += 1
    return res


def get_dependencies(path: str, topological_sort: bool = True) -> list[str]:
    res = dict(get_imports(path))
    g = Graph()
    dct: dict[str, MultiNode] = {}
    for k, v in res.items():
        for o in v:
            dct[o] = dct.get(o, MultiNode(o))
        n = MultiNode(k, [dct[o] for o in v])
        g.add_node(n)

    if topological_sort:
        return [n.data for n in g.topological_sort()]

    return [n.data for n in g]


__all__ = [
    "get_dependencies"
]
