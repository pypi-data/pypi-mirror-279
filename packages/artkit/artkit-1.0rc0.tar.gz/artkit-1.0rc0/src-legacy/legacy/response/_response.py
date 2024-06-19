"""
Implementation of the Response class.
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from collections.abc import Iterator
from typing import Any, Generic, TypeVar

from fluxus.lineage import HasLineage

from artkit.model.llm.history import ChatMessage, UserMessage
from pytools.api import appenddoc, inheritdoc
from pytools.repr import HasDictRepr

from ..challenge.base import Challenge

log = logging.getLogger(__name__)

__all__ = [
    "SingleTurnResponse",
    "Response",
]

#
# Type variables
#
# Naming convention used here:
# _ret for covariant type variables used in return positions
# _arg for contravariant type variables used in argument positions

T_Challenge_ret = TypeVar("T_Challenge_ret", bound=Challenge, covariant=True)
T_Source_ret = TypeVar("T_Source_ret", bound=HasLineage[Any], covariant=True)


class Response(
    HasLineage[T_Source_ret], HasDictRepr, Generic[T_Source_ret], metaclass=ABCMeta
):
    """
    A response from an LLM system to a challenge.
    """

    @property
    def product_name(self) -> str:
        """[see superclass]"""
        return Response.__name__

    @abstractmethod
    def get_messages(self) -> Iterator[ChatMessage]:
        """
        Iterate over the messages in this response.

        :return: an iterator over the messages in this response
        """


@inheritdoc(match="[see superclass]")
class SingleTurnResponse(Response[T_Challenge_ret], Generic[T_Challenge_ret]):
    """
    A response to a challenge.
    """

    #: The response to the challenge.
    message: str

    #: The challenge that the LLM responded to.
    challenge: T_Challenge_ret

    @appenddoc(to=Response.__init__)
    def __init__(self, message: str, *, challenge: T_Challenge_ret) -> None:
        """
        :param message: the response to the challenge
        :param challenge: the challenge that the LLM responded to
        """
        self.message = message
        self.challenge = challenge

    @property
    def precursor(self) -> T_Challenge_ret:
        """[see superclass]"""
        return self.challenge

    def get_messages(self) -> Iterator[ChatMessage]:
        """[see superclass]"""
        yield UserMessage(self.message)
