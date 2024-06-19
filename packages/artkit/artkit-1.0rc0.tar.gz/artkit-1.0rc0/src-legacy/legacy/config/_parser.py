"""
ConfigParser subclasses.
"""

from pytools.api import inheritdoc

from ..persona import Persona
from .base import ConfigParser

__all__ = [
    "PersonaParser",
]


@inheritdoc(match="[see superclass]")
class PersonaParser(ConfigParser):
    """
    Parses an Archetype.
    """

    def parse(self) -> Persona:
        """[see superclass]"""
        return Persona(**self.reader.read())
