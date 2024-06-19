"""
Implementation of ChallengeType.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable

from pytools.data.taxonomy import Category

log = logging.getLogger(__name__)

__all__ = [
    "ChallengeCategory",
]


class ChallengeCategory(Category):
    """
    A type of challenge that an LLM system can be evaluated on.
    """

    #: The name of the challenge type.
    _name: str

    #: A human-readable description of the challenge type.
    description: str

    def __init__(
        self,
        name: str,
        *,
        description: str,
        children: ChallengeCategory | Iterable[ChallengeCategory] = (),
    ) -> None:
        """
        :param name: the name of the challenge type
        :param description: a human-readable description of the challenge type
        :param children: subtypes of this challenge type (optional)
        """
        super().__init__(children=children)
        self._name = name
        self.description = description

    @property
    def name(self) -> str:
        """
        The name of the challenge type.
        """
        return self._name
