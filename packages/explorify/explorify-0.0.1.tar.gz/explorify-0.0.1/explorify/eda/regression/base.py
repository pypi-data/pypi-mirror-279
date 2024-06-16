#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/regression/base.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday August 22nd 2023 07:44:59 pm                                                #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Base classes used throughout the inferential package."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from explorify import DataClass
from explorify.utils.io import IOService

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
ANALYSIS_TYPES = {
    "bivariate": "Bivariate",
    "multivariate": "Multivariate",
}


# ------------------------------------------------------------------------------------------------ #
@dataclass
class RegressionResult(DataClass):
    name: str = None
    intercept: float = None
    intercept_ci: float = None
    intercept_stderr: float = None
    slope: float = None
    slope_ci: float = None
    slope_stderr: float = None
    df_regression: int = None
    df_residual: int = None
    df_total: int = None
    rvalue: float = None
    pvalue: float = None

    @abstractmethod
    def report(self) -> str:
        """Reports results in APA Style"""

    def _report_statistic(self, fvalue: float) -> str:  # pragma no cover
        """Removes leading zero and rounds to 2 decimals"""
        return str(fvalue).lstrip("0")

    def _report_rvalue(self, r: float) -> str:  # pragma no cover
        """Removes leading zero and rounds to 2 decimals"""
        stat = round(r * 100, 2)
        return str(stat).lstrip("0")

    def _report_pvalue(self, pvalue: float) -> str:  # pragma: no cover
        """Rounds the pvalue in accordance with the APA Style Guide 7th Edition"""
        if pvalue < 0.001:
            return "p<.001"
        else:
            return "p=" + (str(round(pvalue, 3))).lstrip("0")


# ------------------------------------------------------------------------------------------------ #
class RegressionAnalyzer(ABC):
    """Base class for Regression Analyzer classes"""

    def __init__(self, io: IOService = IOService, *args, **kwargs) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    @abstractmethod
    def result(self) -> RegressionResult:
        """Returns a Statistical Test Result object."""

    @abstractmethod
    def run(self) -> None:
        """Performs the statistical test and creates a result object."""
