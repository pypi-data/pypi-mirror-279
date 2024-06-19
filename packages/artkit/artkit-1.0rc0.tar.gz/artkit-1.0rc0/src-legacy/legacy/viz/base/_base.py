"""
Implementation of visualization base classes.
"""

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod

import pandas as pd

from pytools.viz import DrawingStyle

log = logging.getLogger(__name__)

__all__ = [
    "EvaluationMatrix",
    "EvaluationMatrixStyle",
]


#
# CLasses
#
class EvaluationMatrix:
    """
    An aggregation of evaluations into a matrix, for use with
    :class:`.EvaluationMatrixDrawer`.
    """

    #: The evaluation matrix, with aggregated scores along dimensions in the rows and
    #: columns
    metrics: pd.DataFrame

    #: The number of groups we have in the rows
    n_groups_row: int

    #: The number of groups we have in the columns
    n_groups_col: int

    #: The individual evaluations associated with each cell in the matrix, with the
    #: index corresponding to the combined levels of the row and column indices
    #: of the evaluation matrix; only required for interactive styles (optional)
    drilldown: pd.DataFrame | None

    def __init__(
        self,
        metrics: pd.DataFrame,
        *,
        n_groups_row: int,
        n_groups_column: int,
        drilldown: pd.DataFrame | None = None,
    ) -> None:
        """
        :param metrics: the evaluation metrics, organised in a matrix
        :param n_groups_row: the number of groups in the matrix rows
        :param n_groups_column: the number of groups in the matrix columns
        :param drilldown: the individual evaluations associated with each cell in the
            matrix; only required for interactive styles (optional)
        """
        self.metrics = metrics
        self.n_groups_row = n_groups_row
        self.n_groups_col = n_groups_column
        self.drilldown = drilldown

        # Check that the indicated number of groups matches the number of index levels
        # in the metrics matrix
        assert metrics.index.nlevels == max(n_groups_row, 1) and n_groups_row >= 0, (
            f"The number of index levels in the matrix must match the number of "
            f"groups in the rows, but got {metrics.index.nlevels} levels while "
            f"n_groups_row={n_groups_row}."
        )
        assert (
            metrics.columns.nlevels == max(n_groups_column, 1) and n_groups_column >= 0
        ), (
            f"The number of column levels in the matrix must match the number of "
            f"groups in the columns, but got {metrics.columns.nlevels} levels while "
            f"n_groups_col={n_groups_column}."
        )

        # Check that indices are compatible
        if drilldown is not None:
            assert isinstance(drilldown, pd.DataFrame), (
                "The drilldown table must be a DataFrame, but got a "
                f"{type(drilldown).__name__}"
            )
            # Ensure we have the correct number of index levels
            assert drilldown.index.nlevels == n_groups_row + n_groups_column, (
                "The number of index levels in the drilldown table must match the sum"
                f"of the index levels in the matrix, but got {drilldown.index.nlevels} "
                f"and {n_groups_row} + {n_groups_column}, "
                f"respectively."
            )


class EvaluationMatrixStyle(DrawingStyle, metaclass=ABCMeta):
    """
    A style for rendering evaluation matrices.
    """

    @property
    @abstractmethod
    def supports_drilldown(self) -> bool:
        """
        ``True`` if the style supports drilldown into individual evaluations and hence
        requires the evaluations to be provided in the :class:`EvaluationMatrix` object;
        ``False`` otherwise.
        """

    @abstractmethod
    def render_matrix(self, matrix: EvaluationMatrix) -> None:
        """
        Render an evaluation matrix as an HTML table for a Jupyter notebook.

        :param matrix: the evaluation matrix to render
        """
