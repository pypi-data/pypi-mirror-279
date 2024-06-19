"""
Utility methods to convert `HasLineage` instances to pandas series and data frames.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable, Mapping
from typing import Any

import pandas as pd
from fluxus.lineage import HasLineage

from ._pandas import simplify_complex_types

log = logging.getLogger(__name__)

__all__ = [
    "products_to_frame",
    "product_to_series",
]


#
# Functions
#


def product_to_series(
    product: HasLineage[Any],
    *,
    include_lineage: bool = True,
    convert_complex_types: bool = False,
) -> pd.Series[Any]:
    """
    Convert a product to a :class:`pandas.Series`, optionally including all products of
    the lineage.

    For individual products, the series index is the product's attribute names and
    the values are the attribute values.

    When including the lineage, the series index is a multi-index with two levels: the
    product names and the attribute names. Both of these are obtained from
    :meth:`.HasLineage.get_lineage_attributes`, please refer to the documentation of
    that method for more details.

    :param product: the product to convert
    :param include_lineage: if ``True``, include all products of the lineage in the
        series; if ``False``, include only the product itself
    :param convert_complex_types: if ``True``, convert complex types to strings;
        keep them as is otherwise
    :return: the series
    """

    #: The series to return
    sr: pd.Series[Any]

    def _convert_lineage(
        attributes: Mapping[str, Mapping[str, Any]]
    ) -> dict[tuple[str, str], Any]:
        # Convert two levels of nested dictionaries to a single level with tuples as
        # keys. Convert complex types to strings if requested.
        return {
            (product_name, attribute_name): attribute_value
            for product_name, product_attributes in _convert_product(attributes).items()
            for attribute_name, attribute_value in product_attributes.items()
        }

    def _convert_product(attributes: Mapping[str, Any]) -> Mapping[str, Any]:
        # Convert complex types to strings if requested.
        if convert_complex_types:
            return {
                attribute_name: (simplify_complex_types(attribute_value))
                for attribute_name, attribute_value in attributes.items()
            }
        else:
            return attributes

    if include_lineage:

        # Create a Series with two index levels: the product names and the attribute
        # names.
        sr = pd.Series(
            _convert_lineage(product.get_lineage_attributes()),
            name=type(product).__name__,
        )

    else:
        # If we only want the product itself, create a series with the product's
        # attributes.
        sr = pd.Series(
            _convert_product(product.product_attributes), name=type(product).__name__
        )

    return sr


def products_to_frame(
    products: Iterable[HasLineage[Any]],
    include_lineage: bool = True,
    convert_complex_types: bool = False,
) -> pd.DataFrame:
    """
    Convert a list of products to a :class:`pandas.DataFrame`.

    :param products: the products to convert
    :param include_lineage: if ``True``, include all products of the lineage in the
        series; if ``False``, include only the product itself
    :param convert_complex_types: if ``True``, convert complex types to strings;
        keep them as is otherwise
    :return: the data frame
    """

    # Convert each product to a series and concatenate them into a data frame.
    return pd.concat(
        [
            product_to_series(
                product,
                include_lineage=include_lineage,
                convert_complex_types=convert_complex_types,
            )
            for product in products
        ],
        axis=1,
        ignore_index=True,
    ).T.convert_dtypes()
