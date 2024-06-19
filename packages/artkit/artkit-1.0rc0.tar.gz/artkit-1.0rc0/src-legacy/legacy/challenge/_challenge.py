"""
Common types of LLM challenges.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TypeVar

from pytools.api import as_tuple, inheritdoc
from pytools.meta import SingletonABCMeta

from .base import Challenge

__all__ = [
    "EmptyChallenge",
    "MultiPromptChallenge",
    "MultipleChoiceChallenge",
    "PromptChallenge",
    "QnAChallenge",
]


#
# Type variables
#

T_Challenge = TypeVar("T_Challenge", bound=Challenge)


#
# Classes
#


@inheritdoc(match="""[see superclass]""")
class EmptyChallenge(Challenge, metaclass=SingletonABCMeta):
    """
    An empty challenge.

    Useful for flows that evaluate responses that have not been generated within
    the flow, or for which no challenge can be specified.
    """

    @property
    def prompt(self) -> str:
        """[see superclass]"""
        return ""

    def __eq__(self, other: Any) -> bool:
        return self is other

    def __hash__(self) -> int:
        return id(self)


@inheritdoc(match="""[see superclass]""")
class PromptChallenge(Challenge):
    """
    A basic challenge, consisting of a prompt.

    This is the most basic test case for an LLM system.
    """

    def __init__(self, prompt: str) -> None:
        """
        :param prompt: the prompt of the challenge
        """
        super().__init__()
        self._prompt = prompt

    @property
    def prompt(self) -> str:
        """[see superclass]"""
        return self._prompt

    def __eq__(self, other: Any) -> bool:
        return type(self) is type(other) and self.prompt == other.prompt

    def __hash__(self) -> int:
        return hash(self.prompt)


@inheritdoc(match="""[see superclass]""")
class QnAChallenge(Challenge):
    """
    A question-and-answer challenge.

    Typically used for factuality tests.
    """

    def __init__(self, prompt: str, *, expected_answer: str) -> None:
        """
        :param prompt: the prompt of the challenge
        :param expected_answer: the expected answer to the prompt
        """
        super().__init__()
        self._prompt = prompt
        self._expected_answer = expected_answer

    @property
    def prompt(self) -> str:
        """[see superclass]"""
        return self._prompt

    @property
    def expected_answer(self) -> str:
        """
        The expected answer to the prompt.
        """
        return self._expected_answer

    def __eq__(self, other: Any) -> bool:
        return (
            type(self) is type(other)
            and self.prompt == other.prompt
            and self.expected_answer == other.expected_answer
        )

    def __hash__(self) -> int:
        return hash((self.prompt, self.expected_answer))


@inheritdoc(match="""[see superclass]""")
class MultipleChoiceChallenge(Challenge):
    """
    A multiple-choice challenge.

    Typically used for factuality tests.
    """

    def __init__(
        self, prompt: str, *, choices: Iterable[str], correct_choice: str
    ) -> None:
        """
        :param prompt: the prompt of the challenge
        :param choices: the list of possible choices
        :param correct_choice: the correct choice
        """
        super().__init__()
        self._prompt = prompt
        self._choices = as_tuple(choices, element_type=str, arg_name="choices")
        self._correct_choice = correct_choice

    @property
    def prompt(self) -> str:
        """[see superclass]"""
        return self._prompt

    @property
    def choices(self) -> tuple[str, ...]:
        """
        The list of possible choices.
        """
        return self._choices

    @property
    def correct_choice(self) -> str:
        """
        The correct choice.
        """
        return self._correct_choice

    def __eq__(self, other: Any) -> bool:
        return (
            type(self) is type(other)
            and self.prompt == other.prompt
            and self.choices == other.choices
            and self.correct_choice == other.correct_choice
        )

    def __hash__(self) -> int:
        return hash((self.prompt, self.choices, self.correct_choice))


class MultiPromptChallenge(Challenge):
    """
    A challenge consisting of multiple prompts, sent to the LLM system one by one.
    """

    #: The prompts.
    prompts: tuple[str, ...]

    def __init__(self, prompts: Iterable[str]) -> None:
        """
        :param prompts: one or more prompts that precede the main prompt
        """
        super().__init__()
        self.prompts = prompts = as_tuple(prompts, element_type=str, arg_name="prompts")
        if len(prompts) < 1:
            raise ValueError("At least one prompt is required")

    @property
    def prompt(self) -> str:
        """
        The main prompt, defined as the final prompt of this multi-prompt challenge.
        """
        return self.prompts[-1]

    @property
    def preamble(self) -> tuple[str, ...]:
        """
        The prompts preceding the main prompt.
        """
        return self.prompts[:-1]

    def __eq__(self, other: Any) -> bool:
        return (
            type(self) is type(other)
            and self.prompt == other.prompt
            and self.preamble == other.preamble
        )

    def __hash__(self) -> int:
        return hash((self.prompt, self.preamble))
