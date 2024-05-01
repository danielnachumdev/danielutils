from quickpub import publish, Version, AdditionalConfiguration, MypyRunner, PylintRunner, UnittestRunner


def main() -> None:
    publish(
        name="danielutils",
        version="0.9.83",
        author="danielnachumdev",
        author_email="danielnachumdev@gmail.com",
        description="A python utils library for things I find useful",
        min_python=Version(3, 8, 0),
        homepage="https://github.com/danielnachumdev/danielutils",
        keywords=['functions', 'decorators', 'methods', 'better_builtins', 'metaclasses'],
        dependencies=[],
        config=AdditionalConfiguration(
            runners=[
                MypyRunner(bound="<150", configuration_path="./mypy.ini"),
                PylintRunner(bound=">=0.8", configuration_path="./.pylintrc"),
                UnittestRunner(bound=">=0.8"),
            ]
        )
    )


if __name__ == "__main__":
    main()
