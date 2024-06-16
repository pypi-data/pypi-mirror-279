from pathlib import Path
from typing import Dict, NamedTuple


class PlatformData(NamedTuple):
    """
    A class to represent the data for a platform.

    Attributes
    ----------
    url : str
        The URL to download the tool from.
    executable : Path
        The path to the executable, relative to the subdir.
    subdir : Path
        The subdirectory to extract the tool to. If None, the tool will be extracted to the tool directory.
    """
    url: str
    executable: Path
    subdir: Path | None = None




