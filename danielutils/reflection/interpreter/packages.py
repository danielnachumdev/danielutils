# from typing import Optional
# from ...system import cm
# from ...decorators import memo
#
# @memo
# def get_currently_installed_packages() -> list[tuple[str, str]]:
#     ret, out, err = cm("pip", "list")
#     text = out.decode("utf-8")
#     res = []
#     for line in text.splitlines()[2:]:
#         splits = line.split(" ")
#         dep = splits[0]
#         ver = splits[-1]
#         res.append((dep, ver))
#     return res
#
#
# def is_package_installed(name: str, *, min_version: Optional[str] = None, max_version: Optional[str] = None) -> bool:
#     for dep, ver in get_currently_installed_packages():
#         if dep == name:
#             res = True
#             if min_version is not None:
#                 res = res and ver >= min_version
#             if max_version is not None:
#                 res = res and ver <= max_version
#             return res
#     return False
#
#
# __all__ = [
#     "get_currently_installed_packages",
#     "is_package_installed"
# ]
