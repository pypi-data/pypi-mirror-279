"""
Implementation of ``LLMResponder``.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator

from artkit.model.llm.base import ChatModel
from pytools.api import appenddoc, inheritdoc

from ..challenge.base import Challenge
from ._response import SingleTurnResponse
from .base import AsyncResponder, Responder

log = logging.getLogger(__name__)

__all__ = [
    "LLMResponder",
]


#
# Classes
#


@inheritdoc(match="[see superclass]")
class LLMResponder(AsyncResponder[Challenge, SingleTurnResponse[Challenge]]):
    """
    Uses an LLM to get responses to challenges from a challenge producer.
    """

    #: The LLM system with which to generate responses.
    llm: ChatModel

    @appenddoc(to=Responder.__init__)
    def __init__(
        self,
        *,
        llm: ChatModel,
    ) -> None:
        """
        :param llm: the LLM system with which to generate responses
        """
        super().__init__()
        self.llm = llm

    async def arespond(
        self, challenge: Challenge
    ) -> AsyncIterator[SingleTurnResponse[Challenge]]:
        """[see superclass]"""

        response: str

        for response in await self.llm.get_response(message=challenge.prompt):
            yield SingleTurnResponse(
                message=response,
                challenge=challenge,
            )
