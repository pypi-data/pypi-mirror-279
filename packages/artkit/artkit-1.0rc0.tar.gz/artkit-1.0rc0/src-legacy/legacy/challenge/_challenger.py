"""
Implementations of challenge producers.
"""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator, Iterable, Iterator
from typing import Generic, TypeVar, cast

import aiofiles
from fluxus import AsyncProducer

from pytools.api import appenddoc, as_tuple
from pytools.typing import get_common_generic_base

from .base import Challenge, Challenger

log = logging.getLogger(__name__)

__all__ = [
    "FixedChallenger",
    "JSONLChallengeLoader",
]

#
# Type variables
#

T_Challenge_ret = TypeVar(
    "T_Challenge_ret",
    bound="Challenge",
    # this is a covariant type variable because we use it in a return position
    covariant=True,
)


T_Challenge = TypeVar("T_Challenge", bound="Challenge")


class FixedChallenger(Challenger[T_Challenge], Generic[T_Challenge]):
    """
    A challenge source that provides challenges from a fixed iterable
    provided at instantiation.
    """

    # The challenges to provide
    challenges: tuple[T_Challenge, ...]

    # The type of challenges in this challenger
    _product_type: type[T_Challenge]

    def __init__(self, challenges: Iterable[T_Challenge]) -> None:
        """
        :param challenges: the challenges to provide
        """

        super().__init__()

        self.challenges = challenges = as_tuple(
            challenges,
            element_type=cast(type[T_Challenge], Challenge),
            arg_name="challenges",
        )

        self._product_type = get_common_generic_base(
            type(challenge) for challenge in challenges
        )

    @property
    def product_type(self) -> type[T_Challenge]:
        """[see superclass]"""
        return self._product_type

    def produce(self) -> Iterator[T_Challenge]:
        """
        Yield each challenge from the list of challenges.

        :return: an async iterable of challenges
        """
        yield from self.challenges


class JSONLChallengeLoader(
    Challenger[T_Challenge_ret],
    AsyncProducer[T_Challenge_ret],
    Generic[T_Challenge_ret],
):
    """
    A challenge source that loads challenges from a jsonl file.
    """

    # The path to a file containing serialized challenges
    path: str

    #: The common type of challenges to expect in the file
    challenge_type: type[T_Challenge_ret]

    @appenddoc(to=Challenger.__init__, prepend=True)
    def __init__(self, path: str, *, challenge_type: type[T_Challenge_ret]) -> None:
        """
        :param path: the path to a file containing serialized challenges
        :param challenge_type: the common type of challenges to expect in the file
        """
        self.path = path
        self.challenge_type = challenge_type

    async def aproduce(self) -> AsyncIterator[T_Challenge_ret]:
        """
        Yield challenges from a jsonl file.

        :return: an async iterable of challenges
        """
        async with aiofiles.open(self.path, "r") as file:
            async for line in file:
                challenge = Challenge.from_dict(json.loads(line.strip()))
                if not isinstance(challenge, self.challenge_type):
                    raise TypeError(
                        f"Expected challenge of type {self.challenge_type}, "
                        f"but got {challenge}"
                    )
                yield challenge
