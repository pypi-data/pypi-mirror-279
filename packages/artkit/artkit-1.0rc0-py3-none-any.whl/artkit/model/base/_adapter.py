"""
Implementation of CachedLLM.
"""

from __future__ import annotations

import json
import logging
import math
import os
import time
from abc import ABCMeta, abstractmethod
from collections.abc import Iterator, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import AbstractSet, Any, Generic, TypeVar, cast, final

from pytools.api import appenddoc, deprecated, inheritdoc

from ..cache import CacheDB
from ._model import GenAIModel

log = logging.getLogger(__name__)

__all__ = [
    "CachedGenAIModel",
    "GenAIModelAdapter",
    "LegacyCachedGenAIModel",
]

#
# Type variables
#
# Naming convention used here:
# _ret for covariant type variables used in return positions
# _arg for contravariant type variables used in argument positions

T_GenAIModel_ret = TypeVar("T_GenAIModel_ret", bound=GenAIModel, covariant=True)
T_ModelOutput = TypeVar("T_ModelOutput")


#
# Constants
#


DURATION_MS = 2**-20


#
# Classes
#


@inheritdoc(match="""[see superclass]""")
class GenAIModelAdapter(GenAIModel, Generic[T_GenAIModel_ret], metaclass=ABCMeta):
    """
    A wrapper for a Gen AI system that changes the wrapped LLM system's behavior.

    This is useful for adding functionality to an LLM system without modifying
    its implementation.
    """

    #: The LLM system to wrap.
    model: T_GenAIModel_ret

    def __init__(self, model: T_GenAIModel_ret) -> None:
        """
        :param model: the LLM system to delegate to
        """
        self.model = model

    @property
    @final
    def model_id(self) -> str:
        """[see superclass]"""
        return self.model.model_id

    @final
    def get_model_params(self) -> Mapping[str, Any]:
        """[see superclass]"""
        return self.model.get_model_params()


class CachedGenAIModel(
    GenAIModelAdapter[T_GenAIModel_ret],
    Generic[T_GenAIModel_ret, T_ModelOutput],
    metaclass=ABCMeta,
):
    """
    A wrapper for a Gen AI model that caches responses.

    This is useful for lowering the number of requests to a GenAI model thus reducing
    costs and improving performance, both for testing and for production where
    prompts may be reused, e.g., for generating or augmenting test prompts for
    evaluating a GenAI system.

    The cache is stored in a database.
    """

    #: A mapping of cached system prompts to user prompts to responses.
    cache: CacheDB

    @appenddoc(to=GenAIModelAdapter.__init__)
    def __init__(
        self,
        model: T_GenAIModel_ret,
        *,
        database: Path | str,
    ) -> None:
        """
        :param database: the path to a cache database file, or ``":memory:"`` for an
            in-memory database
        :raises TypeError: if the LLM chat system to be cached is an adapter
        """
        super().__init__(model)
        if isinstance(model, GenAIModelAdapter) and not isinstance(
            # We allow wrapping a legacy cache so that we can carry over the cache
            # contents
            model,
            LegacyCachedGenAIModel,
        ):
            raise TypeError(
                "Caching is only supported for original LLM chat systems, but instead "
                f"got adapted llm of type {type(model)}"
            )

        self.cache = CacheDB(database=database)

    def _get(
        self,
        *,
        prompt: str,
        **model_params: str | int | float | None,
    ) -> list[str] | None:
        """
        Get the cached item for a given prompt.

        :param model_id: the model identifier
        :param prompt: the prompt for which to retrieve the cached responses
        :param model_params: additional model parameters associated with the prompt
        :return: the cached responses, or ``None`` if the prompt is not in the cache
        """
        # First get the value from the cache, to ensure it exists
        return self.cache.get_entry(
            model_id=self.model_id,
            prompt=prompt,
            **{k: _simplify_type(v) for k, v in model_params.items() if v is not None},
        )

    def _put(
        self,
        *,
        prompt: str,
        responses: list[str],
        **model_params: str | int | float | None,
    ) -> list[str]:
        """
        Update the cache with a response or list of responses for a given prompt.

        :param model_id: the identifier of the model that generated the responses
        :param prompt: the prompt for which the responses were generated
        :param responses: the responses to store in the cache
        :param model_params: additional model parameters associated with the prompt
        """
        self.cache.add_entry(
            model_id=self.model_id,
            prompt=prompt,
            responses=responses,
            **{k: _simplify_type(v) for k, v in model_params.items() if v is not None},
        )
        return responses

    def clear_cache(
        self,
        *,
        created_before: datetime | None = None,
        accessed_before: datetime | None = None,
    ) -> None:
        """
        Evict cached responses before or after a certain time threshold.

        :param created_before: if specified, only evict cached responses created before
            this time
        :param accessed_before: if specified, only evict cached responses last accessed
            before this time
        """
        self.cache.clear(
            model_id=self.model_id,
            created_before=created_before,
            accessed_before=accessed_before,
        )


class LegacyCachedGenAIModel(
    GenAIModelAdapter[T_GenAIModel_ret],
    Generic[T_GenAIModel_ret, T_ModelOutput],
    metaclass=ABCMeta,
):  # pragma: no cover
    """
    .. caution::

        This class is deprecated and will be removed in a future version.
        Use :class:`.CachedGenAIModel` instead.

    A wrapper for a GenAI model that caches responses.

    This is useful for testing and debugging, lowering the number of requests to the
    Gen AI model thus reducing costs and improving performance.

    The cache is stored in memory. Upon creation, cache contents can optionally be
    loaded from a JSON file. Calling method :meth:`save_cache` writes the cache
    back to the same file after use.

    The cache tracks the most recent access time of each cached response, and can
    evict responses before or after a certain time threshold. This is useful for
    removing old responses from the cache, or to "forget" recent responses during
    testing or debugging.

    Note that time stamps are not persisted in the cache file. When the cache is
    loaded from a file, all responses are considered to have been accessed at the
    time of loading.
    """

    #: A mapping of cached system prompts to user prompts to responses.
    _cache: dict[tuple[str, ...], T_ModelOutput]

    #: An ordered dictionary mapping cache keys to time stamps; used for cache eviction;
    #: the time stamps are integers representing seconds since the epoch
    _timestamps: dict[tuple[str, ...], float]

    #: A file path to store the cache (optional)
    cache_path: Path | None

    @deprecated(message="use the matching subclass of CachedGenAIModel instead")
    @appenddoc(to=GenAIModelAdapter.__init__)
    def __init__(
        self,
        model: T_GenAIModel_ret,
        cache_path: Path | str | None = None,
    ) -> None:
        """
        :param cache_path: the path to a cache file (optional)
        :raises TypeError: if the LLM chat system to be cached is an adapter
        """
        super().__init__(model)
        if isinstance(model, GenAIModelAdapter):
            raise TypeError(
                "Caching is only supported for original LLM chat systems, but instead "
                f"got adapted llm of type {type(model)}"
            )

        self.cache_path = (
            cache_path
            if cache_path is None or isinstance(cache_path, Path)
            else Path(cache_path)
        )

        # Load the cache from the file
        self._cache = cache = self._nested_to_flat(self._load_cache())
        timestamps: dict[tuple[str, ...], float] = {}
        self._timestamps = timestamps
        if cache:
            # The cache is not empty, so initialize the timestamps
            now = int(time.time())
            for key in cache.keys():
                timestamps[key] = now

    @abstractmethod
    def _get_n_levels(self) -> int:
        """
        Get the number of levels in this cache; this is also the number of strings in
        the cache key.

        :return: the number of levels in the cache
        """

    def _load_cache(self) -> dict[str, Any]:
        """
        Load the cache from a file.
        """
        cache_path = self.cache_path
        if cache_path is not None and os.path.exists(cache_path):
            with open(cache_path) as cache_file:
                return cast(dict[str, Any], json.load(cache_file))
        else:
            return {}

    def save_cache(self) -> None:
        """
        Save the cache to a file as json.
        """
        if self.cache_path is None:
            raise OSError("No cache path specified")
        else:
            # Create the directory of the cache file if it does not exist
            dirname = os.path.dirname(self.cache_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            # Save the cache to the file
            with open(self.cache_path, "w") as cache_file:
                # We use a pretty-printed format for better readability
                json.dump(self._flat_to_nested(self._cache), cache_file, indent=2)

    def _get(self, *key: str) -> T_ModelOutput:
        """
        Get the cached item for a key composed of one or more strings.

        :param key: the components of the key to retrieve from the cache; must match
            the number of levels in the cache (see :attr:`n_levels`)
        :return: the cached responses, or ``None`` if the key is not in the cache
        """
        # First get the value from the cache, to ensure it exists
        value = self._cache[key]
        # Update the timestamp for the key
        self._timestamps[key] = time.time()
        # Return the value
        return value

    def _put(self, *key: str, value: T_ModelOutput) -> None:
        """
        Update the cache with a new value for a key composed of one or more strings.

        :param key: the components of the key to retrieve from the cache; must match
            the number of levels in the cache (see :attr:`n_levels`)
        :param value: the new value to store in the cache
        """
        self._cache[key] = value
        self._timestamps[key] = time.time()

    @property
    def current_timestamp(self) -> float:
        """
        The current timestamp, in seconds since the epoch; waits for ~1 µs to ensure
        a new timestamp.
        """
        # Wait for a tiny amount of time to ensure a new timestamp
        time.sleep(DURATION_MS)
        return time.time()

    def clear_cache(
        self,
        *,
        before: float | None = None,
        after: float | None = None,
    ) -> None:
        """
        Evict cached responses before or after a certain time threshold.

        :param before: the time, expressed in seconds before the current
            time, before which to evict cached responses (optional)
        :param after: the time, expressed in seconds before the current
            time, after which to evict cached responses (optional)
        """
        if before is None and after is None:
            return

        earliest: float = before or 0
        latest: float = after or math.inf

        cache = self._cache
        timestamps = self._timestamps

        for key, timestamp in list(
            # We use list() to avoid modifying the dictionary while iterating over it
            timestamps.items()
        ):
            if not (earliest <= timestamp <= latest):
                del cache[key]
                del timestamps[key]

    def _nested_to_flat(
        self, d: dict[str, Any]
    ) -> dict[tuple[str, ...], T_ModelOutput]:
        """
        Pack a nested dictionary with the given number of levels into a flat dictionary,
        with keys as tuples of strings composed of the nested dictionary keys.

        :param d: the nested dictionary
        :return: the flat dictionary
        """

        n_levels = self._get_n_levels()

        def _unpack(
            sub: dict[str, Any], level: int
        ) -> Iterator[tuple[tuple[str, ...], T_ModelOutput]]:
            if level == 0:
                return (
                    ((key,), value)
                    for key, value in cast(dict[str, T_ModelOutput], sub).items()
                )
            else:
                return (
                    ((head, *tail), value)
                    for head, sub_dict in sub.items()
                    for tail, value in _unpack(sub_dict, level - 1)
                )

        return dict(_unpack(d, n_levels - 1))

    @staticmethod
    def _flat_to_nested(d: dict[tuple[str, ...], T_ModelOutput]) -> dict[str, Any]:
        """
        Unpack a flat dictionary into a nested dictionary.

        :param d: the flat dictionary
        :return: the nested dictionary
        """
        nested_dict: dict[str, Any] = {}

        def _add_to_dict(
            sub_dict: dict[str, Any], key_: Sequence[str], value_: T_ModelOutput
        ) -> None:
            head, *tail = key_
            if not tail:
                sub_dict[head] = value_
            else:
                _add_to_dict(sub_dict.setdefault(head, {}), tail, value_)

        for key, value in d.items():
            _add_to_dict(nested_dict, key, value)

        return nested_dict


#
# Auxiliary functions
#


def _simplify_type(value: Any) -> str | int | float | bool:
    """
    Ensure that the given value is a string, integer, float, or boolean.

    If the value is not one of these types, it is converted to a string.

    :param value: the value to check and potentially convert
    :return: the value, potentially converted to a string
    """
    if isinstance(value, (str, int, float, bool)):
        return value
    elif isinstance(value, AbstractSet):
        return str(set(map(_simplify_type, value)))
    elif isinstance(value, Mapping):
        # Convert the dictionary to a string representation that is independent of the
        # order of the dictionary's keys
        return str(
            dict(
                sorted((_simplify_type(k), _simplify_type(v)) for k, v in value.items())
            )
        )
    elif isinstance(value, list):
        return str(list(map(_simplify_type, value)))
    elif isinstance(value, tuple):
        return str(tuple(map(_simplify_type, value)))
    else:
        return str(value)
