
import danielutils

danielutils.write_to_file(
    "dir.txt", [f"{v}\n" for v in dir(danielutils) if "__" not in v])
