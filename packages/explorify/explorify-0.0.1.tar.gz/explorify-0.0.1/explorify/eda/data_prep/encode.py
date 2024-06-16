#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/data_prep/encode.py                                                  #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 08:05:57 pm                                                 #
# Modified   : Saturday June 15th 2024 03:13:33 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Encoding Module"""
import numpy as np
import pandas as pd
from category_encoders import TargetEncoder
from sklearn.preprocessing import LabelEncoder

from explorify.eda.data_prep.base import BaseEncoder


# ------------------------------------------------------------------------------------------------ #
class EncoderFactory:
    """
    Factory class to create encoder objects.

    Methods:
        get_encoder(method: str, data: pd.DataFrame) -> BaseEncoder:
            Factory method to get the appropriate encoder.
    """

    @staticmethod
    def get_encoder(method: str, data: pd.DataFrame) -> BaseEncoder:
        """
        Factory method to get the appropriate encoder.

        Args:
            method (str): The method to use for encoding (e.g., 'onehot', 'label', 'target').
            data (pd.DataFrame): The dataset containing categorical variables to encode.

        Returns:
            BaseEncoder: The encoder object.
        """
        if method == "onehot":
            return AOneHotEncoder(data)
        elif method == "label":
            return ALabelEncoder(data)
        elif method == "target":
            return ATargetEncoder(data)
        else:
            raise ValueError(f"Unknown method: {method}")


# ------------------------------------------------------------------------------------------------ #
class AOneHotEncoder(BaseEncoder):
    """
    A class to handle one-hot encoding of categorical variables.

    Methods:
        encode(columns: list[str]) -> pd.DataFrame:
            Encodes the specified columns using one-hot encoding.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def encode(self, columns: list[str] = None) -> pd.DataFrame:
        """
        Encodes the specified columns using one-hot encoding.

        Args:
            columns (list[str]): The columns to apply one-hot encoding to. Optional.
                 If columns is None then all the columns with object, string,
                 or category dtype will be converted.

        Returns:
            pd.DataFrame: The dataset with the specified columns one-hot encoded.
        """
        return pd.get_dummies(self._data, columns=columns, dtype=int)


# ------------------------------------------------------------------------------------------------ #
class ALabelEncoder(BaseEncoder):
    """
    A class to handle label encoding of categorical target variables.

    Methods:
        encode(columns: list[str]) -> pd.DataFrame:
            Encodes the specified columns using label encoding.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def encode(self, column: str) -> pd.DataFrame:
        """
        Encodes the specified column using label encoding.

        Args:
            column (str): The target column to encode.

        Returns:
            pd.DataFrame: The dataset with the specified column label encoded.
        """
        le = LabelEncoder()
        self._data[column] = le.fit_transform(self._data[column])
        return self._data


# ------------------------------------------------------------------------------------------------ #


class ATargetEncoder(BaseEncoder):
    """
    A class to handle target encoding of categorical variables.

    Target encoding assumes a dataset with a discrete or continuous target variable.

    Methods:
        encode(columns: list[str], target: str) -> pd.DataFrame:
            Encodes the specified columns using target encoding.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def encode(self, target: str, columns: list[str] = None) -> pd.DataFrame:
        """
        Encodes the specified columns using target encoding.

        Args:
            columns (list[str]): The columns to apply target encoding to. Optional.
                If columns is None, all non-numeric columns are encoded.
            target (str): The target variable for calculating means.

        Returns:
            pd.DataFrame: The dataset with the specified columns target encoded.
        """
        te = TargetEncoder()
        if columns is None:
            columns = self._data.select_dtypes(exclude=[np.number]).columns

        self._data[columns] = te.fit_transform(self._data[columns], self._data[target])
        return self._data
