#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/overview.py                                                          #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday June 8th 2024 10:54:53 am                                                  #
# Modified   : Sunday June 9th 2024 03:20:13 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Dataset Overview Module"""
from functools import cache

import pandas as pd

from explorify.utils.print import Printer

# ------------------------------------------------------------------------------------------------ #


class Overview:
    """Provides an overview of a pandas DataFrame.

    The Overview class contains methods to generate and print summary statistics and information
    about a DataFrame, such as its shape, memory usage, and column-specific details.

    Args:
        _data (pd.DataFrame): The DataFrame to analyze.
        printer_cls (type[Printer], optional): The Printer class to use for output. Defaults to Printer.
    """

    def __init__(
        self, data: pd.DataFrame, printer_cls: type[Printer] = Printer
    ) -> None:
        """Initializes the Overview class with the given DataFrame and Printer class."""
        self._data = data
        self._printer = printer_cls()

    def summary(self) -> None:
        """Prints a summary of the DataFrame.

        This method prints a summary of the DataFrame including the number of rows, columns, and the
        size in megabytes.

        Returns:
            None
        """
        summary = {
            "Rows": self._data.shape[0],
            "Columns": self._data.shape[1],
            "Size (Mb)": round(
                self._data.memory_usage(deep=True).sum() / (1024 * 1024), 2
            ),
        }
        self._printer.print_dict(data=summary, title="Dataset Summary")

    @cache
    def info(self) -> pd.DataFrame:
        """Generates a DataFrame with detailed information about each column.

        This method returns a DataFrame containing detailed information about each column,
        including data type, number of complete cases, number of missing values, completeness,
        number of unique values, number of duplicate values, uniqueness, and memory usage in bytes.

        Returns:
            pd.DataFrame: A DataFrame with detailed information about each column.
        """
        info = pd.DataFrame()
        info["Column"] = self._data.columns
        info["DataType"] = self._data.dtypes.values
        info["Complete"] = self._data.count().values
        info["Null"] = self._data.isna().sum().values
        info["Completeness"] = info["Complete"] / len(self._data)
        info["Unique"] = self._data.nunique().values
        info["Duplicate"] = len(self._data) - info["Unique"]
        info["Uniqueness"] = info["Unique"] / len(self._data)
        info["Size (Bytes)"] = self._data.memory_usage(deep=True, index=False).values
        return info
