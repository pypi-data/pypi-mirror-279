"""
Implementation of ``ResponseProducer``.
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from collections.abc import AsyncIterator, Iterator
from typing import Any, Generic, TypeVar, final

from fluxus import AsyncTransformer
from fluxus.lineage import LabelingTransformer

from ...challenge.base import Challenge
from .._response import Response

log = logging.getLogger(__name__)

__all__ = [
    "AsyncResponder",
    "Responder",
]

#
# Type variables
#
# Naming convention used here:
# _ret for covariant type variables used in return positions
# _arg for contravariant type variables used in argument positions

T_Challenge_arg = TypeVar("T_Challenge_arg", bound=Challenge, contravariant=True)
T_Response_ret = TypeVar("T_Response_ret", bound=Response[Any], covariant=True)


class Responder(
    LabelingTransformer[T_Challenge_arg, T_Response_ret],
    Generic[T_Challenge_arg, T_Response_ret],
    metaclass=ABCMeta,
):
    """
    Generates an iterable of responses to challenges from a challenger.
    """

    @final
    def transform(self, source_product: T_Challenge_arg) -> Iterator[T_Response_ret]:
        """
        Generate one or more responses to the given challenge, deferring to
        :meth:`respond`.

        :param source_product: the challenge to respond to
        :return: the response to the challenge
        """
        return self.respond(source_product)

    @abstractmethod
    def respond(self, challenge: T_Challenge_arg) -> Iterator[T_Response_ret]:
        """
        Generate one or more responses to the given challenge.

        :param challenge: the challenge to respond to
        :return: the response to the challenge
        """


class AsyncResponder(
    AsyncTransformer[T_Challenge_arg, T_Response_ret],
    Generic[T_Challenge_arg, T_Response_ret],
    metaclass=ABCMeta,
):
    """
    A responder for use with asynchronous I/O.
    """

    @final
    def atransform(
        self, source_product: T_Challenge_arg
    ) -> AsyncIterator[T_Response_ret]:
        """
        Generate one or more responses to the given challenge, deferring to
        :meth:`arespond`.

        :param source_product: the challenge to respond to
        :return: the response to the challenge
        """
        return self.arespond(source_product)

    @abstractmethod
    def arespond(self, challenge: T_Challenge_arg) -> AsyncIterator[T_Response_ret]:
        """
        Generate one or more responses to the given challenge.

        :param challenge: the challenge to respond to
        :return: the response to the challenge
        """
