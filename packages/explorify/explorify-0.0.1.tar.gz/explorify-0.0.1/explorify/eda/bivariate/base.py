#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/bivariate/base.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday June 14th 2024 03:13:55 pm                                                   #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Bivariate Base Module"""
from abc import abstractmethod
from typing import Union

import pandas as pd

from explorify.eda.base import Analyzer


# ------------------------------------------------------------------------------------------------ #
class BivariateAnalyzer(Analyzer):  # pragma: no cover
    """Abstract base class for bivariate analyses"""

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)


# ------------------------------------------------------------------------------------------------ #
#                       CATEGORICAL NUMERIC BIVARIATE ANALYSIS                                     #
# ------------------------------------------------------------------------------------------------ #
class BivariateCategoricalNumericAnalyzer(BivariateAnalyzer):  # pragma: no cover
    """
    Base class for categorical-numeric bivariate analysis.

    Attributes:
        _data (pd.DataFrame): The input data containing the variables.

    Methods:
        __init__(self, data: pd.DataFrame):
            Initializes the BivariateCategoricalNumericAnalyzer instance.

        validate_input(self, a_name: str, b_name: str) -> None:
            Validates the input variables.

        analyze(self, *args, **kwargs) -> Union[pd.DataFrame, float, int]:
            Abstract method to conduct the analysis for the class.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the BivariateCategoricalNumericAnalyzer instance.

        Args:
            data (pd.DataFrame): The input data containing the variables.
        """
        super().__init__(data=data)

    def validate_input(self, a_name: str, b_name: str) -> None:
        """
        Validates the input variables.

        Args:
            a_name (str): The name of the categorical variable.
            b_name (str): The name of the numeric variable.

        Raises:
            ValueError: If the input variables are not in the DataFrame or are not of the correct type.
        """
        if a_name not in self._data.columns or b_name not in self._data.columns:
            raise ValueError(
                f"Variables '{a_name}' and/or '{b_name}' are not in the DataFrame."
            )

        if pd.api.types.is_numeric_dtype(self._data[a_name]):
            raise ValueError(f"Variable '{a_name}' is not categorical.")

        if not pd.api.types.is_numeric_dtype(self._data[b_name]):
            raise ValueError(f"Variable '{b_name}' is not numeric.")

    @abstractmethod
    def analyze(self, *args, **kwargs) -> Union[pd.DataFrame, float, int]:
        """
        Abstract method to conduct the analysis for the class.

        Subclasses must implement this method.

        Returns:
            Union[pd.DataFrame, float, int]: The result of the analysis, which can be a DataFrame, float, or int depending on the analysis.
        """
        pass


# ------------------------------------------------------------------------------------------------ #
#                             CATEGORICAL BIVARIATE ANALYSIS                                       #
# ------------------------------------------------------------------------------------------------ #


class BivariateCategoricalAnalyzer(BivariateAnalyzer):  # pragma: no cover
    """
    Base class for categorical-to-categorical bivariate analysis.

    Attributes:
        _data (pd.DataFrame): The input data containing the variables.

    Methods:
        __init__(self, data: pd.DataFrame):
            Initializes the BivariateCategoricalAnalyzer instance.

        validate_input(self, a_name: str, b_name: str) -> None:
            Validates the input variables.

        analyze(self, *args, **kwargs) -> Union[pd.DataFrame, float, int]:
            Abstract method to conduct the analysis for the class.

    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the BivariateCategoricalAnalyzer instance.

        Args:
            data (pd.DataFrame): The input data containing the variables.
        """
        super().__init__(data=data)

    def validate_input(self, a_name: str, b_name: str) -> None:
        """
        Validates the input variables.

        Parameters
        ----------
        a_name : str
            The name of the first categorical variable.
        b_name : str
            The name of the second categorical variable.

        Raises
        ------
        ValueError
            If the input variables are not in the DataFrame or are numeric.
        """
        if a_name not in self._data.columns or b_name not in self._data.columns:
            raise ValueError(
                f"Variables '{a_name}' and/or '{b_name}' are not in the DataFrame."
            )

        if pd.api.types.is_numeric_dtype(self._data[a_name]):
            raise ValueError(f"Variable '{a_name}' is numeric and not categorical.")

        if pd.api.types.is_numeric_dtype(self._data[b_name]):
            raise ValueError(f"Variable '{b_name}' is numeric and not categorical.")

    @abstractmethod
    def analyze(self, *args, **kwargs) -> Union[pd.DataFrame, float, int]:
        """
        Abstract method to conduct the analysis for the class.

        Subclasses must implement this method.

        Returns
        -------
        Union[pd.DataFrame, float, int]
            The result of the analysis, which can be a DataFrame, float, or int depending on the analysis.
        """
        pass


# ------------------------------------------------------------------------------------------------ #
#                               NUMERIC BIVARIATE ANALYSIS                                         #
# ------------------------------------------------------------------------------------------------ #


class BivariateNumericAnalyzer(BivariateAnalyzer):  # pragma: no cover
    """
    Base class for numeric-to-numeric bivariate analysis.

    Attributes:
        _data (pd.DataFrame): The input data containing the variables.

    Methods:
        __init__(self, data: pd.DataFrame):
            Initializes the BivariateNumericAnalyzer instance.

        validate_input(self, a_name: str, b_name: str) -> None:
            Validates the input variables.

        analyze(self, *args, **kwargs) -> Union[pd.DataFrame, float, int]:
            Abstract method to conduct the analysis for the class.

    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the BivariateNumericAnalyzer instance.

        Args:
            data (pd.DataFrame): The input data containing the variables.
        """
        super().__init__(data=data)

    def validate_input(self, a_name: str, b_name: str) -> None:
        """
        Validates the input variables.

        Parameters
        ----------
        a_name : str
            The name of the first numeric variable.
        b_name : str
            The name of the second numeric variable.

        Raises
        ------
        ValueError
            If the input variables are not in the DataFrame or are numeric.
        """
        if a_name not in self._data.columns or b_name not in self._data.columns:
            raise ValueError(
                f"Variables '{a_name}' and/or '{b_name}' are not in the DataFrame."
            )

        if not pd.api.types.is_numeric_dtype(self._data[a_name]):
            raise ValueError(f"Variable '{a_name}' is not numeric.")

        if not pd.api.types.is_numeric_dtype(self._data[b_name]):
            raise ValueError(f"Variable '{b_name}' is not numeric.")

    @abstractmethod
    def analyze(self, *args, **kwargs) -> Union[pd.DataFrame, float, int]:
        """
        Abstract method to conduct the analysis for the class.

        Subclasses must implement this method.

        Returns
        -------
        Union[pd.DataFrame, float, int]
            The result of the analysis, which can be a DataFrame, float, or int depending on the analysis.
        """
        pass
