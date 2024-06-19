"""
Utility functions for pandas.
"""

from __future__ import annotations

import functools
import logging
import operator
from types import NoneType
from typing import Any

import pandas as pd

log = logging.getLogger(__name__)

__all__ = [
    "find_columns",
    "simplify_complex_types",
]


def find_columns(
    names: list[str | tuple[str, str]], *, column_index: pd.Index[str]
) -> pd.Index[str]:
    """
    Find the columns in the given column index that match the given names.

    We support two types of column names: single strings and pairs of strings. The
    former is a simple column name on the second level of the multi-index, while the
    latter is a column name on the first level and a column name on the second level.

    :param names: the names of the columns to find
    :param column_index: the column index to search in
    :return: the index of the columns that match the given names
    :raises KeyError: if any of the columns could not be found
    """

    column_index_l1: pd.Index[str] = column_index.get_level_values(1)

    column_selections: dict[str | tuple[str, str], pd.Index[bool]] = {
        col: (
            (column_index_l1 if isinstance(col, str) else column_index)
            == col  # type: ignore[misc]
        )
        for col in names
    }

    # Raise an error if any of the columns could not be found
    missing_columns = [
        col
        for col, selection in column_selections.items()
        if not selection.any()  # type: ignore[attr-defined]
    ]
    if missing_columns:
        raise KeyError("Column(s) not found: " + ", ".join(map(str, missing_columns)))

    # Return a flattened index of the columns that we matched
    return column_index[functools.reduce(operator.or_, column_selections.values())]


def simplify_complex_types(
    value: Any,
) -> bool | int | float | str | bytes | complex | None:
    """
    Convert instances of complex types to strings.

    :param value: the value to convert
    :return: the value, with complex types converted to strings
    """
    if isinstance(value, (bool, int, float, str, bytes, complex, NoneType)):
        return value
    else:
        return str(value)
