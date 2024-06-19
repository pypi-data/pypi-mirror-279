"""
Configuration
"""

from abc import ABCMeta, abstractmethod
from typing import Any

from pytools.repr import HasDictRepr

__all__ = [
    "ConfigReader",
    "ConfigParser",
]


class ConfigReader(HasDictRepr, metaclass=ABCMeta):
    """
    Reads data from some source and produces a dict suitable for
    parsing by a ``ConfigParser``.
    """

    @abstractmethod
    def read(self) -> dict[str, Any]:
        """
        Read this reader's source and produce a dict.

        :return: a dict representation of a configuration
        """


class ConfigParser(HasDictRepr, metaclass=ABCMeta):
    """
    Parses data from the provided reader and produces a configured
    class instance.
    """

    #: The reader to use as a data source.
    reader: ConfigReader

    def __init__(self, *, reader: ConfigReader) -> None:
        """
        :param reader: the reader to use as a data source
        """
        self.reader = reader

    @abstractmethod
    def parse(self) -> Any:
        """
        Parse data from the reader and produce a configured
        class instance.

        :return: a configured class instance
        """
