#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/data_prep/outliers.py                                                #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 08:05:10 pm                                                 #
# Modified   : Friday June 14th 2024 09:26:11 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from explorify.eda.data_prep.base import BaseOutlierHandler


# ------------------------------------------------------------------------------------------------ #
class OutlierHandlerFactory:
    @staticmethod
    def get_handler(method: str, data: pd.DataFrame) -> BaseOutlierHandler:
        """
        Factory method to get the appropriate outlier handler.

        Parameters:
        -----------
        method : str
            The method to use for outlier detection (e.g., 'zscore', 'iqr', 'custom').
        data : pd.DataFrame
            The dataset containing potential outliers.

        Returns:
        --------
        BaseOutlierHandler
            The outlier handler object.
        """
        if method == "zscore":
            return ZScoreOutlierHandler(data)
        elif method == "iqr":
            return IQROutlierHandler(data)
        elif method == "custom":
            return CustomThresholdOutlierHandler(data)
        else:
            raise ValueError(f"Unknown method: {method}")


# ------------------------------------------------------------------------------------------------ #
class ZScoreOutlierHandler(BaseOutlierHandler):
    """
    A class to handle outliers using the Z-score method.

    Methods:
        remove_outliers(column: str, threshold: float = 3) -> pd.DataFrame:
            Removes outliers based on Z-score method for a specific column.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data)

    def remove_outliers(self, column: str, threshold: float = 3) -> pd.DataFrame:
        """
        Removes outliers based on Z-score method for a specific column.

        Args:
            column (str): The column to apply the Z-score outlier removal to.
            threshold (float, optional): The Z-score threshold above which data points are considered outliers. Default is 3.

        Returns:
            pd.DataFrame: The dataset with outliers removed for the specified column.
        """
        z_scores = np.abs(stats.zscore(self._data[column].dropna()))
        return self._data[z_scores < threshold]


# ------------------------------------------------------------------------------------------------ #
class IQROutlierHandler(BaseOutlierHandler):
    """
    A class to handle outliers using the IQR method.

    Methods:
        remove_outliers(column: str, factor: float = 1.5) -> pd.DataFrame:
            Removes outliers based on the IQR method for a specific column.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data)

    def remove_outliers(self, column: str, factor: float = 1.5) -> pd.DataFrame:
        """
        Removes outliers based on the IQR method for a specific column.

        Args:
            column (str): The column to apply the IQR outlier removal to.
            factor (float, optional): The factor to multiply the IQR by to determine the upper and lower bounds for outliers. Default is 1.5.

        Returns:
            pd.DataFrame: The dataset with outliers removed for the specified column.
        """
        Q1 = self._data[column].quantile(0.25)
        Q3 = self._data[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - (factor * IQR)
        upper_bound = Q3 + (factor * IQR)
        return self._data[
            (self._data[column] >= lower_bound) & (self._data[column] <= upper_bound)
        ]


# ------------------------------------------------------------------------------------------------ #
class CustomThresholdOutlierHandler(BaseOutlierHandler):
    """
    A class to handle outliers using custom thresholds.

    Methods:
        remove_outliers(column: str, lower_bound: float, upper_bound: float) -> pd.DataFrame:
            Removes outliers based on custom thresholds for a specified column.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data)

    def remove_outliers(
        self, column: str, lower_bound: float = None, upper_bound: float = None
    ) -> pd.DataFrame:
        """
        Removes outliers based on custom thresholds for a specified column.

        Args:
            column (str): The column to apply the custom thresholds to.
            lower_bound (float): The lower bound to use for identifying outliers.
            upper_bound (float): The upper bound to use for identifying outliers.

        Returns:
            pd.DataFrame: The dataset with outliers removed for the specified column.
        """
        data = self._data.copy()
        if lower_bound is not None:
            data = data.loc[data[column] >= lower_bound]
        if upper_bound is not None:
            data = data.loc[data[column] <= upper_bound]
        return data
