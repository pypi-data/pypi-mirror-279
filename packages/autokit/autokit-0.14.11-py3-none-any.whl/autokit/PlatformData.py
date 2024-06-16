from pathlib import Path
from typing import Dict, NamedTuple


class PlatformData(NamedTuple):
    """
    A class to represent the data for a platform.

    Attributes
    ----------
    url : str
        The URL to download the tool from.
    subdir : Path
        The subdirectory to extract the tool to.
    executable : Path
        The path to the executable, relative to the subdir.
    """
    url: str
    subdir: Path
    executable: Path



