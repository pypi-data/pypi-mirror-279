#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/univariate/base.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday June 14th 2024 03:14:50 pm                                                   #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Univariate EDA Base Module"""
import pandas as pd

from explorify.eda.base import Analyzer


# ------------------------------------------------------------------------------------------------ #
class UnivariateAnalyzer(Analyzer):
    """Abstract base class for univariate analyses"""

    def __init__(self, data: pd.DataFrame) -> None:  # pragma: no cover
        super().__init__(data)


# ------------------------------------------------------------------------------------------------ #
class UnivariateCategoricalAnalyzer(Analyzer):
    """Abstract class for univariate analyses of categorical variables."""

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the BivariateCategoricalAnalyzer instance.

        Args:
            data (pd.DataFrame): The input data containing the variables.
        """
        super().__init__(data=data)

    def validate_input(self, a_name: str) -> None:
        """
        Validates the input variables.

        Args:
            a_name (str): The name of the categorical variable.

        Raises
        ------
        ValueError
            If the input variables are not in the DataFrame or are numeric.
        """
        if a_name not in self._data.columns:
            raise ValueError(f"Variables '{a_name}' is not in the DataFrame.")

        if pd.api.types.is_numeric_dtype(self._data[a_name]):
            raise ValueError(f"Variable '{a_name}' is not categorical.")


# ------------------------------------------------------------------------------------------------ #
class UnivariateNumericAnalyzer(Analyzer):
    """Abstract base class for univariate analyses of numeric variables."""

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the BivariateCategoricalAnalyzer instance.

        Args:
            data (pd.DataFrame): The input data containing the variables.
        """
        super().__init__(data=data)

    def validate_input(self, a_name: str) -> None:
        """
        Validates the input variables.

        Args:
            a_name (str): The name of the numeric variable.

        Raises
        ------
        ValueError
            If the input variables are not in the DataFrame or are numeric.
        """
        if a_name not in self._data.columns:
            raise ValueError(f"Variables '{a_name}' is not in the DataFrame.")

        if not pd.api.types.is_numeric_dtype(self._data[a_name]):
            raise ValueError(f"Variable '{a_name}' is not numeric.")
