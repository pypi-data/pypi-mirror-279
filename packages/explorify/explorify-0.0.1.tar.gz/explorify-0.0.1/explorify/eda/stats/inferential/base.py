#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/stats/inferential/base.py                                            #
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
from explorify.eda.stats.inferential.profile import StatTestProfile
from explorify.utils.io import IOService

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
ANALYSIS_TYPES = {
    "univariate": "Univariate",
    "bivariate": "Bivariate",
    "multivariate": "Multivariate",
}


# ------------------------------------------------------------------------------------------------ #
@dataclass
class StatTestResult(DataClass):
    name: str = None
    hypothesis: str = None
    H0: str = None
    statistic: str = None
    value: float = 0
    pvalue: float = 0
    alpha: float = 0.05

    @property
    @abstractmethod
    def report(self) -> str:
        """Reports results in APA Style"""

    def _report_alpha(self) -> str:
        a = int(self.alpha * 100)
        return f"significant at {a}%."

    def _report_statistic(self, statistic: float) -> str:  # pragma no cover
        """Removes leading zero and rounds to 2 decimals"""
        stat = round(statistic, 2)
        return (str(stat)).lstrip("0")

    def _report_pvalue(self, pvalue: float) -> str:  # pragma: no cover
        """Rounds the pvalue in accordance with the APA Style Guide 7th Edition"""
        if pvalue < 0.001:
            return "p<.001"
        else:
            return "p=" + (str(round(pvalue, 3))).lstrip("0")


# ------------------------------------------------------------------------------------------------ #
class StatisticalTest(ABC):
    """Base class for Statistical Tests"""

    def __init__(self, io: IOService = IOService, *args, **kwargs) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    @abstractmethod
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""

    @property
    @abstractmethod
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""

    @abstractmethod
    def run(self) -> None:
        """Performs the statistical test and creates a result object."""


# ------------------------------------------------------------------------------------------------ #
class StatAnalyzer(ABC):
    """Base class for Statistical Measurer classes"""

    def __init__(self, io: IOService = IOService, *args, **kwargs) -> None:
        self._io = io
        self._logger = logging.getLogger(f"{self.__class__.__name__}")

    @property
    @abstractmethod
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""

    @abstractmethod
    def run(self) -> None:
        """Performs the statistical test and creates a result object."""
