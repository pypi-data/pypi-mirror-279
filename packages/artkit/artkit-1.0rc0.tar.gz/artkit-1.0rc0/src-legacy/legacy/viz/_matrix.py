"""
Implementation of evaluation matrix visualization.
"""

from __future__ import annotations

import json
import logging
import random
import string
from abc import ABCMeta
from collections.abc import Callable, Iterable
from typing import Any, Literal, TypeAlias

import pandas as pd
from pandas.core.groupby import DataFrameGroupBy

from pytools.api import appenddoc, inheritdoc
from pytools.viz import Drawer, HTMLStyle, TextStyle
from pytools.viz.color import MatplotColorScheme

from ..report import Report
from ..util import find_columns
from .base import EvaluationMatrix, EvaluationMatrixStyle

log = logging.getLogger(__name__)

__all__ = [
    "EvaluationMatrixDrawer",
    "EvaluationMatrixHTMLStyle",
    "EvaluationMatrixHTMLInteractiveStyle",
    "EvaluationMatrixTextStyle",
]


#
# Type aliases
#

EvaluationMetric: TypeAlias = Literal["failure rate", "weak failure rate"] | None


#
# Classes
#


@inheritdoc(match="[see superclass]")
class EvaluationMatrixDrawer(Drawer[Report, EvaluationMatrixStyle]):
    """
    A drawer for evaluation matrices.

    See :class:`.Report` for more information on the structure of evaluation reports,
    and the approach to aggregating evaluations into a matrix.
    """

    #: The name of the evaluation metric to be displayed
    metric: EvaluationMetric | str | Callable[..., Any]

    #: The attributes to aggregate by in the rows of the evaluation matrix
    agg_rows: list[str | tuple[str, str]]

    #: The attributes to aggregate by in the columns of the evaluation matrix
    agg_columns: list[str | tuple[str, str]]

    @appenddoc(to=Drawer.__init__)
    def __init__(
        self,
        style: EvaluationMatrixStyle | str | None = None,
        *,
        agg_rows: str | tuple[str, str] | list[str | tuple[str, str]],
        agg_columns: str | tuple[str, str] | list[str | tuple[str, str]],
        metric: EvaluationMetric | str | Callable[..., Any] = None,
    ) -> None:
        """
        :param agg_rows: the attributes to aggregate by in the rows of the evaluation
            matrix
        :param agg_columns: the attributes to aggregate by in the columns of the
            evaluation matrix
        :param metric: the name of the evaluation metric to be displayed; defaults
            to "weak failure rate"
        """
        super().__init__(style)
        # noinspection PyTypeChecker
        self.metric = metric or Report.METRIC_WEAK_FAILURE_RATE

        def _index_names_to_list(
            names: str | tuple[str, str] | list[str | tuple[str, str]], *, arg_name: str
        ) -> list[str | tuple[str, str]]:
            if names is None:
                return []
            elif isinstance(names, (str, tuple)):
                return [names]
            elif isinstance(names, list):
                return names
            else:
                raise ValueError(
                    f"Invalid type for arg {arg_name}: {type(names).__name__}"
                )

        self.agg_rows = _index_names_to_list(agg_rows, arg_name="agg_rows")
        self.agg_columns = _index_names_to_list(agg_columns, arg_name="agg_columns")

    @classmethod
    def get_style_classes(cls) -> Iterable[type[EvaluationMatrixStyle]]:
        return [
            EvaluationMatrixHTMLStyle,
            EvaluationMatrixHTMLInteractiveStyle,
            EvaluationMatrixTextStyle,
        ]

    @classmethod
    def get_default_style(cls) -> EvaluationMatrixStyle:
        """[see superclass]"""
        return EvaluationMatrixHTMLStyle()

    def draw(self, data: Report, *, title: str | None = None) -> None:
        """[see superclass]"""
        super().draw(data, title=title or f"Evaluation Matrix ({self.metric})")

    def _draw(self, data: Report) -> None:
        self.style.render_matrix(
            EvaluationMatrix(
                metrics=data.to_frame(
                    agg_rows=self.agg_rows,
                    agg_columns=self.agg_columns,
                    metric=self.metric,
                ),
                n_groups_row=len(self.agg_rows or []),
                n_groups_column=len(self.agg_columns or []),
                drilldown=(
                    data.to_frame().pipe(
                        lambda df: df.set_index(
                            # match the grouping columns for rows and columns in the
                            # evaluation matrix, and make them the index of the
                            # drilldown data frame, also preserving them as data columns
                            find_columns(
                                self.agg_rows + self.agg_columns,
                                column_index=df.columns,
                            ).tolist(),
                            drop=False,
                        )
                    )
                    if self.style.supports_drilldown
                    else None
                ),
            )
        )


@inheritdoc(match="[see superclass]")
class _BaseEvaluationMatrixHTMLStyle(
    HTMLStyle[MatplotColorScheme], EvaluationMatrixStyle, metaclass=ABCMeta
):
    """
    A style for rendering evaluation matrices as HTML tables.
    """

    #: The title of the drawing
    _title: str = ""

    def render_title(self, title: str) -> str:
        """[see superclass]"""
        self._title = title
        return ""

    def finalize_drawing(self, **kwargs: Any) -> None:
        """[see superclass]"""
        super().finalize_drawing()
        self._title = ""


@inheritdoc(match="[see superclass]")
class EvaluationMatrixHTMLStyle(_BaseEvaluationMatrixHTMLStyle):
    """
    A style for rendering evaluation matrices as HTML tables.
    """

    @property
    def supports_drilldown(self) -> bool:
        """``False``"""
        return False

    def render_matrix(self, matrix: EvaluationMatrix) -> None:
        """[see superclass]"""

        print(
            matrix.metrics
            # get the Styler object
            .style
            # set the caption
            .set_caption(self._title)
            # set the background gradient
            .background_gradient(
                cmap=self.colors.colormap,
                low=0.0,
                high=1.0,
            )
            # render html
            .to_html(),
            # output to the stream associated with this style
            file=self.out,
        )


@inheritdoc(match="[see superclass]")
class EvaluationMatrixHTMLInteractiveStyle(_BaseEvaluationMatrixHTMLStyle):
    """
    A style for rendering evaluation matrices as HTML tables with
    interactivity.
    """

    @classmethod
    def get_default_style_name(cls) -> str:
        """[see superclass]"""
        return "interactive"

    @property
    def supports_drilldown(self) -> bool:
        """``True``"""
        return True

    def render_matrix(self, matrix: EvaluationMatrix) -> None:
        """[see superclass]"""

        # Get the metrics data frame
        metrics_df = matrix.metrics

        # Get the evaluations data frame, whose index levels correspond to the
        # rows and columns of the matrix
        drilldown_df = matrix.drilldown

        if drilldown_df is None:  # pragma: no cover
            raise ValueError(
                "The drilldown data frame is required for interactive drilldown."
            )

        # Create a groupby object that groups the evaluations by the evaluations index
        grouped: DataFrameGroupBy[Any] = drilldown_df.groupby(
            level=list(range(drilldown_df.index.nlevels))
        )

        html_sr: pd.Series[Any] = (
            grouped
            # Generate a series with a multiindex comprising all index levels of the
            # matrix row and column groups, and the values as HTML tables containing
            # drilldown information in each cell, derived from all evaluations that
            # contributed to the aggregated metric in that cell
            .apply(
                lambda group_df: group_df.style.set_table_styles(
                    [
                        {
                            "selector": "td",
                            "props": [
                                ("text-align", "left"),
                                ("vertical-align", "top"),
                                ("white-space", "pre-wrap"),
                            ],
                        }
                    ],
                    overwrite=False,
                ).to_html(index=False)
            )
        )

        html_df: pd.DataFrame

        if matrix.n_groups_col:
            if matrix.n_groups_row:
                # Pivot the column dimensions to the column index
                html_df = html_sr.unstack(matrix.n_groups_col)
            else:
                # If there are no row groups, we turn the series into a single-row
                # DataFrame
                html_df = html_sr.to_frame().T
        else:
            html_df = html_sr.to_frame()

        # escaped JSON representation of the df
        df_json = json.dumps(html_df.to_json(orient="split")).replace("'", "\\'")

        # create a unique id for this table
        table_id = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        # js to inject into the notebook
        script = """
        <style>
        .cell-highlight {{
            font-weight: bold;
        }}
        </style>
        <script>
        // embed json dataframe
        var dfData = JSON.parse({df_json});
        // add click event to each cell in the table with a data class
        document.querySelectorAll('[id^="T_{table_id}"].data').forEach(cell => {{
            cell.addEventListener('click', (e) => {{
                const prev_hl = document.querySelector('.cell-highlight');
                if (prev_hl) {{
                    prev_hl.classList.remove('cell-highlight');
                }}
                e.target.classList.add('cell-highlight');
                const indices = e.target.id.split('_').slice(2).map(\
i => +i.replace(/\\D/g, ''));
                const data = dfData.data[indices[0]][indices[1]];
                document.getElementById('detail_{table_id}').innerHTML = data;
            }});
        }});
        </script>
        """.format(  # use format since mypy has trouble with f-strings
            df_json=df_json,
            table_id=table_id,
        )

        # div to contain cell details
        detail_div = f'<div id="detail_{table_id}" style="margin-top:20px;"></div>'

        html = (
            metrics_df.style.set_caption(self._title)
            .background_gradient(
                cmap=self.colors.colormap,
                low=0.0,
                high=1.0,
            )
            .to_html(table_uuid=table_id)
        )

        print(html + script + detail_div, file=self.out)

    def finalize_drawing(self, **kwargs: Any) -> None:
        """[see superclass]"""
        super().finalize_drawing()
        self._title = ""


@inheritdoc(match="[see superclass]")
class EvaluationMatrixTextStyle(EvaluationMatrixStyle, TextStyle):
    """
    A style for rendering evaluation matrices as text tables.
    """

    @property
    def supports_drilldown(self) -> bool:
        """``False``"""
        return False

    def render_matrix(self, matrix: EvaluationMatrix) -> None:
        """[see superclass]"""
        # write the data frame, honouring the maximum width
        print(matrix.metrics.to_string(line_width=self.width), file=self.out)
