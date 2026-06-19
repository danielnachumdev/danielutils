from pathlib import Path
from typing import Any

from quickpub import publish, Version, MypyRunner, PylintRunner, PypircEnforcer, LocalVersionEnforcer, \
    ReadmeEnforcer, PypiRemoteVersionEnforcer, LicenseEnforcer, GithubUploadTarget, PypircUploadTarget, \
    SetuptoolsBuildSchema, PytestRunner
from quickpub.strategies.upload_target import UploadTarget
from tqdm import tqdm


class PyprojectRestoreUploadTarget(UploadTarget):
    """Restore full pyproject.toml before GithubUploadTarget commits."""

    def __init__(self, pyproject_backup: str, verbose: bool = False) -> None:
        super().__init__(verbose)
        self.pyproject_backup = pyproject_backup

    def upload(self, **kwargs: Any) -> None:
        Path("pyproject.toml").write_text(self.pyproject_backup, encoding="utf-8")


def main() -> None:
    pyproject_path = Path("pyproject.toml")
    pyproject_backup = pyproject_path.read_text(encoding="utf-8")
    try:
        publish(
            name="danielutils",
            version="1.1.25",
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
            upload_targets=[
                PypircUploadTarget(),
                PyprojectRestoreUploadTarget(pyproject_backup),
                GithubUploadTarget(),
            ],
            global_quality_assurance_runners=[
                MypyRunner(bound="<=158"),
                PylintRunner(bound=">=0.8"),
                PytestRunner(bound=">=0.8"),
            ],
            pbar=tqdm(desc="QA", leave=False),  # type: ignore
        )
    finally:
        pyproject_path.write_text(pyproject_backup, encoding="utf-8")


if __name__ == "__main__":
    main()
