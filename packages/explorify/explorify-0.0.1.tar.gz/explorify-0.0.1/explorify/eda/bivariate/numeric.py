#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/bivariate/numeric.py                                                 #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday June 9th 2024 03:08:05 pm                                                    #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Numeric Bivariate Analyzer Module"""
from typing import Type

import pandas as pd

from explorify.eda.bivariate.base import BivariateNumericAnalyzer
from explorify.eda.regression.simple import (
    SimpleRegressionAnalyzer,
    SimpleRegressionResult,
)


# ------------------------------------------------------------------------------------------------ #
#                                 BIVARIATE REGRESSION ANALYSIS                                    #
# ------------------------------------------------------------------------------------------------ #
class BivariateRegressionAnalyzer(BivariateNumericAnalyzer):
    """
    Performs regression analysis and visualization between two numeric variables.

    Inherits from BivariateNumericAnalyzer.

    Args:
        data (pd.DataFrame): The input data containing the variables.
        visualizer (Visualizer): Visualizer instance for plotting.
        simple_linear_regression_cls (SimpleRegressionAnalyzer): Class for performing simple linear regression.

    Attributes:
        _visualizer (Visualizer): Visualizer instance for plotting.
        _simple_linear_regression_cls (SimpleRegressionAnalyzer): Class for performing simple linear regression.

    """

    def __init__(
        self,
        data: pd.DataFrame,
        simple_linear_regression_cls: Type[
            SimpleRegressionAnalyzer
        ] = SimpleRegressionAnalyzer,
    ) -> None:
        super().__init__(data=data)
        self._simple_linear_regression_cls = simple_linear_regression_cls

    def analyze(self, a_name: str, b_name: str) -> SimpleRegressionResult:
        """
        Performs regression analysis between two numeric variables.

        Args:
            a_name (str): Name of the independent variable.
            b_name (str): Name of the dependent variable.

        Returns:
            SimpleRegressionResult: Results of the regression analysis including coefficients, p-values, and R-squared value.
        """
        self.validate_input(a_name=a_name, b_name=b_name)
        analysis = self._simple_linear_regression_cls(
            a_name=a_name, b_name=b_name, data=self._data
        )
        analysis.run()
        return analysis.result

    def plot(self, a_name: str, b_name: str, title: str = None) -> None:
        """
        Visualizes the relationship between two numeric variables.

        Args:
            a_name (str): Name of the first numeric variable.
            b_name (str): Name of the second numeric variable.
            title (str): Title for the plot. Optional.

        Returns:
            None
        """
        self._visualizer.scatterplot(data=self._data, x=a_name, y=b_name, title=title)
