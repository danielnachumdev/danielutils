from quickpub import publish, Version


def main() -> None:
    publish(
        name="danielutils",
        version="0.9.75",
        author="danielnachumdev",
        author_email="danielnachumdev@gmail.com",
        description="A python utils library for things I find useful",
        min_python=Version(3, 8, 0),
        homepage="https://github.com/danielnachumdev/danielutils",
        keywords=['functions', 'decorators', 'methods', 'better_builtins', 'metaclasses'],
        dependencies=[]
    )


if __name__ == "__main__":
    main()
