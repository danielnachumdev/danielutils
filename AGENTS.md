# danielutils – Agent Context

Implementation guide for coding agents changing **danielutils**. Product pitch and user-facing install: [`README.md`](README.md).

---

## Orientation

| Question | Answer |
| -------- | ------ |
| What is this? | Python utilities library (types, async, DB abstractions, retry, data structures, DX tools) |
| Importable code | `danielutils/` |
| Toolchain | [uv](https://docs.astral.sh/uv/) + `pyproject.toml` / `uv.lock` |
| Python | `>=3.11` (CI matrix **3.11, 3.12, 3.13** via actions) |
| Tests | `tests/` — pytest + coverage; **never delete** |
| Secrets | Never commit `.pypirc`, API keys, tokens |

```text
.
├── .github/             # CODEOWNERS, dependabot.yml, thin CI/CD orchestrators
├── danielutils/         # Importable package
├── tests/
├── scripts/             # Local helpers (not publish path)
├── pyproject.toml
├── uv.lock
├── README.md            # Marketing / user docs
├── LICENSE              # MIT
└── READMES/             # Feature deep-dives
```

Shared CI/CD: [`danielnachumdev/actions`](https://github.com/danielnachumdev/actions) (`@latest`). How to adopt: [`HOW-TO-USE.md`](https://github.com/danielnachumdev/actions/blob/latest/HOW-TO-USE.md).

---

## Develop

```bash
uv sync                 # default-groups: dev + test → .venv
uv sync --group dev     # explicit; same with current pyproject
# or: uv sync --all-groups
```

`tool.uv.default-groups` is `["dev", "test"]` — plain `uv sync` installs those groups.

| Task | Command |
| ---- | ------- |
| Import smoke | `uv run python -c "import danielutils; print(danielutils.__version__)"` |
| Tests | `uv run pytest` |
| Types | `uv run mypy` |
| Lint | `uv run pylint danielutils` |

Config for mypy / pylint / pytest / coverage lives in `pyproject.toml`.

### Dependencies

- **Runtime:** `pydantic`, `redis`, `sqlalchemy`, `tqdm`
- **Dev group:** mypy, pylint≥4.0.9, setuptools≥84.1.0, twine, wheel≥0.46.2, `types-tqdm`, `githooklib`
- **Test group:** pytest≥9.0.3, pytest-asyncio, pytest-cov, pytest-xdist, fastapi, uvicorn
- **Constraint floors** (`[tool.uv] constraint-dependencies`): anyio, pygments, requests, setuptools, starlette, urllib3, wheel — keep in sync with Dependabot GHSA patches

Prefer editing floors in `pyproject.toml` and regenerating with `uv lock` / `uv sync`.

---

## Code style & domain notes

- Follow the writing-python skill when adding/refactoring modules (class-first, SRP files, no stub shims).
- Public surface is re-exported from `danielutils/__init__.py` (leaf modules first, then reflection/decorators-dependent layers — **import order matters**).
- `__version__` is `importlib.metadata.version("danielutils")` — always the installed distribution version (CD stamps `pyproject.toml` into the release wheel). Do **not** hard-code a version string in source.
- Feature write-ups for users live under [`READMES/`](READMES/); keep agent/CI details here, not in the marketing README.

---

## PRs, CI, and releases

1. Branch off `main`; open a PR into `main`.
2. Attach **exactly one** semver label: `noBump` | `bumpPatch` | `bumpMinor` | `bumpMajor`.
3. **CI** — `…/ci.yml@latest` (tests) + `…/semver-ci.yml@latest` (validate label). Prefer **`CI / CI`** and **`Semver / Semver`**.
4. **CD** — `…/semver-cd.yml@latest` after CI succeeds on `main`: bump → wheel → GitHub Release → floating `vMAJOR` → **PyPI** (`publish-pypi: true`), or skip on `noBump`.
5. Version **source of truth** is GitHub Release tags. If none yet, CD seeds from `pyproject.toml`.
6. Dependabot PRs stay on `noBump`.
7. Change shared CI/semver behavior in **`danielnachumdev/actions`**, not by re-vendoring here.

**PyPI:** shipped only via CD (Trusted Publishing OIDC preferred for repo + workflow `cd.yml`; optional repo secret `PYPI_API_TOKEN`). Thin CD must grant `id-token: write` and pass `PYPI_API_TOKEN` by name. There is no local `publish.py` / quickpub path.

### Repo gates (already configured)

- `.github/CODEOWNERS` — `@danielnachumdev`
- Branch protection / ruleset: required **`CI / CI`** + **`Semver / Semver`**; code-owner reviews; no force-push to `main`
- Private vulnerability reporting via GitHub Security Advisories

---

## Sensitive / ignored

Do not commit: `.pypirc`, `.venv/`, `venv/`, `dist/`, `__pycache__/`, API keys. Track `uv.lock`. Respect `.gitignore`.
