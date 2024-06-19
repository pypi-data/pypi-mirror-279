"""
Implementation of ``ConfigFileReader``.
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import Any, TextIO, final

from pytools.api import inheritdoc

from ._base import ConfigReader

log = logging.getLogger(__name__)

__all__ = [
    "ConfigFileReader",
]


@inheritdoc(match="[see superclass]")
class ConfigFileReader(ConfigReader, metaclass=ABCMeta):
    """
    Reads data from a configuration file.
    """

    #: The path to the configuration file.
    path: str

    def __init__(self, path: str) -> None:
        """
        :param path: the path to the configuration file
        """
        self.path = path

    @final
    def read(self) -> dict[str, Any]:
        """[see superclass]"""
        with open(self.path) as file:
            data = self.read_file(file)

        if not isinstance(data, dict):
            raise ValueError(
                f"File {self.path!r} must contain a single dictionary, "
                f"but found a {type(data).__name__}"
            )

        return data

    @abstractmethod
    def read_file(self, file: TextIO) -> Any:
        """
        Read the configuration file and produce a dict.

        :param file: the file to read
        :return: a dict representation of a configuration
        """
