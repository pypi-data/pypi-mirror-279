#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/data_prep/base.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 08:05:23 pm                                                 #
# Modified   : Friday June 14th 2024 08:36:48 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod

import pandas as pd

# ------------------------------------------------------------------------------------------------ #


class DataPrep(ABC):  # pragma: no cover
    """
    Abstract base class for data preparation tasks.

    This class provides a blueprint for data preparation operations
    that need to be performed on a given dataset. Subclasses should
    implement the `prep` method to define specific data preparation
    tasks such as handling missing values, normalizing data, encoding
    categorical variables, etc.

    Attributes:
    -----------
    data : pd.DataFrame
        The dataset to be prepared.

    Methods:
    --------
    prep(*args, **kwargs) -> pd.DataFrame:
        Conducts the data preparation task. This method must be implemented
        by subclasses to perform specific data preparation operations.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the DataPrep object with the given dataset.

        Parameters:
        -----------
        data : pd.DataFrame
            The dataset to be prepared.
        """
        super().__init__()
        self._data = data

    @abstractmethod
    def prep(self, *args, **kwargs) -> pd.DataFrame:
        """
        Conducts the data preparation task.

        This abstract method should be overridden by subclasses to perform
        specific data preparation operations.

        Returns:
        --------
        pd.DataFrame
            The prepared dataset.
        """
        pass


# ------------------------------------------------------------------------------------------------ #
class BaseOutlierHandler(ABC):  # pragma: no cover
    """
    Abstract base class for data preparation tasks.

    This class provides a blueprint for data preparation operations
    that need to be performed on a given dataset. Subclasses should
    implement the `prep` method to define specific data preparation
    tasks such as handling missing values, normalizing data, encoding
    categorical variables, etc.

    Attributes:
        data (pd.DataFrame): The dataset to be prepared.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the BaseOutlierHandler with the given dataset.

        Args:
            data (pd.DataFrame): The dataset containing potential outliers.
        """
        self._data = data

    @abstractmethod
    def remove_outliers(self, column: str, *args, **kwargs) -> pd.DataFrame:
        """
        Abstract method to remove outliers. Must be implemented by subclasses.

        Args:
            column (str): The column to apply the outlier removal technique to.

        Returns:
            pd.DataFrame: The dataset with outliers removed.
        """
        pass


# ------------------------------------------------------------------------------------------------ #
class BaseEncoder(ABC):  # pragma: no cover
    """
    Abstract base class for encoding categorical variables.

    This class provides a blueprint for encoding operations that need to be performed on a
    given dataset. Subclasses should implement the `encode` method to define specific
    encoding techniques such as one-hot encoding, label encoding, target encoding, etc.

    Attributes:
        data (pd.DataFrame): The dataset to be encoded.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the BaseEncoder with the given dataset.

        Args:
            data (pd.DataFrame): The dataset containing categorical variables to encode.
        """
        self._data = data

    @abstractmethod
    def encode(self, columns: list[str], *args, **kwargs) -> pd.DataFrame:
        """
        Abstract method to encode categorical variables. Must be implemented by subclasses.

        Args:
            columns (list[str]): The columns to apply the encoding technique to.

        Returns:
            pd.DataFrame: The dataset with the specified columns encoded.
        """
        pass
