import os
from io import TextIOWrapper
from typing import Union, TextIO, Mapping
from importlib.metadata import metadata

PROG = "send-s3"
AUTHOR = metadata(PROG)["author-email"]
VERSION = metadata(PROG)["version"]
DESCRIPTION = metadata(PROG)["summary"]
LICENSE_NAME = metadata(PROG)["license"]
LINESEP = os.linesep
MACOS_HELPER_URL = "https://www.icloud.com/shortcuts/b84eab4b8df141d89a25f048047ea4ff"


URLParams = Mapping[str, str]
HTTPHeaders = Mapping[str, str]
HTTPPayload = Union[bytes, str]


def data_directory() -> str:
    if os.environ.get("APPDATA"):
        return os.environ["APPDATA"]
    if os.environ.get("XDG_CONFIG_HOME"):
        return os.path.join(os.environ["XDG_CONFIG_HOME"], '.config')
    if os.environ.get("HOME"):
        return os.path.join(os.environ["HOME"], '.config')
    raise FileNotFoundError("Could not find a suitable directory for configuration files.")


def app_directory(filename: str) -> str:
    return os.path.join(data_directory(), PROG, filename)


def human_readable_size(size: int) -> str:
    units = ['B', 'KB', 'MB', 'GB']
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"


class Console:
    def __init__(self, text: str = '') -> None:
        self.text = text

    def __rshift__(self, other: Union[str, TextIOWrapper, TextIO]) -> Union['Console', None]:
        if isinstance(other, str):
            return Console(self.text + other)
        if isinstance(other, TextIOWrapper) or isinstance(other, TextIO):
            return print(self.text, file=other, flush=True, end='')
        raise TypeError("Unsupported type for right shift operator")


__all__ = [
    "PROG", "AUTHOR", "VERSION", "DESCRIPTION", "LICENSE_NAME", "LINESEP", "MACOS_HELPER_URL",
    "URLParams", "HTTPHeaders", "HTTPPayload",
    "Console", "data_directory", "app_directory", "human_readable_size"
]
