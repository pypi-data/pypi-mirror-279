"""
This legacy API Reference provides a detailed overview of ARTkit's original classes and
functions.

Key Pipeline Steps
------------------

1. Retrieve or generate challenges
2. Augment challenges (optional)
3. Interact with the target system
4. Evaluate interactions
5. Produce summary report

Overview of Modules
-------------------

Flow elements
~~~~~~~~~~~~~

- :mod:`legacy.challenge`: Contains the :class:`.Challenge` class and its
  subclasses, which represent the input to an LLM system.
- :mod:`legacy.persona`: Contains the :class:`.Persona` class and its subclasses,
  which represent the persona used to generate prompts and chat agents.
  Also implements a :class:`.PersonaAgent` class that can be used for automated
  interactions with a target LLM system.
- :mod:`artkit.response`: Implements the :class:`.Response` class and its subclasses,
  which represent the output of an LLM system.
- :mod:`legacy.evaluation`: Implements the :class:`.Evaluation` class and its
  subclasses, which represent the evaluation of an LLM system's response to a challenge.
- :mod:`legacy.report`: Implements the :class:`.Reporter` class, which is used
  to report on the results of an evaluation.

Supporting elements
~~~~~~~~~~~~~~~~~~~

- :mod:`artkit.model.llm`: Contains the :class:`ChatModel` class, which represents
  an LLM system used to generate text items.
- :mod:`artkit.util`: Contains utility classes and functions used throughout the
  library.
- :mod:`artkit.test`: Contains the tests for the library.

Core elements
~~~~~~~~~~~~~

- :mod:`fluxus`: Implements classes for the flow of data through the
  testing pipeline, including the `Flow` class and a class hierarchy for `conduits`
  that make up the elements of the flow, including producers, transformers, consumers,
  and groups of concurrent conduits.
"""

__version__ = "0.1.0"
