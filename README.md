# danielutils

**Python utilities for day-to-day development** — type safety, async helpers, database abstractions, retry executors, data structures, and DX tools in one MIT-licensed package.

[![CI](https://github.com/danielnachumdev/danielutils/actions/workflows/ci.yml/badge.svg)](https://github.com/danielnachumdev/danielutils/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/danielutils.svg)](https://pypi.org/project/danielutils/)
[![Python](https://img.shields.io/pypi/pyversions/danielutils.svg)](https://pypi.org/project/danielutils/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Requires **Python 3.11+**.

## Why danielutils?

Common scripting and library work often re-implements the same helpers. **danielutils** packages the ones used across projects so you can validate types at runtime, talk to several DB backends behind one API, retry flaky calls, and ship progress/logging/reflection utilities without reinventing them.

- **Type safety** — `isoftype`, `@validate`, `@overload`, typed collections (`tlist`, …)
- **Async** — worker pools and async utilities
- **Database abstractions** — SQLite, Redis, and in-memory backends via one factory
- **Retry** — configurable executors with backoff strategies
- **Data structures & algorithms** — graphs, heaps, and related helpers
- **DX** — progress bars, logging, reflection, debugging aids
- **Academic** — probability / statistics helpers under `university`

## Install

```bash
pip install danielutils
# or
uv add danielutils
```

## Quick start

```python
from danielutils import isoftype, validate, tlist
from danielutils.abstractions.db import DatabaseFactory
from danielutils.abstractions.db.database_definitions import TableSchema, TableColumn, ColumnType

numbers = tlist[int]([1, 2, 3, 4, 5])

@validate
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

db = DatabaseFactory.get_database("memory")
with db:
    schema = TableSchema(
        name="users",
        columns=[
            TableColumn(name="id", type=ColumnType.AUTOINCREMENT, primary_key=True),
            TableColumn(name="name", type=ColumnType.TEXT, nullable=False),
            TableColumn(name="age", type=ColumnType.INTEGER),
        ],
    )
    db.create_table(schema)
    db.insert("users", {"name": "Alice", "age": 30})

if isoftype(numbers, list[int]):
    print("Numbers is a list of integers!")
```

## Docs by feature

Deep dives live under [`READMES/`](./READMES/):

| Topic | Doc |
| ----- | --- |
| Runtime type checks | [`isoftype`](./READMES/isoftype.md) |
| Function overloading | [`@overload`](./READMES/overload.md) |
| Argument validation | [`@validate`](./READMES/validate.md) |
| Typed lists | [`tlist`](./READMES/tlist.md) |
| Interfaces | [`Interface`](./READMES/Interface.md) |
| DB abstraction | [`database_abstraction`](./READMES/database_abstraction.md) |
| Retry | [`retry_executor`](./READMES/retry_executor.md) |
| Progress bars | [`progress_bar`](./READMES/progress_bar.md) |
| Async workers | [`async_worker_pool`](./READMES/async_worker_pool.md) |
| Singleton | [`singleton`](./READMES/singleton.md) |

## Contributing & development

Agent/developer workflow (uv, tests, CI/CD labels, secrets, `__version__`): see [`AGENTS.md`](./AGENTS.md).

Report security issues privately via [GitHub advisories](https://github.com/danielnachumdev/danielutils/security/advisories/new) — please do not open a public issue for vulnerabilities.

## License

MIT — see [`LICENSE`](./LICENSE).
