"""
Implementation of ``StringMatchEvaluator``.
"""

import re
from collections.abc import Iterator
from typing import Any

from pytools.api import inheritdoc

from ..response import Response
from ._scored import Score, ScoredEvaluation
from .base import Evaluator

__all__ = [
    "StringMatchEvaluator",
]


@inheritdoc(match="""[see superclass]""")
class StringMatchEvaluator(Evaluator[Response[Any], ScoredEvaluation]):
    """
    An evaluator that determines success or failure by matching regular expressions in
    the messages of an LLM response.

    If any message in the response matches the success pattern, the evaluation passes.

    If an optional failure pattern is provided, the evaluator will first attempt to
    match the failure pattern. If the failure pattern is matched, the evaluation will
    report a failure. If neither the success pattern nor the failure pattern is matched,
    the evaluation will report a weak failure.
    """

    #: The pattern to match for success.
    success_pattern: re.Pattern[str]

    #: The pattern to match for failure.
    failure_pattern: re.Pattern[str] | None

    #: The failure mode for this evaluator.
    failure_mode: str

    def __init__(
        self,
        *,
        success_pattern: re.Pattern[str] | str,
        failure_pattern: re.Pattern[str] | str | None = None,
        failure_mode: str,
    ) -> None:
        """
        :param success_pattern: if matched, the evaluation will pass
        :param failure_pattern: if matched, the evaluation will fail (optional)
        :param failure_mode: the failure mode for this evaluator
        """
        self.success_pattern = (
            re.compile(success_pattern)
            if isinstance(success_pattern, str)
            else success_pattern
        )
        self.failure_pattern = (
            None
            if failure_pattern is None or isinstance(failure_pattern, re.Pattern)
            else re.compile(failure_pattern)
        )
        self.failure_mode = failure_mode

    def evaluate(self, response: Response[Any]) -> Iterator[ScoredEvaluation]:
        """[see superclass]"""
        yield ScoredEvaluation(
            score=self._evaluate(response),
            response=response,
            failure_mode=self.failure_mode,
        )

    def _evaluate(self, response: Response[Any]) -> Score:
        """
        Evaluate the response and return a score indicating a pass, weak failure, or
        failure.

        :param response: the response to evaluate
        :return: a score
        """

        failure_pattern = self.failure_pattern

        # If the failure pattern is defined, check for it first
        if failure_pattern and any(
            failure_pattern.search(message.text) for message in response.get_messages()
        ):
            return Score.Fail

        # If the success pattern is matched, return a pass
        elif any(
            self.success_pattern.search(message.text)
            for message in response.get_messages()
        ):
            return Score.Pass

        # If the success pattern was not matched we have no failure pattern, return
        # a failure
        elif failure_pattern is None:
            return Score.Fail

        # If the success pattern was not matched, and we have a failure pattern, return
        # a weak failure
        else:
            return Score.WeakFail
