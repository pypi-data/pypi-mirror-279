"""
Implementation of ``ChallengeProducer``.
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from collections.abc import AsyncIterator, Iterator
from typing import Generic, TypeVar, final

from fluxus import AsyncProducer, AsyncTransformer
from fluxus.lineage import LabelingProducer, LabelingTransformer

from ._challenge import Challenge

log = logging.getLogger(__name__)

__all__ = [
    "AsyncChallengeAugmenter",
    "AsyncChallenger",
    "ChallengeAugmenter",
    "Challenger",
]

#
# Type variables
#
# Naming convention used here:
# _ret for covariant type variables used in return positions
# _arg for contravariant type variables used in argument positions

T_Challenge_arg = TypeVar("T_Challenge_arg", bound=Challenge, contravariant=True)
T_Challenge_ret = TypeVar("T_Challenge_ret", bound=Challenge, covariant=True)


class Challenger(
    LabelingProducer[T_Challenge_ret],
    Generic[T_Challenge_ret],
    metaclass=ABCMeta,
):
    """
    Generates challenges that target the same failure modes.
    """


class AsyncChallenger(
    Challenger[T_Challenge_ret],
    AsyncProducer[T_Challenge_ret],
    Generic[T_Challenge_ret],
    metaclass=ABCMeta,
):
    """
    A challenger for use with asynchronous I/O.
    """


class ChallengeAugmenter(
    LabelingTransformer[T_Challenge_arg, T_Challenge_ret],
    Generic[T_Challenge_arg, T_Challenge_ret],
    metaclass=ABCMeta,
):
    """
    Augments challenges.
    """

    @final
    def transform(self, source_product: T_Challenge_arg) -> Iterator[T_Challenge_ret]:
        """
        Augment the given challenge.

        :param source_product: the challenge to augment
        :return: the augmented challenge
        """
        for augmented in self.augment(source_product):
            augmented.precursor = source_product
            yield augmented

    @abstractmethod
    def augment(self, original_challenge: T_Challenge_arg) -> Iterator[T_Challenge_ret]:
        """
        Augment the given challenge, yielding one or more augmented challenges.

        This challenge augmenter will set the precursor of all augmented challenges to
        the given challenge.

        :param original_challenge: the challenge to augment
        :return: the augmented challenge
        """


class AsyncChallengeAugmenter(
    AsyncTransformer[T_Challenge_arg, T_Challenge_ret],
    Generic[T_Challenge_arg, T_Challenge_ret],
    metaclass=ABCMeta,
):
    """
    A challenge transformer for use with asynchronous I/O.
    """

    @final
    async def atransform(
        self, source_product: T_Challenge_arg
    ) -> AsyncIterator[T_Challenge_ret]:
        """
        Asynchronously augment the given challenge.

        :param source_product: the challenge to augment
        :return: the augmented challenge
        """
        async for augmented in self.aaugment(source_product):
            augmented.precursor = source_product
            yield augmented

    @abstractmethod
    def aaugment(
        self, original_challenge: T_Challenge_arg
    ) -> AsyncIterator[T_Challenge_ret]:
        """
        Asynchronously augment the given challenge, yielding one or more augmented
        challenges.

        This challenge augmenter will set the precursor of all augmented challenges to
        the given original challenge.

        :param original_challenge: the challenge to augment
        :return: the augmented challenge
        """
