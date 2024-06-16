# autokit version 0.14.15



A framework for effortlessly integrating external tools into your Python projects.

## Installation

```bash
pip install autokit 
```

## Basic Usage

```python
from autokit import ToolConfig, PlatformData, ExternalTool
from pathlib import Path

class TestTool(ExternalTool):
    def __init__(self, base_dir: str = "./third-party", progress_bar: bool = True, lazy_setup: bool = False):
        super().__init__(base_dir, progress_bar, lazy_setup)

    @property
    def config(self) -> ToolConfig:
        return ToolConfig(
            tool_name="tests-tool",
            platform_data={
                "windows": PlatformData(
                    url="https://github.com/IRSS-UBC/MediaTools/releases/download/latest/win-x64.zip",
                    subdir=Path(""),
                    executable=Path("IRSSMediaTools.exe")
                ),
            },
            python=False,
        )

    def help(self):
        self.run_command("help")


if __name__ == "__main__":
    test = TestTool()
    test.help()
```

## Features
- Automatic download and configuration of external tools on first use.
- Define tools and their commands in a configuration file.
- Streamlined execution of tool commands from within your Python code.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)


Contact: olson@student.ubc.ca