#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/multivariate/analysis.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 08:37:22 pm                                                 #
# Modified   : Saturday June 15th 2024 05:21:39 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Multivariate Analaysis Module"""
from typing import List, Union

import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

from explorify.eda.multivariate.base import MultivariateAnalyzer


# ------------------------------------------------------------------------------------------------ #
class ConditionalProbabilityAnalyzer(MultivariateAnalyzer):
    """
    A class to compute conditional probabilities between events in a dataset.

    Attributes:
        _data (pd.DataFrame): Input dataset containing events.

    Methods:
        __init__(self, data: pd.DataFrame) -> None:
            Initializes the ConditionalProbabilityAnalyzer instance.

        calculate_probability(self, event_a: str, event_b: str) -> float:
            Computes the conditional probability P(event_a | event_b).

    Examples:
        >>> # Example dataset
        >>> data = {
        >>>     'Sentiment': [True, True, False, True, False],
        >>>     'Rating': [4, 3, 5, 2, 4],
        >>>     'LongReview': [True, False, True, True, False]
        >>> }
        >>> df = pd.DataFrame(data)
        >>>
        >>> # Create ConditionalProbabilityAnalyzer instance
        >>> analyzer = ConditionalProbabilityAnalyzer(df)
        >>>
        >>> # Calculate and print conditional probabilities
        >>> prob_sentiment_given_rating = analyzer.calculate_probability('Sentiment', 'Rating')
        >>> print(f"P(Sentiment=True | Rating=True) = {prob_sentiment_given_rating:.2f}")
        >>>
        >>> prob_sentiment_given_long_review = analyzer.calculate_probability('Sentiment', 'LongReview')
        >>> print(f"P(Sentiment=True | LongReview=True) = {prob_sentiment_given_long_review:.2f}")

    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def analyze(self, event_a: str, event_b: str) -> float:
        """
        Computes the conditional probability P(event_a | event_b).

        Args:
            event_a (str): Event A for which conditional probability is computed.
            event_b (str): Event B given in the condition.

        Returns:
            float: Conditional probability P(event_a | event_b).
        """
        # Count occurrences of A and B together
        count_a_and_b = np.where(
            (self._data[event_a] is True) and (self._data[event_b] is True), True, False
        ).sum()
        # Count occurrences of B
        count_b = self._data[event_b].sum()

        # Compute conditional probability
        if count_b > 0:
            return count_a_and_b / count_b
        else:  # pragma: no cover
            return 0  # Handle division by zero if necessary


# ------------------------------------------------------------------------------------------------ #
class CovarianceAnalyzer(MultivariateAnalyzer):
    """
    A class to compute the covariance matrix for multivariate analysis.

    Attributes:
        _visualizer (Visualizer): Instance of Visualizer for plotting.

    Methods:
        analyze(**kwargs) -> pd.DataFrame:
            Computes the covariance matrix.

        plot(**kwargs) -> None:
            Plots the covariance matrix.

    Notes:
        This class requires a Visualizer instance provided through dependency injection.

    Raises:
        ValueError: If the provided data is not suitable for covariance analysis.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def analyze(self, **kwargs) -> pd.DataFrame:
        """
        Computes the covariance matrix.

        Args:
            **kwargs: Additional arguments for computing covariance.

        Returns:
            pd.DataFrame: The covariance matrix.
        """
        data = self._data.select_dtypes(include=np.number)
        return data.cov(**kwargs)

    def plot(
        self, cmap: str = "Blues_r", title: str = "Covariance Matrix", **kwargs
    ) -> None:
        """
        Plots the covariance matrix.

        Args:
            **kwargs: Additional arguments for plotting (optional).
        """
        cov_matrix = self.analyze()
        self._visualizer.heatmap(
            data=cov_matrix, annot=True, cmap=cmap, title=title, **kwargs
        )


# ------------------------------------------------------------------------------------------------ #
class VIFAnalyzer(MultivariateAnalyzer):
    """
    A class to compute Variance Inflation Factor (VIF) for multivariate analysis.

    Attributes:
        _visualizer (Visualizer): Instance of Visualizer for plotting.

    Methods:
        analyze(**kwargs) -> pd.DataFrame:
            Computes VIF for each feature.

        plot(**kwargs) -> None:
            Plots the VIF values.

    Notes:
        This class requires a Visualizer instance provided through dependency injection.

    Raises:
        ValueError: If the provided data is not suitable for VIF analysis.

    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def analyze(
        self,
        include: Union[List, None] = None,
        exclude: Union[List, None] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Computes Variance Inflation Factor (VIF) for each feature.

        Args:
            features (list): Features to include in the VIF calculation.
            **kwargs: Additional arguments for computing VIF.

        Returns:
            pd.DataFrame: VIF values for each feature.
        """
        # Relates to numeric variables
        X = self._data.select_dtypes(include=[np.number]).dropna()
        # Exclude variables so listed.
        if exclude is not None:
            X = X.drop(columns=exclude)
        # Include variables so listed.
        if include is not None:
            X = X[include]
        # Create a VIF dataframe containing VIF values for variables of interest.
        vif_data = pd.DataFrame()
        vif_data["Feature"] = X.columns
        vif_data["VIF"] = [
            variance_inflation_factor(X.values, i) for i in range(X.shape[1])
        ]
        return vif_data

    def plot(
        self,
        palette: str = "Blues_r",
        title: str = "Variance Inflation Factor (VIF)",
        **kwargs
    ) -> None:
        """
        Plots the VIF values.

        Args:
            **kwargs: Additional arguments for plotting (optional).
        """
        vif_data = self.analyze()
        title = title
        self._visualizer.barplot(
            x="Feature", y="VIF", data=vif_data, title=title, palette=palette, **kwargs
        )


# ------------------------------------------------------------------------------------------------ #
class CorrelationAnalyzer(MultivariateAnalyzer):
    """
    A class to compute the correlation matrix for multivariate analysis.

    Attributes:
        _visualizer (Visualizer): Instance of Visualizer for plotting.

    Methods:
        analyze(**kwargs) -> pd.DataFrame:
            Computes the correlation matrix.

        plot(**kwargs) -> None:
            Plots the correlation matrix using a heatmap.

    Notes:
        This class requires a Visualizer instance provided through dependency injection.

    Raises:
        ValueError: If the provided data is not suitable for correlation analysis.

    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def analyze(self, **kwargs) -> pd.DataFrame:
        """
        Computes the correlation matrix.

        Args:
            **kwargs: Additional arguments for computing correlation.

        Returns:
            pd.DataFrame: The correlation matrix.
        """
        data = self._data.select_dtypes(include=np.number)
        return data.corr(**kwargs)

    def plot(self, **kwargs) -> None:
        """
        Plots the correlation matrix.

        Args:
            **kwargs: Additional arguments for plotting (optional).
        """
        corr_matrix = self.analyze()
        title = "Correlation Matrix"
        self._visualizer.heatmap(
            data=corr_matrix, annot=True, cmap="crest", title=title, **kwargs
        )
