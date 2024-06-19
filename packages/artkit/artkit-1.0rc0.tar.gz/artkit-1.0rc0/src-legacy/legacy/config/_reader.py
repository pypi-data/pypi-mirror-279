"""
ConfigReader subclasses.
"""

import json
from typing import Any, TextIO

import yaml

from pytools.api import inheritdoc

from .base import ConfigFileReader

__all__ = [
    "JSONReader",
    "YAMLReader",
]


@inheritdoc(match="[see superclass]")
class YAMLReader(ConfigFileReader):
    """
    Reads data from a yaml file.
    """

    def read_file(self, file: TextIO) -> Any:
        """[see superclass]"""
        return yaml.safe_load(file)


@inheritdoc(match="[see superclass]")
class JSONReader(ConfigFileReader):
    """
    Reads data from a json file.
    """

    def read_file(self, file: TextIO) -> Any:
        """[see superclass]"""
        return json.load(file)
