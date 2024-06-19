"""
Base class implementations
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import Any

from fluxus.lineage import HasLineage

from pytools.repr import HasDictRepr

log = logging.getLogger(__name__)

__all__ = [
    "Challenge",
]


#
# Classes
#


class Challenge(HasLineage[Any], HasDictRepr, metaclass=ABCMeta):
    """
    Abstract base class for all types of challenges to test a target LLM system.

    Includes a prompt to be sent to the target LLM system.

    Concrete subclasses include

    - :class:`PromptChallenge`
    - :class:`QnAChallenge`
    - :class:`MultipleChoiceChallenge`
    - :class:`PersonaChallenge`

    Challenges form part of the lineage of a testing flow.

    For challenges that are derived from a preceding challenge, the :attr:`precursor`
    property can be set to the preceding challenge.
    The preferred way to augment a challenge is to use a :class:`ChallengeAugmenter`,
    which will take care of setting the :attr:`precursor` property.
    """

    #: The original challenge that this challenge augments.
    _precursor: HasLineage[Any] | None = None

    @property
    def product_name(self) -> str:
        """[see superclass]"""
        return Challenge.__name__

    @property
    def precursor(self) -> HasLineage[Any] | None:
        """
        The preceding product.
        """
        return self._precursor

    @precursor.setter
    def precursor(self, precursor: HasLineage[Any] | None) -> None:
        self._precursor = precursor

    @property
    @abstractmethod
    def prompt(self) -> str:
        """
        A main prompt of this challenge.
        """
