from tqdm import tqdm

from quickpub import (
    publish,
    MypyRunner,
    PylintRunner,
    PypircUploadTarget,
    UvBuildSchema,
    GithubUploadTarget,
    PypircEnforcer,
    ReadmeEnforcer,
    LicenseEnforcer,
    PypiRemoteVersionEnforcer,
    LocalVersionEnforcer,
    PytestRunner,
)


def main() -> None:
    publish(
        name="danielutils",
        version="1.1.27",
        author="danielnachumdev",
        author_email="danielnachumdev@gmail.com",
        description=(
            "A comprehensive Python utilities library providing type-safe collections, "
            "async programming tools, database abstractions, retry executors, data "
            "structures, and developer productivity enhancements to streamline Python "
            "development workflows"
        ),
        homepage="https://github.com/danielnachumdev/danielutils",
        dependencies=[
            "pydantic>=2.10.6",
            "redis>=6.1.1",
            "sqlalchemy>=2.0.51",
            "tqdm>=4.68.3",
        ],
        min_python="3.8.0",
        enforcers=[
            PypircEnforcer(),
            ReadmeEnforcer(),
            LicenseEnforcer(),
            LocalVersionEnforcer(),
            PypiRemoteVersionEnforcer(),
        ],
        build_schemas=[UvBuildSchema()],
        generate_project_files=False,
        upload_targets=[PypircUploadTarget(), GithubUploadTarget()],
        global_quality_assurance_runners=[
            MypyRunner(bound="<=158"),
            PylintRunner(bound=">=0.8"),
            PytestRunner(bound=">=0.8"),
        ],
        pbar=tqdm(desc="QA", leave=False),  # type: ignore
    )


if __name__ == "__main__":
    main()
