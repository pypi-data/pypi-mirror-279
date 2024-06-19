"""
Implementation of the evaluation base classes.
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from typing import Any, Generic, TypeVar, cast

from fluxus.lineage import HasLineage

from pytools.api import as_tuple, inheritdoc
from pytools.expression import HasExpressionRepr
from pytools.repr import HasDictRepr

from ...response import Response

log = logging.getLogger(__name__)

__all__ = [
    "AggregateEvaluation",
    "Evaluation",
    "ResponseEvaluation",
]

#
# Type variables
#
# Naming convention used here:
# _ret for covariant type variables used in return positions
# _arg for contravariant type variables used in argument positions

T_Evaluation_ret = TypeVar("T_Evaluation_ret", bound="Evaluation[Any]", covariant=True)
T_Precursor_ret = TypeVar("T_Precursor_ret", bound=HasLineage[Any], covariant=True)

#
# Classes
#


class Evaluation(
    HasLineage[T_Precursor_ret],
    HasDictRepr,
    Generic[T_Precursor_ret],
    metaclass=ABCMeta,
):
    """
    The result of evaluating one or more challenges for a given failure mode.
    """

    @property
    def product_name(self) -> str:
        """[see superclass]"""
        return Evaluation.__name__

    @property
    @abstractmethod
    def failure_mode(self) -> str:
        """
        The failure mode that this evaluation is for.
        """


@inheritdoc(match="""[see superclass]""")
class ResponseEvaluation(Evaluation[Response[Any]], metaclass=ABCMeta):
    """
    The result of evaluating a single LLM response to a challenge.
    """

    #: The response that was evaluated.
    response: Response[Any]

    #: The failure mode that this evaluation is for.
    _failure_mode: str

    def __init__(self, *, response: Response[Any], failure_mode: str) -> None:
        """
        :param response: the response that was evaluated
        :param failure_mode: the failure mode that this evaluation is for
        """
        self.response = response
        self._failure_mode = failure_mode

    @property
    def failure_mode(self) -> str:
        """[see superclass]"""
        return self._failure_mode

    @property
    def precursor(self) -> Response[Any]:
        """[see superclass]"""
        return self.response


class AggregateEvaluation(
    HasExpressionRepr, Generic[T_Evaluation_ret], metaclass=ABCMeta
):
    """
    An evaluation that aggregates multiple evaluations.

    This abstract base class represents aggregate evaluations of one or more responses
    to a single challenge.

    All constituent evaluations of this aggregation are guaranteed to have the same
    failure mode and challenge category, which may also be higher up in the respective
    taxonomy.

    """

    #: The evaluations aggregated by this evaluation.
    evaluations: tuple[T_Evaluation_ret, ...]

    def __init__(self, evaluations: Iterable[T_Evaluation_ret]) -> None:
        """
        :param evaluations: the evaluations to be aggregated
        """
        super().__init__()

        evaluations_tuple = as_tuple(
            evaluations,
            element_type=cast(type[T_Evaluation_ret], Evaluation),
            arg_name="scored_evaluations",
        )

        if not evaluations_tuple:
            raise ValueError("At least one evaluation must be provided")

        self.evaluations = evaluations_tuple
