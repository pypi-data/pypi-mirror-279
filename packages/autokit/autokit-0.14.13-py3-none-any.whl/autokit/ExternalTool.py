"""
A framework for managing and executing downloadable tools.
"""

import platform
import shlex
import shutil
import subprocess
import sys
from abc import ABC, abstractmethod
from pathlib import Path

from . import ToolConfig, PlatformData
from .ExecutableType import ExecutableType
from .downloader import download
from .progressBar import print_progress_bar


class ExternalTool(ABC):
    """
    The base class for all external tools. This class provides a framework for managing and executing downloadable tools.
    Make sure to implement the config property in the subclass by defining the config property in the subclass.
    """

    def __init__(self, base_dir: Path = "./third-party", progress_bar: bool = False, lazy_setup: bool = False):
        self.base_dir = Path(base_dir)

        if not lazy_setup:
            self.setup(progress_bar)

    @property
    @abstractmethod
    def config(self) -> ToolConfig:

        raise NotImplementedError("config property must be implemented. Have you forgot to add @property decorator?")

    @property
    def tool_name(self) -> str:
        """
        Returns the name of the tool.
        """
        return self.config.tool_name

    @property
    def python(self) -> bool:
        return self.config.executable_type == ExecutableType.PYTHON

    @property
    def tool_directory(self) -> Path:
        """
        Returns the directory where the tool is installed.
        """
        return Path(self.base_dir) / self.tool_name

    def setup(self, use_progress_bar=False) -> bool:
        """
        Sets up the tool by downloading and extracting it.
        """
        if self.calculate_path().exists():
            return True

        self.tool_directory.mkdir(parents=True, exist_ok=True)
        url = self.get_platform_data().url

        # check if the tool is already downloaded
        if self.calculate_path().exists():
            return True

        if use_progress_bar:
            download(self.tool_directory, url, progress_callback=print_progress_bar)
        else:
            download(self.tool_directory, url)

        if self.python:
            requirements = (self.calculate_dir() / "requirements.txt")

            if requirements.exists():
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-r",
                     requirements.resolve()])

        return True

    def get_platform_data(self) -> PlatformData:
        """
        Returns the platform data for the current operating system.

        Raises:
            ValueError: If the operating system is not supported.
        """
        system = platform.system()

        platform_data = self.config.platform_data

        for key in platform_data:
            if key.lower() == system.lower():
                system = key
                break

        if system not in platform_data:
            raise ValueError(f"Unsupported operating system: {system}")
        return platform_data[system]

    def run_command(self, cmd: str, working_directory: Path = None, stdout=None, stderr=None, stdin=None) -> int:
        """
        Run a command in a subprocess.

        Args:
            cmd: The command to run as a string.
            working_directory: The working directory for the subprocess.
            stdout: The file-like object to use as stdout.
            stderr: The file-like object to use as stderr.
            stdin: The file-like object to use as stdin.

        Returns:
            The exit code of the subprocess.
        """

        if not self.setup():
            raise ValueError(f"Could not set up {self.tool_name}")

        command_args = self.generate_command(cmd)

        with subprocess.Popen(command_args, stdout=stdout, stderr=stderr, stdin=stdin, bufsize=1,
                              universal_newlines=True, cwd=working_directory) as p:

            if p.stdout:
                while True:
                    line = p.stdout.readline()
                    if not line:
                        break

            exit_code = p.wait()
        return exit_code

    def generate_command(self, cmd):
        if self.config.executable_type == ExecutableType.EXECUTABLE:
            full_command = f'"{self.calculate_path().resolve()}" {cmd}'
        elif self.config.executable_type == ExecutableType.PYTHON:
            full_command = f'"{sys.executable}" "{self.calculate_path().resolve()}" {cmd}'
        elif self.config.executable_type == ExecutableType.RScript:
            if shutil.which("Rscript") is None:
                raise ValueError("R is not installed or has not been added to path environment variable.")
            full_command = f'Rscript "{self.calculate_path().resolve()}" {cmd}'
        else:
            raise ValueError(f"Unsupported executable type: {self.config.executable_type}")
        command_args = shlex.split(full_command, posix=False)
        for i, arg in enumerate(command_args):
            if arg.startswith('"') and arg.endswith('"'):
                command_args[i] = arg[1:-1]
        return command_args

    def run_command_console(self, command: str, working_directory: Path = None) -> int:
        return self.run_command(command, working_directory=working_directory, stdin=sys.stdin, stdout=sys.stdout,
                                stderr=sys.stderr)

    def run_command_cmd(self, command: str, stdin=None, stdout=None, working_directory: Path = None) -> int:
        """
        Runs a command by creating a batch file and running it in a new CMD process.
        This is a workaround for running commands that require a CMD environment.
        Note 1) that this method is currently only supported on Windows.
        Note 2) that this method opens up the same can of worms as running popen with shell=True.

        Args:
            command: The command to run as a string.
            stdin: The file-like object to use as stdin.
            stdout: The file-like object to use as stdout.
        """
        # create a new batch file

        # get a temporary file name
        temp_filename = self.tool_name + ".bat"

        batch_file_path = self.tool_directory / temp_filename

        # build folder path
        if not batch_file_path.parent.exists():
            batch_file_path.parent.mkdir(parents=True)

        commands = self.generate_command(command)

        for cmd in commands:
            if " " in cmd:
                commands[commands.index(cmd)] = f'"{cmd}"'

        batch_file_lines = ["@echo off"]

        if working_directory:
            batch_file_lines.append(f'cd "{working_directory.resolve()}"')

        batch_file_lines.append(f'start "{self.tool_name}" /i /wait ' + " ".join(commands))

        batch_file_lines.append(f'cd "{Path.cwd()}"')
        batch_file_lines.append("exit")

        with open(batch_file_path, "w+") as file:
            # write the batch file. Each line is written with a newline character at the end.
            # file.writelines(batch_file_lines) would not add the newline character.
            for line in batch_file_lines:
                file.write(line + "\n")

        # run the batch file in a new cmd window
        result = subprocess.run([batch_file_path], shell=True, stdin=stdin, stdout=stdout)

        # clean up the batch file
        # batch_file.unlink()
        return result.returncode

    def calculate_path(self) -> Path:
        """
        Calculates the path of the tool based on the operating system.
        """
        directory = self.calculate_dir()
        platform_data = self.get_platform_data()
        path = Path(directory) / Path(platform_data.executable)
        return path

    def calculate_dir(self) -> Path:
        """
        Calculates the directory path of the tool based on the operating system.
        """
        subdir = self.get_platform_data().subdir
        if subdir:
            directory = self.tool_directory / subdir
        else:
            directory = self.tool_directory
        return directory
