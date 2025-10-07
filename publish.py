import json

from quickpub import publish, Version, MypyRunner, PylintRunner, UnittestRunner, PypircEnforcer, LocalVersionEnforcer, \
    ReadmeEnforcer, PypiRemoteVersionEnforcer, LicenseEnforcer, GithubUploadTarget, PypircUploadTarget, \
    SetuptoolsBuildSchema, CondaPythonProvider
from tqdm import tqdm


def main() -> None:
    publish(
        name="danielutils",
        version="1.1.1",
        author="danielnachumdev",
        author_email="danielnachumdev@gmail.com",
        description="A python utils library for things I find useful",
        min_python=Version(3, 8, 0),
        dependencies=[],
        homepage="https://github.com/danielnachumdev/danielutils",
        enforcers=[
            PypircEnforcer(), ReadmeEnforcer(), LicenseEnforcer(),
            LocalVersionEnforcer(), PypiRemoteVersionEnforcer()
        ],
        build_schemas=[SetuptoolsBuildSchema()],
        upload_targets=[PypircUploadTarget(), GithubUploadTarget()],
        python_interpreter_provider=CondaPythonProvider(["base", "390", "380"]),
        global_quality_assurance_runners=[
            MypyRunner(bound="<=150", configuration_path="./mypy.ini"),
            PylintRunner(bound=">=0.8", configuration_path="./.pylintrc"),
            UnittestRunner(bound=">=0.8"),
        ],
        pbar=tqdm(desc="QA", leave=False),  # type: ignore
        demo=True
    )


if __name__ == "__main__":
    main()
