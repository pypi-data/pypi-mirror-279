"""
Implementation of the evaluation classes.
"""

import logging
from enum import IntEnum
from typing import Any

from pytools.api import appenddoc, inheritdoc
from pytools.expression import Expression
from pytools.expression.atomic import Id

from ..response import Response
from .base import AggregateEvaluation, ResponseEvaluation

log = logging.getLogger(__name__)

__all__ = [
    "AggregateScoredEvaluation",
    "Score",
    "ScoredEvaluation",
]


#
# Classes
#


class Score(IntEnum):
    """
    A score for a particular failure mode of a challenge.
    """

    #: The LLM system failed to meet the challenge.
    Fail = 1
    #: The LLM system failed to meet the challenge, but not as severely as a Fail.
    WeakFail = 2
    #: The LLM system met the challenge.
    Pass = 3


class ScoredEvaluation(ResponseEvaluation):
    """
    An evaluation with a score ranging from 1 (fail) to 3 (pass).
    """

    #: The score of the response; this is an integer ranging from 1 (fail) to 3 (pass).
    score: Score

    @appenddoc(to=ResponseEvaluation.__init__, prepend=True)
    def __init__(
        self,
        score: Score | int,
        *,
        response: Response[Any],
        failure_mode: str,
    ) -> None:
        """
        :param score: the score of the response; this is an integer ranging from
            1 (fail) to 3 (pass)
        """
        super().__init__(
            response=response,
            failure_mode=failure_mode,
        )

        # Score may be an int instance not Score - make sure we have a Score object.
        # This will also check that the score is within the valid range.
        self.score = score if isinstance(score, Score) else Score(score)


@inheritdoc(match="[see superclass]")
class AggregateScoredEvaluation(AggregateEvaluation[ScoredEvaluation]):
    """
    An aggregation of multiple scored evaluations.

    This is useful when multiple evaluators are used to evaluate a single response.

    Aggregates scores into a failure rate, which is the number of failed evaluations
    divided by the total number of evaluations.

    We distinguish a weak failure rate from a strong failure rate, where a weak failure
    rate does not include weak failures in the numerator. By this definition, the weak
    failure rate is never greater than the strong failure rate.
    """

    @property
    def failure_rate(self) -> float:
        """
        The strong failure rate of the scored evaluations.

        This is the number of failed evaluations divided by the total number of
        evaluations.
        """
        return sum(e.score != Score.Pass for e in self.evaluations) / len(
            self.evaluations
        )

    @property
    def weak_failure_rate(self) -> float:
        """
        The weak failure rate of the scored evaluations.

        This is the number of failed evaluations divided by the total number of
        evaluations, excluding weak failures from the numerator.
        """
        return sum(e.score == Score.Fail for e in self.evaluations) / len(
            self.evaluations
        )

    def __str__(self) -> str:
        return f"{self.failure_rate:.2%} failure rate"

    def to_expression(self) -> Expression:
        """[see superclass]"""
        return Id(type(self))[
            dict(
                failure_rate=self.failure_rate, weak_failure_rate=self.weak_failure_rate
            ),
        ]
