# noinspection GrazieInspection
"""
Implements a taxonomy of categories, along with two specific types of categories for the
two dimensions along which tests are organized:

- Challenge Categories: Different types of challenges that can be posed to an LLM
- Failure Modes: Different types of failure modes that an LLM can exhibit

The taxonomy is implemented as a tree of categories, where each category can have
subcategories.

Categories are implemented as a composite pattern, where the base class `Category` is
abstract and defines the interface for all categories, and the concrete categories
`ChallengeCategory` and `FailureMode` implement the interface and add specific
functionality.

The taxonomy is used to organize the challenges and failure modes that are used in the
evaluation of LLM systems.

As a simple example, code for creating a taxonomy of LLM failure modes could look like
this:

.. code-block:: python

    from artkit.core.taxonomy import FailureMode, Taxonomy

    # Create the taxonomy
    taxonomy = Taxonomy(
        FailureMode(
            name="Malicious use",
            description="The LLM is used for malicious purposes",
            children=[
                FailureMode(
                    name="Trolling",
                    description="Users aiming to provoke inappropriate LLM responses",
                ),
                FailureMode(
                    name="Hate speech",
                    description="Users aiming to generate hate speech",
                ),
                # …
            ],
        ),
        FailureMode(
            # …
        ),
        # …
    )
"""

from ._challenge_category import *
from ._failure_mode import *
