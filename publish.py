from quickpub import publish, Version, MypyRunner, PylintRunner, PypircEnforcer, LocalVersionEnforcer, \
    ReadmeEnforcer, PypiRemoteVersionEnforcer, LicenseEnforcer, GithubUploadTarget, PypircUploadTarget, \
    SetuptoolsBuildSchema, PytestRunner
from tqdm import tqdm


def main() -> None:
    publish(
        name="danielutils",
        version="1.1.24",
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
        upload_targets=[PypircUploadTarget(), GithubUploadTarget()],
        global_quality_assurance_runners=[
            MypyRunner(bound="<=150"),
            PylintRunner(bound=">=0.8"),
            PytestRunner(bound=">=0.8"),
        ],
        pbar=tqdm(desc="QA", leave=False),  # type: ignore
    )


if __name__ == "__main__":
    main()
