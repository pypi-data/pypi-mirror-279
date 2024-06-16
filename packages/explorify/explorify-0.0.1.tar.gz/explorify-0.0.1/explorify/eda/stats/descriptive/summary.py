#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/stats/descriptive/summary.py                                         #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday August 23rd 2023 12:15:10 am                                              #
# Modified   : Thursday June 13th 2024 02:54:51 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Summary Statistics Module"""
import logging
from typing import Union

import numpy as np
import pandas as pd

from explorify import NON_NUMERIC_TYPES, NUMERIC_TYPES
from explorify.eda.stats.descriptive.base import DescriptiveStats

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------ #
class SummaryStats(DescriptiveStats):
    """Object encapsulating numeric and categorical data summary statistics"""

    def __init__(self) -> None:
        super().__init__()
        self._numeric_summary = None
        self._categorical_summary = None

    @property
    def numeric(self) -> pd.DataFrame:
        """Returns descriptive statistics for numeric variables if available."""
        return self._numeric_summary

    @property
    def categorical(self) -> pd.DataFrame:
        """Returns descriptive statistics for numeric variables if available."""
        return self._categorical_summary

    def describe(
        self,
        data: Union[pd.DataFrame, pd.Series],
        groupby: Union[str, list[str]] = None,
        include: Union[str, list[str]] = None,
        exclude: Union[str, list[str]] = None,
    ) -> pd.DataFrame:
        """Computes descriptive statistics

        Args:
            data Union[pd.DataFrame, pd.Series]: Pandas dataframe or series.
            groupby Union[str, list[str]]): key or keys in data to group by. Optional.
            include Union[str, list[str]]):
                A white list of data types to include in the result. Ignored for Series.
                Here are the options:
                - 'all', None: All columns of the input will be included in the output.
                    This departs from pandas default behavior whereby None is interpreted
                    to include all numeric columns only. This means the default
                    behavior is to analyze the dataset unless otherwise specified.
                - A list-like of dtypes : Limits the results to the provided data types.
                    To limit the result to numeric types submit numpy.number.
                    To limit it instead to object columns submit the numpy.object data type.
                    Strings can also be used in the style of select_dtypes
                    (e.g. df.describe(include=['O'])).
                    To select pandas categorical columns, use 'category'
             exclude Union[str, list[str]]):
                A black list of data types to omit from the result. Ignored for Series.
                Here are the options:
                - A list-like of dtypes : Excludes the provided data types from the result,
                    unless a variable of an excluded data type is in x, or groupby. Variable or variables
                    in x or groupby are included by definition.
                    To exclude numeric types submit numpy.number.
                    To exclude object columns submit the data type numpy.object.
                    Strings can also be used in the style of select_dtypes
                    (e.g. df.describe(exclude=['O'])).
                    To exclude pandas categorical columns, use 'category'
                - None (default) : The result will exclude nothing.
        """
        # Not sure why series exist
        if isinstance(data, pd.Series):
            data = data.to_frame()

        if groupby is not None:
            data = data.groupby(by=groupby)

        self._numeric_summary = self._describe_numeric(
            data=data, include=include, exclude=exclude
        )
        self._categorical_summary = self._describe_categorical(
            data=data, include=include, exclude=exclude
        )

    def _describe_categorical(
        self,
        data: pd.DataFrame,
        include: Union[str, list[str]] = None,
        exclude: Union[str, list[str]] = None,
    ) -> pd.DataFrame:
        """Computes summary statistics for categorical variables."""

        # If inclusion/exclusion not specified, we describe objects
        if include is None and exclude is None:
            include = NON_NUMERIC_TYPES
        # If include is an iterable, remove numeric types, bounce if there are none.
        elif isinstance(include, list):
            include = [dtype for dtype in include if dtype not in NUMERIC_TYPES]
            if len(include) == 0:
                return None
        # If include is numeric dtype bounce.
        elif include in NUMERIC_TYPES:
            return None

        # If we are here, include is None and exclude non-Null.
        # If exclude is an iterable, append np.number type to exclusion
        elif isinstance(exclude, (list, np.ndarray)) and np.number not in exclude:
            exclude.append(np.number)

        # Otherwise, exclude is a string or dtype. Create an iterable, and add
        # numeric types to the exclusion list.
        else:
            exclude = [exclude, np.number]

        try:
            return data.describe(include=include, exclude=exclude)
        except ValueError:
            msg = "No categorical values to describe"
            logger.debug(msg)
            return None

    def _describe_numeric(
        self,
        data: pd.DataFrame,
        include: Union[str, list[str]] = None,
        exclude: Union[str, list[str]] = None,
    ) -> pd.DataFrame:
        """Computes summary statistics for numeric variables."""

        # If inclusion/exclusion not specified, we describe numbers
        if include is None and exclude is None:
            include = np.number
        # If include is an iterable, extract numeric types, bounce if there are none.
        elif isinstance(include, list):
            include = [dtype for dtype in include if dtype in NUMERIC_TYPES]
            if len(include) == 0:
                return None
        # If include is not a numeric type, bounce.
        elif include is not None and include not in NUMERIC_TYPES:
            return None

        # If we are here, include is None and exclude non-Null.
        # If exclude is a list, we extend the list with all non-numeric
        # dtypes.
        elif isinstance(exclude, (list, np.ndarray)):
            exclude.extend(NON_NUMERIC_TYPES)

        # Otherwise, exclude is a string or dtype, make it an iterable
        # and add non-null types
        else:
            exclude = [exclude]
            exclude.extend(NON_NUMERIC_TYPES)

        try:
            return data.describe(include=include, exclude=exclude)
        except ValueError:
            msg = "No numeric values to describe"
            logger.debug(msg)
            return None
