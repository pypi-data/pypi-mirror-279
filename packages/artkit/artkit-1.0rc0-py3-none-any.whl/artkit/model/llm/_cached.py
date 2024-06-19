"""
Implementation of CachedLLM.
"""

from __future__ import annotations

import logging
from typing import Any, Generic, TypeVar

from pytools.api import inheritdoc

from ..base import CachedGenAIModel, LegacyCachedGenAIModel
from .base import ChatModel, ChatModelAdapter, CompletionModel, CompletionModelAdapter
from .history import ChatHistory, UserMessage

log = logging.getLogger(__name__)

__all__ = [
    "CachedCompletionModel",
    "CachedChatModel",
    "LegacyCachedChatModel",
    "LegacyCachedCompletionModel",
]

#
# Type variables
#
# Naming convention used here:
# _ret for covariant type variables used in return positions
# _arg for contravariant type variables used in argument positions

T_CompletionModel_ret = TypeVar(
    "T_CompletionModel_ret", bound=CompletionModel, covariant=True
)
T_ChatModel_ret = TypeVar("T_ChatModel_ret", bound=ChatModel, covariant=True)


@inheritdoc(match="""[see superclass]""")
class CachedCompletionModel(
    CachedGenAIModel[T_CompletionModel_ret, list[str]],
    CompletionModelAdapter[T_CompletionModel_ret],
    Generic[T_CompletionModel_ret],
):
    """
    A wrapper for a chat model, caching responses.

    This is useful for testing and in production where repeated requests to the model
    are made, thus reducing costs and improving performance.
    """

    async def get_completion(
        self, *, prompt: str, **model_params: dict[str, Any]
    ) -> str:
        """[see superclass]"""

        model_params_merged = {
            # Add the completion flag to the model params to avoid collisions with
            # chat models
            "_type": "completion",
            **self.get_model_params(),
            **model_params,
        }
        response: list[str] | None = self._get(prompt=prompt, **model_params_merged)

        if response is None:  # pragma: no cover
            return self._put(
                prompt=prompt,
                responses=[
                    await self.model.get_completion(prompt=prompt, **model_params)
                ],
                **model_params_merged,
            )[0]
        else:
            return response[0]


@inheritdoc(match="""[see superclass]""")
class LegacyCachedCompletionModel(
    LegacyCachedGenAIModel[T_CompletionModel_ret, str],
    CompletionModelAdapter[T_CompletionModel_ret],
    Generic[T_CompletionModel_ret],
):  # pragma: no cover
    """
    .. caution::

        This class is deprecated and will be removed in a future version.
        Use :class:`.CachedCompletionModel` instead.

    A wrapper for an LLM text generator that caches responses.

    This is useful for testing and debugging, lowering the number of requests to the LLM
    system thus reducing costs and improving performance.
    """

    async def get_completion(
        self, *, prompt: str, **model_params: dict[str, Any]
    ) -> str:
        """[see superclass]"""
        try:
            return self._get(prompt)
        except KeyError:
            return self._cache_response(
                prompt, await self.model.get_completion(prompt=prompt)
            )

    def _get_n_levels(self) -> int:
        """[see superclass]"""
        return 1

    def _cache_response(self, prompt: str, response: str) -> str:
        # Update the cache and return the response
        self._put(prompt, value=response)
        return response


@inheritdoc(match="""[see superclass]""")
class CachedChatModel(
    CachedGenAIModel[T_ChatModel_ret, list[str]],
    ChatModelAdapter[T_ChatModel_ret],
    Generic[T_ChatModel_ret],
):
    """
    A wrapper for a chat model, caching responses.

    This is useful for testing and in production where repeated requests to the model
    are made, thus reducing costs and improving performance.


    Example:

    .. code-block:: python

        import artkit.api as ak

        cached_openai_llm = ak.CachedChatModel(
            model=ak.OpenAIChat(model_id="gpt-3.5-turbo"),
            database="./cache/example_cache_gpt3.db"
        )
    """

    async def get_response(
        self,
        message: str,
        *,
        history: ChatHistory | None = None,
        **model_params: dict[str, Any],
    ) -> list[str]:
        """[see superclass]"""

        model_params_merged = {**self.get_model_params(), **model_params}
        # Add the chat flag to the model params to avoid collisions
        # with completion models

        # Add the system prompt and chat history to the model params
        # to ensure consistent caching behavior
        if self.system_prompt is not None:
            model_params_merged["_system_prompt"] = self.system_prompt
        if history is not None:
            for i, msg in enumerate(history.get_messages()):
                model_params_merged[f"_history_{i}"] = f"[{msg.role}]\n{msg.text}"

        response: list[str] | None = self._get(prompt=message, **model_params_merged)

        if response is None:  # pragma: no cover
            return self._put(
                prompt=message,
                responses=await self.model.get_response(
                    message, history=history, **model_params
                ),
                **model_params_merged,
            )
        else:
            return response


@inheritdoc(match="""[see superclass]""")
class LegacyCachedChatModel(
    LegacyCachedGenAIModel[T_ChatModel_ret, list[str]],
    ChatModelAdapter[T_ChatModel_ret],
    Generic[T_ChatModel_ret],
):  # pragma: no cover
    """
    .. caution::

        This class is deprecated and will be removed in a future version.
        Use :class:`.CachedChatModel` instead.

    A wrapper for an LLM system that caches responses.

    This approach is beneficial for testing and debugging, as it minimizes the number of
    requests to the LLM system, thereby reducing costs and enhancing performance.
    """

    def _get_n_levels(self) -> int:
        """[see superclass]"""
        return 2

    async def get_response(
        self,
        message: str,
        *,
        history: ChatHistory | None = None,
        **model_params: dict[str, Any],
    ) -> list[str]:
        """[see superclass]"""
        response = self._get_cached_response(message, history=history)

        if response is None:  # pragma: no cover
            return self._cache_response(
                message,
                history=history,
                response=await self.model.get_response(message, history=history),
            )
        else:
            return response

    @staticmethod
    def _make_cache_key(message: str, history: ChatHistory | None) -> str:
        # Convert the message and history into a key for the cache

        if history is None:
            # If no history is provided, use the message as the llm input
            return repr(message)
        else:
            # Otherwise, use the history and the message as the llm input,
            # as a list of role-text pairs, and the message as the concluding
            # user message.
            # These keys will be distinct from message-only keys, since we
            # use repr to escape special characters in the message and history,
            # and we use newline characters to separate the role-text pairs.
            return "\n".join(
                f"{message.role!r}:\n{message.text!r}"
                for message in (*history.messages, UserMessage(message))
            )

    def _cache_response(
        self, message: str, *, history: ChatHistory | None, response: list[str]
    ) -> list[str]:
        # Update the cache and return the response
        self._put(
            self.system_prompt or "",
            self._make_cache_key(message, history=history),
            value=response,
        )
        return response

    def _get_cached_response(
        self, message: str, history: ChatHistory | None
    ) -> list[str] | None:
        # Get the response from the cache, if it exists, else return None
        try:
            return self._get(
                self.system_prompt or "",
                self._make_cache_key(message, history=history),
            )
        except KeyError:
            return None
