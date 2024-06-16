#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/univariate/numeric.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 8th 2024 04:29:10 pm                                                  #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Univariate Numeric Module"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats

from explorify.eda.univariate.base import UnivariateNumericAnalyzer


# ------------------------------------------------------------------------------------------------ #
#                               NUMERIC DESCRIPTIVE STATISTICS                                     #
# ------------------------------------------------------------------------------------------------ #
class UnivariateNumericDescriptiveStatistics(UnivariateNumericAnalyzer):
    """
    Provides univariate descriptive statistics for numeric variables.

    Args:
        data (pd.DataFrame): The DataFrame containing the numeric data for analysis.

    """

    def __init__(self, data: pd.DataFrame):
        super().__init__(data=data)

    def analyze(self, x: str) -> pd.DataFrame:
        """
        Calculate descriptive statistics including mean, median, mode, range,
        standard deviation, skewness, kurtosis, and quantiles for a specified column.

        Args:
            x (str): The column name of the numeric data to analyze.

        Returns:
        --------
        pd.DataFrame
            A DataFrame containing the descriptive statistics.
        """
        self.validate_input(x)
        series = self._data[x]
        df = series.describe(percentiles=[0.25, 0.5, 0.75]).to_frame().T
        df["variance"] = self._data[x].var()
        df["range"] = df["max"] - df["min"]
        df["skewness"] = stats.skew(series)
        df["kurtosis"] = stats.kurtosis(series)

        # Mode handling
        mode_result = stats.mode(series)
        df["mode"] = mode_result.mode if mode_result.count > 0 else np.nan

        return df.T


# ------------------------------------------------------------------------------------------------ #
#                             INTER-QUARTILE RANGE ANALYSIS                                        #
# ------------------------------------------------------------------------------------------------ #
class UnivariateIQRAnalyzer(UnivariateNumericAnalyzer):
    """
    Performs Interquartile Range (IQR) analysis for numerical data.

    Args:
        data (pd.DataFrame): The DataFrame containing the numerical data.
    """

    def __init__(self, data: pd.DataFrame):
        super().__init__(data=data)

    def analyze(self, x: str) -> float:
        """
        Calculate the interquartile range of the specified column.

        Args:
            x (str): The column name of the numeric data to analyze.

        Returns:
            float: The interquartile range of the data.
        """
        self.validate_input(x)
        series = self._data[x]
        return stats.iqr(series)

    def plot(self, x: str, title: str = None, ax: plt.Axes = None) -> plt.Axes:
        """
        Generate a boxplot for the specified column.

        Args:
            x (str): The column name of the numeric data to plot.
            title (str, optional): The title of the plot. Default is None.
            ax (plt.Axes, optional): The matplotlib axes object to plot on. If not provided, a new axes object is created.

        Returns:
            plt.Axes: The matplotlib axes object with the plot.
        """
        return self._visualizer.boxplot(data=self._data, x=x, ax=ax, title=title)


# ------------------------------------------------------------------------------------------------ #
#                             MEDIAN ABSOLUTE DEVIATION ANALYSIS                                   #
# ------------------------------------------------------------------------------------------------ #
class UnivariateMADAnalyzer(UnivariateNumericAnalyzer):
    """
    Performs Mean Absolute Deviation (MAD) analysis for numerical data.

    Args:
        data (pd.DataFrame): The DataFrame containing the numerical data.
    """

    def __init__(self, data: pd.DataFrame):
        super().__init__(data=data)

    def analyze(self, x: str) -> float:
        """
        Calculate the mean absolute deviation of the specified column.

        Args:
            x (str): The column name of the numeric data to analyze.

        Returns:
            float: The mean absolute deviation of the data.
        """
        self.validate_input(x)
        series = self._data[x]
        return np.mean(np.abs(series - np.mean(series)))


# ------------------------------------------------------------------------------------------------ #
#                           COEFFICIENT OF VARIATION ANALYSIS                                      #
# ------------------------------------------------------------------------------------------------ #
class UnivariateCoefficientVariationAnalyzer(UnivariateNumericAnalyzer):
    """
    Calculate the coefficient of variation of the specified column.

    Args:
        data (pd.DataFrame): The DataFrame containing the numerical data.
    """

    def __init__(self, data: pd.DataFrame):
        super().__init__(data=data)

    def analyze(self, x: str) -> float:
        """
        Calculate the coefficient of variation of the specified column.

        Args:
        -----
        x : str
            The column name of the numeric data to analyze.

        Returns:
        --------
        float
            The coefficient of variation of the data, expressed as a percentage.
        """
        self.validate_input(x)
        series = self._data[x]
        mean = np.mean(series)
        std_dev = np.std(series, ddof=1)
        return (std_dev / mean) * 100


# ------------------------------------------------------------------------------------------------ #
#                                STANDARD ERROR ANALYSIS                                           #
# ------------------------------------------------------------------------------------------------ #
class UnivariateStdErrorAnalyzer(UnivariateNumericAnalyzer):
    """
    Calculate the standard error of the mean of the specified column.

    Args:
        data (pd.DataFrame): The DataFrame containing the numerical data.
    """

    def __init__(self, data: pd.DataFrame):
        super().__init__(data=data)

    def analyze(self, x: str) -> float:
        """
        Calculate the standard error of the mean of the specified column.

        Args:
        -----
        x : str
            The column name of the numeric data to analyze.

        Returns:
        --------
        float
            The standard error of the mean of the data.
        """
        self.validate_input(x)
        series = self._data[x]
        std_dev = np.std(series, ddof=1)
        return std_dev / np.sqrt(len(series))
