from typing import Any

__all__ = ["dist_is_editable", "package_is_editable"]

import pkg_resources


def dist_is_editable(dist: Any) -> bool:
    """
    Return True if given Distribution is an editable installation."""
    import sys
    from pathlib import Path

    for path_item in sys.path:
        egg_link = Path(path_item) / f"{dist.project_name}.egg-link"
        if egg_link.is_file():
            return True
    return False


def package_is_editable(package_name: Any) -> bool:
    distributions = {v.key: v for v in pkg_resources.working_set}
    if package_name in distributions:
        distribution = distributions[package_name]
        return dist_is_editable(distribution)
