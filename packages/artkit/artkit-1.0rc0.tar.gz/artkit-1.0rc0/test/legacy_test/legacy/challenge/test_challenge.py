import logging
from collections.abc import Iterator

import pytest

from legacy.challenge import (
    FixedChallenger,
    MultiPromptChallenge,
    MultipleChoiceChallenge,
    PromptChallenge,
    QnAChallenge,
)
from legacy.challenge.base import Challenge, ChallengeAugmenter

log = logging.getLogger(__name__)

#
# Constants
#


#
# Unit tests
#


def test_prompt_challenge() -> None:
    """
    Test the Challenge class.
    """

    # test the Challenge class
    challenge = PromptChallenge("prompt1").label(category="Persona")
    assert challenge.prompt == "prompt1"
    from_dict = PromptChallenge.from_dict(challenge.to_dict())
    assert from_dict == challenge
    assert hash(from_dict) == hash(challenge)


def test_qna_challenge() -> None:
    qna_challenge = QnAChallenge("prompt1", expected_answer="answer1").label(
        category="Persona"
    )
    assert qna_challenge.prompt == "prompt1"
    assert qna_challenge.expected_answer == "answer1"
    from_dict = QnAChallenge.from_dict(qna_challenge.to_dict())
    assert from_dict == qna_challenge
    assert hash(from_dict) == hash(qna_challenge)


def test_multi_step_challenge() -> None:
    multi_step_challenge = MultiPromptChallenge(
        prompts=["prompt1", "prompt2", "prompt_final"],
    ).label(category="Persona")
    assert multi_step_challenge.prompt == "prompt_final"
    assert multi_step_challenge.preamble == ("prompt1", "prompt2")
    from_dict = MultiPromptChallenge.from_dict(multi_step_challenge.to_dict())
    assert from_dict == multi_step_challenge
    assert hash(from_dict) == hash(multi_step_challenge)

    multi_step_challenge = MultiPromptChallenge(prompts=("prompt1",)).label(
        category="Persona"
    )
    assert multi_step_challenge.prompt == "prompt1"
    assert multi_step_challenge.preamble == ()
    assert hash(multi_step_challenge) == hash(
        MultiPromptChallenge(prompts=("prompt1",)).label(category="Persona")
    )

    with pytest.raises(ValueError):
        # ValueError is raised when no prompts are provided
        MultiPromptChallenge(prompts=()).label(category="Persona")


def test_multiple_choice_challenge() -> None:
    multiple_choice_challenge = MultipleChoiceChallenge(
        prompt="prompt1",
        choices=["choice1", "choice2"],
        correct_choice="choice1",
    ).label(category="Persona")
    assert multiple_choice_challenge.prompt == "prompt1"
    assert multiple_choice_challenge.choices == ("choice1", "choice2")
    assert multiple_choice_challenge.correct_choice == "choice1"
    from_dict = MultipleChoiceChallenge.from_dict(multiple_choice_challenge.to_dict())
    assert from_dict == multiple_choice_challenge
    assert hash(from_dict) == hash(multiple_choice_challenge)


def test_fixed_challenger() -> None:

    # test the FixedChallenger class
    challenges = [
        PromptChallenge("prompt1").label(category="Persona"),
        QnAChallenge(
            "prompt2",
            expected_answer="answer2",
        ).label(category="Persona"),
        MultiPromptChallenge(prompts=("prompt3", "prompt4")).label(category="Persona"),
        MultipleChoiceChallenge(
            prompt="prompt5",
            choices=("choice1", "choice2"),
            correct_choice="choice1",
        ).label(category="Persona"),
    ]
    challenger = FixedChallenger(challenges=challenges)
    assert challenger.challenges == tuple(challenges)
    assert challenger.product_type == Challenge

    # test the FixedChallenger class with a single challenge type
    assert (
        FixedChallenger(
            challenges=[PromptChallenge("prompt1"), PromptChallenge("prompt2")],
        ).product_type
        == PromptChallenge
    )

    # raise TypeError when a challenge does not implement the Challenge interface
    with pytest.raises(TypeError):
        FixedChallenger(  # type: ignore[type-var]
            challenges=[
                PromptChallenge("prompt1"),
                "prompt2",
            ],
        )


def test_challenge_transformer() -> None:
    """
    Test the ChallengeTransformer class.
    """

    class TestAugmenter(ChallengeAugmenter[QnAChallenge, PromptChallenge]):
        def augment(
            self, original_challenge: QnAChallenge
        ) -> Iterator[PromptChallenge]:
            yield PromptChallenge(original_challenge.prompt)

    challenge_original = QnAChallenge(
        "prompt1",
        expected_answer="answer1",
    )
    transformer = TestAugmenter()
    challenges_augmented = list(
        transformer.transform(challenge_original.label(category="QnA"))
    )
    assert len(challenges_augmented) == 1
    challenge_augmented = challenges_augmented[0]

    assert transformer.input_type == QnAChallenge
    assert transformer.product_type == PromptChallenge
    assert challenge_augmented == (
        PromptChallenge(
            prompt="prompt1",
        ).label(category="Persona")
    )

    lineage = challenge_augmented.get_lineage()
    assert len(lineage) == 2
    assert lineage[0] is challenge_original
    assert lineage[1] is challenge_augmented
