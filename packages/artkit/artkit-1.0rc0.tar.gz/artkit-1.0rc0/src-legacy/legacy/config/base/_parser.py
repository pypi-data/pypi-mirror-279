"""
Implementation of base configuration parsers.
"""

from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Any, Generic, TypeVar

from pytools.api import inheritdoc
from pytools.data.taxonomy import Category, Taxonomy

from ._base import ConfigParser

log = logging.getLogger(__name__)

__all__ = [
    "TaxonomyParser",
]

#
# Type variables
#

T_Category = TypeVar("T_Category", bound=Category)

#
# Classes
#


@inheritdoc(match="[see superclass]")
class TaxonomyParser(ConfigParser, Generic[T_Category]):
    """
    Creates :class:`.Taxonomy` objects from configuration data.
    """

    @property
    @abstractmethod
    def category_type(self) -> type[T_Category]:
        """
        The type of category to parse.
        """

    def parse(self) -> Taxonomy[T_Category]:
        """[see superclass]"""

        read = self.reader.read()
        log.debug(read)
        return Taxonomy(root=self._build_category(config=read))

    def _build_category(self, config: dict[str, Any]) -> T_Category:
        """
        Helper function for constructing nested categories.

        :param config: the config dict containing category fields
        :return: a category instance
        """

        return self.category_type(
            **{
                key: (
                    value
                    if key != "children"
                    else tuple(self._build_category(child) for child in value)
                )
                for key, value in config.items()
            }
        )
