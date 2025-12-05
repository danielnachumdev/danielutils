import sys
import os
import pkgutil
from pathlib import Path
from collections import defaultdict
from typing import Set as Set, List as List, Dict as Dict
from ..interpreter import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as List, set as Set, dict as Dict


def get_all_modules() -> Set[str]:
    all_modules = set()

    # Get built-in modules
    builtin_modules = set(o.strip("_") for o in sys.builtin_module_names)

    # Get modules from the Python Standard Library
    stdlib_modules = set()
    for module in pkgutil.iter_modules():
        try:
            if not module.ispkg and module.module_finder.path.startswith(sys.prefix):  # type:ignore
                stdlib_modules.add(module.name)
        except AttributeError:
            pass

    # Combine built-in modules and modules from the Python Standard Library
    all_modules.update(builtin_modules)
    all_modules.update(stdlib_modules)

    all_modules.update({
        "platform", 'os', 'pathlib', 'subprocess', "inspect", "types", "dataclasses", "__future__", "ctypes", "pkgutil",
        "logging", "importlib", "enum", "multiprocessing", "traceback", "re", "threading"
    })
    return all_modules


ALL_MODULES: set = get_all_modules()


def get_imports_helper(path: str):
    from danielutils import file_exists
    if not file_exists(path):
        raise ValueError(f"Can't find file {path}")
    is_in_multiline_comment = False
    with open(path, "r", encoding="utf-8") as f:
        for l in f.readlines():
            l = l.strip()
            if l.startswith("#"):
                continue
            if '"""' in l:
                if l.count('"""') % 2 == 1:
                    is_in_multiline_comment = not is_in_multiline_comment

            if is_in_multiline_comment:
                continue

            if any([l.startswith("import "), l.startswith("from ")]):
                yield l


def resolve_relative(base_path: str, statement: str) -> str:
    res = base_path
    splits = statement.split(".")
    for s in splits:
        if s == "":
            res = str(Path(res).parent)
        else:
            res = os.path.join(res, s)
            break
    from danielutils import is_directory
    if not is_directory(res):
        res = f"{res}.py"
    return res


def resolve_absolute(statement: str) -> str:
    if statement in ALL_MODULES:
        return statement
    if "." in statement:
        statement = statement.split(".")[0]
        return resolve_absolute(statement)
    return statement


def resolve_path(base_path, statement: str) -> str:
    og = statement
    FROM = "from"
    IMPORT = "import"
    if FROM in statement:
        statement = statement[statement.index(FROM) + len(FROM):].strip()
        statement = statement[:statement.index(IMPORT)].strip()
        if statement.startswith("."):
            return resolve_relative(base_path, statement)
    else:
        statement = statement[statement.index(IMPORT) + len(IMPORT):].strip()
    return resolve_absolute(statement)


def normalize_path(path: str) -> str:
    from danielutils import is_directory
    if is_directory(path):
        path = os.path.join(path, '__init__.py')
    return str(Path(path).absolute())


def get_imports(path: str) -> Dict[str, Set[str]]:
    res: Dict[str, Set[str]] = defaultdict(set)
    i = 0
    path = normalize_path(path)
    queue: List[str] = [path]
    while i < len(queue):
        cur = queue[i]
        imports = list(get_imports_helper(cur))
        paths = [resolve_path(cur, imp) for imp in imports]
        for sub_path in paths:
            if sub_path in res:
                continue
            from danielutils import file_exists, is_directory
            if not (file_exists(sub_path) or is_directory(sub_path)):
                res[cur].add(sub_path)
            else:
                if sub_path not in res:
                    sub_path = normalize_path(sub_path)
                    queue.append(sub_path)
                    res[cur].add(sub_path)
        i += 1
    return res


def create_dependency_graph(path: str) -> 'Graph[str]':
    from danielutils import Graph, MultiNode
    res = dict(get_imports(path))
    g: Graph[str] = Graph()
    dct: Dict[str, MultiNode[str]] = {}
    for k, v in res.items():
        for o in v:
            dct[o] = dct.get(o, MultiNode(o))
        n = MultiNode(k, [dct[o] for o in v])
        g.add_node(n)

    return g


def get_dependencies(path: str, topological_sort: bool = True) -> List[str]:
    from danielutils import Graph
    g: Graph[str] = create_dependency_graph(path)

    if topological_sort:
        return [n.data for n in g.topological_sort()]

    return [n.data for n in g]


__all__ = [
    "get_dependencies",
    "create_dependency_graph",
    'ALL_MODULES'
]
