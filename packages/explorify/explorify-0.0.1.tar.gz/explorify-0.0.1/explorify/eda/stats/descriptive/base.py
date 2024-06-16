#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/stats/descriptive/base.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 22nd 2023 09:03:39 pm                                                #
# Modified   : Thursday June 13th 2024 02:54:51 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from typing import Union

import pandas as pd


# ------------------------------------------------------------------------------------------------ #
class DescriptiveStats(ABC):
    """Base class for describing numeric and categorical data."""

    @abstractproperty
    def numeric(self) -> pd.DataFrame:
        """Returns descriptive statistics for numeric variables if available."""

    @abstractproperty
    def categorical(self) -> pd.DataFrame:
        """Returns descriptive statistics for categorical variables if available."""

    @abstractmethod
    def describe(
        self,
        data: Union[pd.DataFrame, pd.Series],
        groupby: Union[str, list[str]] = None,
        include: Union[str, list[str]] = None,
        exclude: Union[str, list[str]] = None,
    ) -> None:
        """Computes descriptive statistics

        Args:
            data Union[pd.DataFrame, pd.Series]: Pandas dataframe or series.
            groupby Union[str, list[str]]): key or keys in data to group by. Optional.
            include Union[str, list[str]]):
                A white list of data types to include in the result. Ignored for Series.
                Here are the options:
                - 'all' : All columns of the input will be included in the output.
                - A list-like of dtypes : Limits the results to the provided data types.
                    To limit the result to numeric types submit numpy.number.
                    To limit it instead to object columns submit the numpy.object data type.
                    Strings can also be used in the style of select_dtypes
                    (e.g. df.describe(include=['O'])).
                    To select pandas categorical columns, use 'category'
                - None (default) : The result will include all numeric columns.
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
