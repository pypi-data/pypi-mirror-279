"""
Abstract base classes for LLM evaluations and evaluators.

Evaluations are the results of evaluating an LLM system's response to a challenge.
Each evaluation is associated with a specific failure mode.
Multiple evaluations can be aggregated by response, across responses, and across
the failure mode taxonomy.
These different aggregation steps make it easier to implement summaries and drill-downs
of evaluations.
Different abstract classes represent these different aggregation levels:

- :class:`ResponseEvaluation`: an evaluation of a single response
- :class:`AggregateEvaluation`: an aggregation of multiple evaluations

The abstract base class of all of these is :class:`Evaluation`.


Evaluators are classes that evaluate LLM systems.
"""

from ._evaluation import *
from ._evaluator import *
from ._llm import *
