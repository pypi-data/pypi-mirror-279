from typing import Dict, NamedTuple

from autokit import PlatformData
from autokit.ExecutableType import ExecutableType


class ToolConfig(NamedTuple):
    """
    A class to represent the configuration for a tool.

    Attributes
    ----------
    tool_name : str
        The name of the tool.
    platform_data : Dict[str, PlatformData]
        The platform data for the tool.
    executable_type : ExecutableType
    """
    tool_name: str
    platform_data: Dict[str, PlatformData]
    executable_type: ExecutableType = ExecutableType.EXECUTABLE
