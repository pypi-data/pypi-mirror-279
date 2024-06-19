"""
Implementation of the evaluation base classes.
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from collections.abc import AsyncIterator, Iterator
from typing import Any, Generic, TypeVar, final

from fluxus import AsyncTransformer, Transformer

from ...response import Response
from ._evaluation import Evaluation

log = logging.getLogger(__name__)

__all__ = [
    "AsyncEvaluator",
    "Evaluator",
]

#
# Type variables
#
# Naming convention used here:
# _ret for covariant type variables used in return positions
# _arg for contravariant type variables used in argument positions

T_Evaluation_ret = TypeVar("T_Evaluation_ret", bound=Evaluation[Any], covariant=True)
T_Response_arg = TypeVar("T_Response_arg", bound=Response[Any], contravariant=True)


class Evaluator(
    Transformer[T_Response_arg, T_Evaluation_ret],
    Generic[T_Response_arg, T_Evaluation_ret],
    metaclass=ABCMeta,
):
    """
    An abstract base class for evaluating LLM systems.
    """

    @final
    def transform(self, source_product: T_Response_arg) -> Iterator[T_Evaluation_ret]:
        """
        Generate one or more evaluations for the given response, deferring to
        :meth:`evaluate`.

        :param source_product: the response to evaluate
        :return: the evaluations for the response, as an evaluation bundle
        """
        return self.evaluate(source_product)

    @abstractmethod
    def evaluate(self, response: T_Response_arg) -> Iterator[T_Evaluation_ret]:
        """
        Evaluate a response and return an evaluation bundle.

        :param response: the response to evaluate
        :return: the evaluation bundle
        """


class AsyncEvaluator(
    AsyncTransformer[T_Response_arg, T_Evaluation_ret],
    Generic[T_Response_arg, T_Evaluation_ret],
    metaclass=ABCMeta,
):
    """
    An abstract base class for evaluating LLM systems asynchronously.
    """

    @final
    def atransform(
        self, source_product: T_Response_arg
    ) -> AsyncIterator[T_Evaluation_ret]:
        """
        Generate one or more evaluations for the given response, deferring to
        :meth:`evaluate`.

        :param source_product: the response to evaluate
        :return: the evaluations for the response, as an evaluation bundle
        """
        return self.aevaluate(source_product)

    @abstractmethod
    def aevaluate(self, response: T_Response_arg) -> AsyncIterator[T_Evaluation_ret]:
        """
        Evaluate a response and return an evaluation bundle.

        :param response: the response to evaluate
        :return: the evaluation bundle
        """
