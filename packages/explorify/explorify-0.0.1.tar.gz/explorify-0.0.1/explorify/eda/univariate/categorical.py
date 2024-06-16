#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/univariate/categorical.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 8th 2024 11:45:10 am                                                  #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dependency_injector.wiring import Provide, inject

from explorify.container import VisualizeContainer
from explorify.eda.univariate.base import UnivariateCategoricalAnalyzer
from explorify.eda.visualize.visualizer import Visualizer


# ------------------------------------------------------------------------------------------------ #
#                         CATEGORICAL DESCRIPTIVE STATISTICS                                       #
# ------------------------------------------------------------------------------------------------ #
class UnivariateCategoricalDescriptiveStatisticsAnalyzer(UnivariateCategoricalAnalyzer):
    """Descriptive statistics for a univariate categorical variable.

    Args:
        _data (pd.DataFrame): The DataFrame containing the categorical data.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        self._data = data

    def analyze(self, x: str) -> pd.DataFrame:
        """Calculates descriptive statistics for a specific categorical column.

        Args:
            x (str): The column to be analyzed.

        Returns:
            pd.DataFrame: A DataFrame containing the descriptive statistics.
        """
        self.validate_input(x)
        desc_stats = self._data[x].describe()
        return desc_stats.to_frame()


# ------------------------------------------------------------------------------------------------ #
#                               FREQUENCY ANALYSIS                                                 #
# ------------------------------------------------------------------------------------------------ #
class UnivariateFrequencyAnalyzer(UnivariateCategoricalAnalyzer):
    """Calculates the frequency distribution for categorical data.

    Args:
        _data (pd.DataFrame): The DataFrame containing the categorical data.

    """

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        visualizer: Visualizer = Provide[VisualizeContainer.visualizer],
    ) -> None:
        """
        Initializes the UnivariateFrequencyAnalyzer class.

        Args:
            data (pd.DataFrame): The DataFrame containing the categorical data.
            visualizer (Visualizer): An instance of Visualizer for plotting,
                injected via dependency injection.
        """
        super().__init__(data=data)
        self._visualizer = visualizer

    def analyze(self, x: str, n: int = None) -> pd.DataFrame:
        """
        Calculates the frequency distribution for categorical data.

        This yields frequency distribution, including proportions and
        cumulative counts. For large categories, the method takes
        an optional value, 'n', which specifies the top n categories
        to report, based on frequency.

        Args:
            x (str): The column in the dataset containing the categorical
                variable.
            n (int, optional): The number of top categories to report. If not
                specified, the method reports all categories.

        Returns:
            pd.DataFrame: A DataFrame containing the frequency distribution.
        """
        self.validate_input(x)
        # Calculate frequency distribution
        freq = self._data[x].value_counts().reset_index()
        freq.columns = [x, "Count"]

        # Calculate cumulative count and proportions
        freq["Cumulative Count"] = freq["Count"].cumsum()
        total_count = freq["Count"].sum()
        freq["Proportion"] = freq["Count"] / total_count
        freq["Cumulative Proportion"] = freq["Proportion"].cumsum()

        if n is None:
            return freq
        else:
            # Top N rows
            top_n = freq.head(n).copy()

            # Row for the rest of the dataset
            if len(freq) > n:
                rest_count = freq.iloc[n:]["Count"].sum()
                rest_cumulative_count = top_n["Cumulative Count"].iloc[-1] + rest_count
                rest_proportion = rest_count / total_count
                rest_cumulative_proportion = (
                    1.0  # because it's the rest, it covers the remaining percentage
                )
                rest_row = pd.DataFrame(
                    {
                        x: [f"Rest of {x}"],
                        "Count": [rest_count],
                        "Cumulative Count": [rest_cumulative_count],
                        "Proportion": [rest_proportion],
                        "Cumulative Proportion": [rest_cumulative_proportion],
                    }
                )
                top_n = pd.concat([top_n, rest_row], ignore_index=True, axis=0)

            # Total row
            total_row = pd.DataFrame(
                {
                    x: ["Total"],
                    "Count": [total_count],
                    "Cumulative Count": [total_count],
                    "Proportion": [1.0],
                    "Cumulative Proportion": [1.0],
                }
            )
            top_n = pd.concat([top_n, total_row], ignore_index=True, axis=0)

            return top_n

    def plot(
        self, x: str, n: int, ax: plt.Axes = None, title: str = None, orient: str = "h"
    ) -> plt.Axes:
        """
        Generates a bar plot of the top-n frequencies.

        Args:
            x (str): The column in the dataset containing the categorical variable.
            n (int): The number of top categories to plot.
            ax (plt.Axes, optional): The matplotlib axes object to plot on. If not
                provided, a new axes object is created.
            title (str, optional): The title of the plot.
            orient (str, optional): The orientation of the plot, either 'h' for
                horizontal or 'v' for vertical. Default is 'h'.

        Returns:
            plt.Axes: The matplotlib axes object with the plot.
        """
        frequencies = self.analyze(x=x, n=n)
        if orient == "h":
            return self._visualizer.barplot(
                data=frequencies,
                x=x,
                y="Count",
                ax=ax,
                title=title,
                rotate_ticks=["x", 45],
            )
        else:
            return self._visualizer.barplot(
                data=frequencies,
                x="Count",
                y=x,
                ax=ax,
                title=title,
            )


# ------------------------------------------------------------------------------------------------ #
#                                   DIVERSITY INDICES                                              #
# ------------------------------------------------------------------------------------------------ #
class UnivariateDiversityAnalyzer(UnivariateCategoricalAnalyzer):
    """Calculates the frequency distribution for categorical data.

    Args:
        _data (pd.DataFrame): The DataFrame containing the categorical data.

    """

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        visualizer: Visualizer = Provide[VisualizeContainer.visualizer],
    ) -> None:
        """
        Initializes the UnivariateDiversityAnalyzer class.

        Args:
            data (pd.DataFrame): The DataFrame containing the categorical data.
            visualizer (Visualizer): An instance of Visualizer for plotting,
                injected via dependency injection.
        """
        super().__init__(data=data)
        self._visualizer = visualizer

    def analyze(self, x: str) -> pd.Series:
        """
        Calculates diversity indices for a specific categorical column.

        This method calculates Shannon Entropy and Simpson Index to measure
        the diversity of the categorical data.

        Args:
            x (str): The column to be analyzed.

        Returns:
            pd.Series: A Series containing the diversity indices.
        """
        self.validate_input(x)

        def shannon_entropy(series):
            counts = series.value_counts()
            probs = counts / len(series)
            return -sum(probs * np.log2(probs))

        def simpson_index(series):
            counts = series.value_counts()
            n = len(series)
            return 1 - sum((counts / n) ** 2)

        indices = pd.Series(
            {
                "Shannon Entropy": shannon_entropy(self._data[x]),
                "Simpson Index": simpson_index(self._data[x]),
            }
        )
        return indices


# ------------------------------------------------------------------------------------------------ #
#                                   INEQUALITY ANALYSIS                                            #
# ------------------------------------------------------------------------------------------------ #
class UnivariateInequalityAnalyzer(UnivariateCategoricalAnalyzer):
    """
    Performs inequality analysis for categorical data.

    Args:
        _data (pd.DataFrame): The DataFrame containing the categorical data.
    """

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        visualizer: Visualizer = Provide[VisualizeContainer.visualizer],
    ) -> None:
        """
        Initializes the UnivariateInequalityAnalyzer class.

        Args:
            data (pd.DataFrame): The DataFrame containing the categorical data.
            visualizer (Visualizer): An instance of Visualizer for plotting,
                injected via dependency injection.
        """
        super().__init__(data=data)
        self._visualizer = visualizer

    def analyze(self, x: str) -> pd.Series:
        """
        Calculates inequality measures for a specific categorical column.

        This method calculates the Gini Coefficient to measure the inequality
        of the categorical data.

        Args:
            x (str): The column to be analyzed.

        Returns:
            pd.Series: A Series containing the inequality measures.
        """
        self.validate_input(x)

        def gini_coefficient(series):
            counts = series.value_counts()
            n = len(series)
            sorted_counts = counts.sort_values()
            cum_counts = sorted_counts.cumsum()
            gini = 1 - (2 * cum_counts - sorted_counts).sum() / (n * counts.sum())
            return gini

        measures = pd.Series({"Gini Coefficient": gini_coefficient(self._data[x])})
        return measures


# ------------------------------------------------------------------------------------------------ #
#                                   ENTROPY ANALYSIS                                               #
# ------------------------------------------------------------------------------------------------ #
class UnivariateEntropyAnalyzer(UnivariateCategoricalAnalyzer):
    """
    Performs entropy analysis for categorical data.

    Args:
        _data (pd.DataFrame): The DataFrame containing the categorical data.
    """

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        visualizer: Visualizer = Provide[VisualizeContainer.visualizer],
    ) -> None:
        """
        Initializes the UnivariateEntropyAnalyzer class.

        Args:
            data (pd.DataFrame): The DataFrame containing the categorical data.
            visualizer (Visualizer): An instance of Visualizer for plotting,
                injected via dependency injection.
        """
        super().__init__(data=data)
        self._visualizer = visualizer

    def analyze(self, x: str) -> pd.Series:
        """
        Calculates entropy for a specific categorical column.

        This method calculates the Shannon Entropy to measure the uncertainty
        or diversity of the categorical data.

        Args:
            x (str): The column to be analyzed.

        Returns:
            pd.Series: A Series containing the entropy value.
        """
        self.validate_input(x)

        def shannon_entropy(series):
            counts = series.value_counts()
            probs = counts / len(series)
            return -sum(probs * np.log2(probs))

        entropy_value = pd.Series({"Entropy": shannon_entropy(self._data[x])})
        return entropy_value


# ------------------------------------------------------------------------------------------------ #
#                                   SPREAD ANALYSIS                                                #
# ------------------------------------------------------------------------------------------------ #
class UnivariateSpreadAnalyzer(UnivariateCategoricalAnalyzer):
    """
    Performs spread analysis for categorical data.

    Args:
        _data (pd.DataFrame): The DataFrame containing the categorical data.
    """

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        visualizer: Visualizer = Provide[VisualizeContainer.visualizer],
    ) -> None:
        """
        Initializes the UnivariateSpreadAnalyzer class.

        Args:
            data (pd.DataFrame): The DataFrame containing the categorical data.
            visualizer (Visualizer): An instance of Visualizer for plotting,
                injected via dependency injection.
        """
        super().__init__(data=data)
        self._visualizer = visualizer

    def analyze(self, x: str) -> pd.Series:
        """
        Calculates spread measures for a specific categorical column.

        This method calculates the spread of the categorical data by
        finding the difference between the maximum and minimum counts
        of the categories.

        Args:
            x (str): The column to be analyzed.

        Returns:
            pd.Series: A Series containing the spread measure.
        """
        self.validate_input(x)

        spread_value = pd.Series(
            {
                "Spread": self._data[x].value_counts().max()
                - self._data[x].value_counts().min()
            }
        )
        return spread_value
