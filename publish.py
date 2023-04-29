from danielutils import cm, read_file, get_files, directory_exists
import re
VERSION_PATTERN = r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
SETUP = "./setup.py"
TOML = "./pyproject.toml"
README = "./README.md"
DIST = "./dist"


def get_latest(version: str = '0.0.0') -> str:
    """returns the latest version currently in the DIST fuller

    Args:
        version (str, optional): the version to compare against. Defaults to '0.0.0'.

    Returns:
        str: the biggest version number
    """
    if not directory_exists(DIST):
        return version
    DIST_PATTERN = r"danielutils-(\d+)\.(\d+)\.(\d+)\.tar\.gz"
    best = version
    for filename in get_files(DIST):
        a1, b1, c1 = best.split(".")
        match = re.match(DIST_PATTERN, filename)
        if match:
            a2, b2, c2 = match.groups()
            other_version = f"{a2}.{b2}.{c2}"
            if int(a2) > int(a1):
                best = other_version
            elif int(a2) == int(a1):
                if int(b2) > int(b1):
                    best = other_version
                elif int(b2) == int(b1):
                    if int(c2) > int(c1):
                        best = other_version
    return best


def handle_git(version):
    cm("git add .")
    cm(f"git commit -m \"updated to version {version}\"")
    cm("git push")


def main(version: str):
    """main function, create a new release and update the files and call terminal to upload the release

    Args:
        version (str): the new version
    """

    def update_version(version: str):
        """updates the new version number in the relevant files

        Args:
            version (_type_): _description_
        """
        def update_setup():
            lines = read_file(SETUP)
            with open(SETUP, "w", encoding="utf8") as f:
                for line in lines:
                    if line.startswith("VERSION"):
                        f.write(f"VERSION = \"{version}\"\n")
                    else:
                        f.write(line)

        def update_readme():
            lines = read_file(README)
            with open(README, "w", encoding="utf8") as f:
                for line in lines:
                    if line.startswith("# danielutils v="):
                        f.write(f"# danielutils v={version}\n")
                    else:
                        f.write(line)

        def update_toml():
            lines = read_file(TOML)
            with open(TOML, "w", encoding="utf8") as f:
                for line in lines:
                    if line.startswith("version = "):
                        f.write(f"version = \"{version}\"\n")
                    else:
                        f.write(line)
        update_readme()
        update_toml()
        update_setup()

    latest = get_latest(version)
    if latest != version:
        print(f"{version} is not the latest version, found {latest}, cancelling...")
        exit()
    print("updating version in files...")
    update_version(version)
    print("Creating new distribution...")
    ret, stdout, stderr = cm("python", "setup.py", "sdist")
    if ret != 0:
        print(stderr)
        exit()
    print("Created dist successfully")
    # # twine upload dist/...
    ret, stdout, stderr = cm("wt.exe",
                             "twine", "upload", f"dist/danielutils-{version}.tar.gz")

    handle_git(version)


def run_tests() -> bool:
    """run pytest

    Returns:
        bool: success status
    """
    def has_fails(pytest_out: str) -> bool:
        RE = r'=+ (?:(?P<FAIL>\d+ failed), )?(?P<PASS>\d+ passed) in [\d\.]+s =+'
        if not re.match(RE, pytest_out):
            print("Failed to match pytest output")
            return True

        res = re.findall(RE, pytest_out)[0]
        failed = int(res[0].split()[0]) if res[0] != "" else 0
        return failed > 0

    COMMAND = "pytest"
    if input("Do you want to generate a report as well? <y|n>: ") == "y":
        COMMAND += " --html=pytest_report.html"
    code, stdout, stderr = cm(COMMAND)
    if code != 0:
        err = stderr.decode()
        if err != "":
            print(err)
            return False
    summary = stdout.decode().splitlines()[-1]
    if has_fails(summary):
        print(summary)
        return False
    return True


def pylint():
    """run pylint
    """
    print("running pylint...")
    cm("pylint", "./danielutils", ">", "pylint_output.txt")


if __name__ == "__main__":
    if run_tests():
        pylint()
        print("Passed all tests!")
        version = input(
            f"Please supply a new version number (LATEST = {get_latest()}): ")
        if re.match(VERSION_PATTERN, version):
            main(version)
        else:
            print("invalid version. example 1.0.5.20")
__all__ = []
