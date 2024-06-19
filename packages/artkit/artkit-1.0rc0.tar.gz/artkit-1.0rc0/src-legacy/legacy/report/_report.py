"""
Implementation of test suites.
"""

from __future__ import annotations

import io
import logging
from collections.abc import AsyncIterable, Callable, Iterable, Iterator
from types import FunctionType
from typing import Any, Literal, TypeAlias, TypeVar, cast

import pandas as pd
from fluxus import AsyncConsumer

from pytools.api import as_list, inheritdoc
from pytools.asyncio import iter_async_to_sync
from pytools.expression import Expression, HasExpressionRepr
from pytools.expression.atomic import Id
from pytools.viz import DrawingStyle, is_running_in_notebook

from ..evaluation import Score, ScoredEvaluation
from ..evaluation.base import Evaluation
from ..util import find_columns, products_to_frame

log = logging.getLogger(__name__)

__all__ = [
    "Reporter",
    "Report",
]


#
# Type variables
#
T_Evaluation = TypeVar("T_Evaluation", bound=Evaluation[Any])

#
# Type aliases
#

EvaluationMetric: TypeAlias = Literal["failure rate", "weak failure rate"]


class Report(HasExpressionRepr):
    """
    A matrix of evaluations along a taxonomy of challenge categories and a taxonomy of
    failure modes, retaining the context of each evaluation.

    See :class:`.AggregateScoredEvaluation` for more details on the failure rate
    evaluation metric.
    """

    #: The failure rate evaluation metric,
    #: see :attr:`.AggregateScoredEvaluation.failure_rate`.
    METRIC_FAILURE_RATE: EvaluationMetric = "failure rate"

    #: The weak failure rate evaluation metric,
    #: see :attr:`.AggregateScoredEvaluation.weak_failure_rate`.
    METRIC_WEAK_FAILURE_RATE: EvaluationMetric = "weak failure rate"

    #: The column name for the evaluation.
    COL_SCORE = ("Evaluation", "score")

    #: The evaluations in this report, each as a tuple of a numerical index and the
    #: scored evaluation, where the index indicates the unique path taken through the
    #: flow.
    evaluations: list[tuple[int, ScoredEvaluation]]

    #: The default list of fields to group by as rows in a reporting matrix.
    agg_rows: list[str | tuple[str, str]] | None

    #: The default list of fields to group by as columns in a reporting matrix.
    agg_columns: list[str | tuple[str, str]] | None

    def __init__(
        self,
        *,
        evaluations: Iterable[tuple[int, ScoredEvaluation]],
        agg_rows: list[str | tuple[str, str]] | None = None,
        agg_columns: list[str | tuple[str, str]] | None = None,
    ) -> None:
        """
        :param evaluations: the evaluations in this report, each as a tuple of a
            numerical index and the scored evaluation, where the index indicates the
            unique path taken through the flow
        """
        # Docstrings for the agg… parameters are added below from Reporter.__init__

        self.evaluations = as_list(
            evaluations,
            element_type=cast(type[tuple[int, ScoredEvaluation]], tuple),
            arg_name="evaluations",
        )
        self.agg_rows = agg_rows
        self.agg_columns = agg_columns

    def get_evaluations(self) -> Iterator[ScoredEvaluation]:
        """
        Yield the scored evaluations in this matrix, as an iterator.

        :return: the scored evaluations
        """
        return (evaluation for _, evaluation in self.evaluations)

    def to_expression(self) -> Expression:
        """
        Convert this evaluation matrix to an expression.

        :return: the expression representation of this evaluation matrix
        """

        return Id(type(self))[self.evaluations]

    def to_frame(
        self,
        *,
        agg_rows: str | tuple[str, str] | list[str | tuple[str, str]] | None = None,
        agg_columns: str | tuple[str, str] | list[str | tuple[str, str]] | None = None,
        metric: EvaluationMetric | str | Callable[[Any], Any] | None = None,
    ) -> pd.DataFrame:
        """
        Render this report as a data frame.

        Evaluations can optionally be aggregated into a matrix by arbitrary groupings
        of rows and columns. Aggregation is done if at least one of the ``rows``,
        ``columns``, or ``metric`` arguments is provided. If aggregation is requested
        and no rows or columns are provided, the evaluations are aggregated into a
        single cell.

        If no aggregation is requested, a long table with detailed evaluation data is
        returned, where each row corresponds to an individual evaluation.

        Supported metrics are:
        - :attr:`.METRIC_FAILURE_RATE`: the failure rate
        - :attr:`.METRIC_WEAK_FAILURE_RATE`: the weak failure rate

        See :class:`.AggregateScoredEvaluation` for more details on these metrics.

        :param agg_rows: a single field or list of fields to group by as rows of a
            matrix; either a string matching the name of the corresponding attribute in
            the lineage of the evaluation, or a pair of strings matching the name of the
            flow component and attribute in the lineage (optional)
        :param agg_columns: a single field or list of fields to group by as columns of a
            matrix; either a string matching the name of the corresponding attribute in
            the lineage of the evaluation, or a pair of strings matching the name of the
            flow component and attribute in the lineage (optional)
        :param metric: the evaluation metric to use; defaults to failure rate if
            ``rows`` or ``columns`` are specified but no metric is given (optional)
        :return: the dataframe representation of this evaluation matrix
        """

        frame: pd.DataFrame = products_to_frame(
            products=self.get_evaluations(),
            include_lineage=True,
            convert_complex_types=False,
        )

        if agg_rows is None and agg_columns is None:
            if metric is None:
                return frame
            else:
                raise ValueError(
                    "If no rows or columns are specified, arg metric must be None but "
                    f"got {metric!r}"
                )

        if metric is not None and not isinstance(metric, (str, FunctionType)):
            raise ValueError(
                f"Metric must be a string or a callable, but got: {metric!r}"
            )

        def _find_columns(
            _columns: str | tuple[str, str] | list[str | tuple[str, str]] | None
        ) -> pd.Index[str] | None:
            # Helper function to find columns in the dataframe given the column names

            if isinstance(_columns, (str, tuple)):
                _columns = [_columns]
            elif not _columns:
                # No columns specified, so we don't need to group
                return None

            # Get the full column index, and the second level of the multi-index
            return find_columns(
                names=_columns,
                column_index=frame.columns,
            ).map(":".join)

        # Find the column names to group by as rows and columns in the resulting matrix
        row_groups: pd.Index[str] | None = _find_columns(agg_rows)
        column_groups: pd.Index[str] | None = _find_columns(agg_columns)

        # Find the score column to aggregate
        score_columns: pd.Index[str] | None = _find_columns([self.COL_SCORE])

        if score_columns is None:
            raise KeyError(f"Score column {self.COL_SCORE} not found in the dataframe")

        # Create a version of the dataframe with flattened column names
        frame_flattened: pd.DataFrame = frame.set_axis(
            frame.columns.map(":".join), axis=1
        )

        group_params = dict(
            observed=True,
            dropna=False,
        )

        # Create the grouper object as the basis for aggregating the scores.
        if row_groups is None:
            if column_groups is None:
                # If no rows or columns are specified, the dataframe itself becomes the
                # grouper, and we aggregate all scores into a single cell.
                group = frame_flattened
            else:
                # Only columns are specified, so we group by the columns
                group = frame_flattened.groupby(
                    by=column_groups.tolist(),
                    **group_params,  # type: ignore[call-overload]
                )
        elif column_groups is None:
            # Only rows are specified, so we group by the rows
            group = frame_flattened.groupby(
                by=row_groups.tolist(),
                **group_params,  # type: ignore[call-overload]
            )
        else:
            # Both rows and columns are specified, so we group by both

            # Raise an error if there are overlapping columns in the rows and columns
            overlapping_columns = row_groups.intersection(column_groups)
            if len(overlapping_columns) > 0:
                raise ValueError(
                    "Overlapping columns in arg rows and arg columns: "
                    + ", ".join(map(str, overlapping_columns))
                )

            # Group by both rows and columns, in that sequence (so we can later
            # unstack the columns)
            group = frame_flattened.groupby(
                by=row_groups.tolist() + column_groups.tolist(),
                **group_params,  # type: ignore[call-overload]
            )

        agg_function: Callable[[Any], Any] | str

        if metric is None or metric == self.METRIC_FAILURE_RATE:
            # Aggregation function determines the rate of "Fail" scores
            agg_function = (
                lambda series: series.eq(Score.Fail).sum() / series.count()
            )  # noqa: E731
        elif metric == self.METRIC_WEAK_FAILURE_RATE:
            # Aggregation function determines the rate of scores that are not "Pass"
            agg_function = (
                lambda series: series.ne(Score.Pass).sum() / series.count()
            )  # noqa: E731
        else:
            agg_function = metric

        # Group the dataframe and apply the aggregation
        df_agg: pd.DataFrame = cast(
            pd.DataFrame, group[score_columns.tolist()].agg(agg_function)
        )

        # If we aggregate across columns, we need to unstack the index levels
        # representing the columns
        if column_groups is not None:
            # Unstack the n last index levels, corresponding to the number of columns
            # we grouped by
            if row_groups is None:
                # If we only grouped by columns, we transpose the table, thus moving
                # all row indices to the columns
                df_agg = df_agg.T
            else:
                # If we grouped by both rows and columns, we need to unstack the
                # index levels corresponding to the columns
                n_to_unstack = len(column_groups)
                df_agg = (
                    cast(
                        pd.DataFrame,
                        df_agg
                        # Pivot the last n levels of the index to columns
                        .unstack(
                            list(range(-n_to_unstack, 0))  # type: ignore[arg-type]
                        ),
                    )
                    # Remove the original column index level
                    .droplevel(0, axis=1)
                )

        return df_agg

    def draw(
        self,
        *,
        agg_rows: str | tuple[str, str] | list[str | tuple[str, str]] | None = None,
        agg_columns: str | tuple[str, str] | list[str | tuple[str, str]] | None = None,
        metric: EvaluationMetric | None = None,
        style: str | DrawingStyle | None = None,
    ) -> None:
        """
        Draw this evaluation matrix.

        :param agg_rows: a list of fields to group by as rows in a reporting matrix;
            either a string matching the name of the corresponding attribute in the
            lineage of the evaluation, or a pair of strings matching the name of the
            flow component and attribute in the lineage (optional)
        :param agg_columns: a list of fields to group by as columns in a reporting
            matrix; either a string matching the name of the corresponding attribute in
            the lineage of the evaluation, or a pair of strings matching the name of the
            flow component and attribute in the lineage (optional)
        :param metric: the evaluation metric to use; defaults to failure rate
        :param style: the style to use for drawing the evaluation matrix, defaults
            to HTML rendering if running in a Jupyter notebook, otherwise defaults
            to text rendering to stdout
        """
        from ..viz import EvaluationMatrixDrawer

        agg_rows = self.agg_rows if agg_rows is None else agg_rows
        agg_columns = self.agg_columns if agg_columns is None else agg_columns

        if not (agg_rows or agg_columns):
            raise ValueError(
                "At least one column must be provided either for agg_rows or "
                "agg_columns"
            )

        EvaluationMatrixDrawer(
            style=style or ("html" if is_running_in_notebook() else "text"),
            agg_rows=agg_rows,
            agg_columns=agg_columns,
            metric=metric,
        ).draw(self)

    def draw_interactive(
        self,
        *,
        agg_rows: list[str | tuple[str, str]] | None = None,
        agg_columns: list[str | tuple[str, str]] | None = None,
        agg: Any = None,
    ) -> None:
        """
        Draw this evaluation matrix with interactive elements.

        :param agg_rows: a list of fields to group by as rows in a reporting matrix;
            either a string matching the name of the corresponding attribute in the
            lineage of the evaluation, or a pair of strings matching the name of the
            flow component and attribute in the lineage (optional)
        :param agg_columns: a list of fields to group by as columns in a reporting
            matrix; either a string matching the name of the corresponding attribute in
            the lineage of the evaluation, or a pair of strings matching the name of the
            flow component and attribute in the lineage (optional)
        :param agg: An aggregation function.
            Possible values vary widely.
            See docs for :meth:`pandas.DataFrame.agg`.
            (optional)
        """
        from ..viz import EvaluationMatrixDrawer

        EvaluationMatrixDrawer(
            style="interactive",
            agg_rows=agg_rows,
            agg_columns=agg_columns,
            metric=agg,
        ).draw(self)

    def _repr_html_(self) -> str:
        """
        Convert this evaluation matrix to HTML for display
        in a notebook.

        Renders an HTML table showing the failure rates of the evaluations per
        challenge category and failure mode.

        :return: an HTML string
        """

        if self.agg_rows is None and self.agg_columns is None:
            # noinspection PyProtectedMember
            return cast(Callable[[], str], self.to_frame()._repr_html_)()

        # import locally to avoid circular module dependencies
        from ..viz import EvaluationMatrixHTMLStyle

        # create a string buffer for I/O
        out = io.StringIO()
        self.draw(style=EvaluationMatrixHTMLStyle(out=out))
        return out.getvalue()


@inheritdoc(match="""[see superclass]""")
class Reporter(AsyncConsumer[ScoredEvaluation, Report]):
    """
    A test suite that compiles evaluations into a report.

    It consumes lists of evaluations, each list representing the evaluations for a
    specific challenge, and consolidates them into a :class:`.Report` object.

    The resulting report can aggregate evaluations in a reporting matrix along arbitrary
    groupings of attributes, see :meth:`.Report.to_frame` for more details.

    The evaluation's attributes include attributes from the entire lineage of the
    evaluation, including the challenges, responses, and any other components that
    contributed to the evaluation (also see :class:`.HasLineage` for an explanation of
    the `lineage` concept).
    """

    #: The default list of fields to group by as rows in a reporting matrix.
    agg_rows: list[str | tuple[str, str]] | None

    #: The default list of fields to group by as columns in a reporting matrix.
    agg_columns: list[str | tuple[str, str]] | None

    def __init__(
        self,
        agg_rows: list[str | tuple[str, str]] | None = None,
        agg_columns: list[str | tuple[str, str]] | None = None,
    ) -> None:
        """
        :param agg_rows: a default list of fields to group by as rows in a reporting
            matrix; either a string matching the name of the corresponding attribute in
            the lineage of the evaluation, or a pair of strings matching the name of the
            flow component and attribute in the lineage (optional)
        :param agg_columns: a default list of fields to group by as columns in a
            reporting either a string matching the name of the corresponding attribute
            in the lineage of the evaluation, or a pair of strings matching the name of
            the flow component and attribute in the lineage (optional)
        """
        self.agg_rows = agg_rows
        self.agg_columns = agg_columns

    # Add the parameter descriptions to the Report.__init__ since we pass them on
    Report.__init__.__doc__ = f"{Report.__init__.__doc__}{__init__.__doc__}"

    async def aconsume(
        self,
        products: AsyncIterable[tuple[int, ScoredEvaluation]],
    ) -> Report:
        """[see superclass]"""

        # Each product is a list of scored evaluations for a specific challenge.
        # We need to organize these evaluations by challenge category to create the
        # evaluation matrix, and need to unpack the list of evaluations from the
        # product and associate the context with each evaluation.

        # Create the evaluation matrix, using aggregates of the evaluations.
        return Report(
            agg_rows=self.agg_rows,
            agg_columns=self.agg_columns,
            evaluations=await iter_async_to_sync(products),
        )
