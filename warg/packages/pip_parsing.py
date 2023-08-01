from pathlib import Path
from typing import List, Union

from packaging.requirements import Requirement
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
from pip._internal.req.req_file import ParsedRequirement
from pip._internal.utils.packaging import get_requirement


from urllib.parse import urlparse

__all__ = ["get_requirements_from_file"]


def get_reqed(req: ParsedRequirement) -> Requirement:
    req_ = req.requirement
    if req.is_editable:  # parse out egg=... fragment from VCS URL
        parsed = urlparse(req_)
        egg_name = parsed.fragment.partition("egg=")[-1]
        without_fragment = parsed._replace(fragment="").geturl()
        req_parsed = f"{egg_name} @ {without_fragment}"
    else:
        req_parsed = req_
    return get_requirement(req_parsed)


def get_requirements_from_file(
    file_path: Union[str, Path], session: Union[str, PipSession] = "test"
) -> List[Requirement]:
    """Turn requirements.txt into a list"""
    if isinstance(file_path, Path):
        file_path = str(file_path)
    return [get_reqed(ir) for ir in parse_requirements(file_path, session=session)]


if __name__ == "__main__":
    print(get_requirements_from_file(Path(__file__).parent.parent.parent / "requirements.txt"))
