"""
Implementation of the Evaluator base class.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Any

from pytools.data.taxonomy import Category

log = logging.getLogger(__name__)

__all__ = [
    "FailureMode",
]


class FailureMode(Category):
    """
    A failure mode that an LLM system can exhibit.
    """

    #: The name of the failure mode.
    _name: str

    #: A human-readable description of the failure mode.
    description: str

    def __init__(
        self,
        *,
        name: str,
        description: str,
        children: FailureMode | Iterable[FailureMode] = (),
    ) -> None:
        """
        :param name: the name of the failure mode
        :param description: a human-readable description of the failure mode
        :param children: sub-modes of this failure mode
        (optional, defaults to an empty iterable)
        """
        super().__init__(children=children)
        self._name = name
        self.description = description

    @property
    def name(self) -> str:
        """
        The name of the failure mode.
        """
        return self._name

    def __eq__(self, other: Any) -> bool:
        return super().__eq__(other) and self.description == other.description

    def __hash__(self) -> int:
        return super().__hash__()
