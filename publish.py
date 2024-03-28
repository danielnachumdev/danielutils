from quickpub import publish, Version


def main() -> None:
    publish(
        name="danielutils",
        src="./danielutils",
        version="0.9.69",
        author="danielnachumdev",
        author_email="danielnachumdev@gmail.com",
        description="A python utils library for things I find useful",
        min_python=Version(3, 8, 17),
        homepage="https://github.com/danielnachumdev/danielutils",
        keywords=['functions', 'decorators', 'methods', 'classes', 'metaclasses'],
        dependencies=["tqdm"]
    )


if __name__ == "__main__":
    main()
