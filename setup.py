from setuptools import setup, find_packages
import codecs


def read_file(path: str) -> "list[str]":
    with codecs.open(path, 'r', 'utf-8') as f:
        return [l.strip() for l in f.readlines()]


README_PATH = 'README.md'
VERSION = '0.7.6'
DESCRIPTION = 'A python utils library for things I find useful'
LONG_DESCRIPTION = '\n'.join(read_file(README_PATH))
setup(
    name="danielutils",
    version=VERSION,
    author="danielnachumdev",
    author_email="<danielnachumdev@gmail.com>",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/danielnachumdev/danielutils',
    license="MIT License",
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests", "archive/"]),
    install_requires=["bs4"],
    platforms=["All"],
    keywords=['functions', 'decorators', 'methods'],
    classifiers=[
        # "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
# python .\setup.py sdist
# twine upload dist/...
