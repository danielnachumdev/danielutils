from pathlib import Path

from quickpub import publish, Version, MypyRunner, PylintRunner, PypircEnforcer, LocalVersionEnforcer, \
    ReadmeEnforcer, PypiRemoteVersionEnforcer, LicenseEnforcer, PypircUploadTarget, \
    SetuptoolsBuildSchema, PytestRunner
from quickpub.enforcers import exit_if
from quickpub.proxy import cm
from tqdm import tqdm

VERSION = "1.1.25"


def _commit_and_push(version: str) -> None:
    ret, _, stderr = cm("git", "add", ".")
    exit_if(ret != 0, stderr.decode(encoding="utf-8"))
    ret, _, stderr = cm("git", "commit", "-m", f"updated to version {version}")
    exit_if(ret != 0, stderr.decode(encoding="utf-8"))
    ret, _, stderr = cm("git", "push")
    exit_if(ret != 0, stderr.decode(encoding="utf-8"))


def main() -> None:
    pyproject_path = Path("pyproject.toml")
    pyproject_backup = pyproject_path.read_text(encoding="utf-8")
    published = False
    try:
        publish(
            name="danielutils",
            version=VERSION,
            author="danielnachumdev",
            author_email="danielnachumdev@gmail.com",
            description="A comprehensive Python utilities library providing type-safe collections, async programming tools, database abstractions, retry executors, data structures, and developer productivity enhancements to streamline Python development workflows",
            min_python=Version(3, 8, 0),
            dependencies=[
                "pydantic>=2.10.6",
                "redis>=6.1.1",
                "sqlalchemy>=2.0.51",
                "tqdm>=4.68.3",
            ],
            homepage="https://github.com/danielnachumdev/danielutils",
            enforcers=[
                PypircEnforcer(), ReadmeEnforcer(), LicenseEnforcer(),
                LocalVersionEnforcer(), PypiRemoteVersionEnforcer()
            ],
            build_schemas=[SetuptoolsBuildSchema()],
            upload_targets=[PypircUploadTarget()],
            global_quality_assurance_runners=[
                MypyRunner(bound="<=158"),
                PylintRunner(bound=">=0.8"),
                PytestRunner(bound=">=0.8"),
            ],
            pbar=tqdm(desc="QA", leave=False),  # type: ignore
        )
        published = True
    finally:
        pyproject_path.write_text(pyproject_backup, encoding="utf-8")

    if published:
        _commit_and_push(VERSION)


if __name__ == "__main__":
    main()
