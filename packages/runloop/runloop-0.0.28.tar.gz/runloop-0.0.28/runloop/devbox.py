import abc
from dataclasses import dataclass
from typing import Tuple, overload


@dataclass
class FileTools(abc.ABC):
    """The runloop FileTools provides the ability to interact with files. TODO."""

    @overload
    @abc.abstractmethod  # File handle operation ?
    def create_file(self, file_name: str, file_contents: str) -> None: ...

    @overload
    @abc.abstractmethod
    def read_file(self, file_name: str) -> str: ...

    @overload
    @abc.abstractmethod
    def write_file(self, file_name: str, file_contents: str) -> None: ...

    @overload
    @abc.abstractmethod
    def delete_file(self, file_name: str) -> None: ...


@dataclass
class ShellTools(abc.ABC):
    """The runloop ShellTools provides the ability to interact with the shell. TODO."""

    @overload
    @abc.abstractmethod
    def exec(self, command: str) -> Tuple[str, str, str]: ...


class Devbox(abc.ABC):
    """A developer box that can be utilized for running, code, tests and other tasks. TODO."""

    # Constructor initialization with latch ID
    def __init__(self, devbox_id: str, file_tools: FileTools, shell_tools: ShellTools):
        self.id = devbox_id
        self.file_tools = file_tools
        self.shell_tools = shell_tools
