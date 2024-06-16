#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /explorify/eda/stats/inferential/gof.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Tuesday June 6th 2023 01:45:05 am                                                   #
# Modified   : Thursday June 13th 2024 11:37:33 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import pandas as pd
from dependency_injector.wiring import Provide, inject
from scipy import stats

from explorify.container import VisualizeContainer
from explorify.eda.stats.inferential.base import StatisticalTest, StatTestResult
from explorify.eda.stats.inferential.profile import StatTestProfile
from explorify.eda.visualize.visualizer import Visualizer


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class KSTestResult(StatTestResult):
    """Encapsulates the hypothesis test results."""

    name: str = "Kolmogorov-Smirnov Test"
    a_name: str = None
    b_name: str = None
    data: pd.DataFrame = None
    n: int = None
    advisory: str = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.kstestplot(
            statistic=self.value,
            n=len(self._data[self.a_name]),
            result=self.result,
            alpha=self.alpha,
        )

    @property
    def report(self) -> str:
        """Reports the result in APA style."""
        result = f"Kolmogorov-Smirnov Goodness of Fit\nD({self.n})={round(self.value,4)}, p={round(self.pvalue,3)}"
        return result


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class KSTest(StatisticalTest):
    """Performs the (one-sample or two-sample) Kolmogorov-Smirnov test for goodness of fit.

    The one-sample test compares the underlying distribution F(x) of a sample against a given
    distribution G(x). The two-sample test compares the underlying distributions of
    two independent samples. Both tests are valid only for continuous distributions.

    Args:
        a_name (str): Name of a continuous column in the dataset
        b_name (str): Name of a continuous column in the dataset
        data (pd.DataFrame): DataFrame containing the two columns.

    """

    __id = "kstest"

    def __init__(
        self,
        a_name: str,
        b_name: str,
        data: pd.DataFrame,
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._a_name = a_name
        self._b_name = b_name
        self._data = data
        self._alpha = alpha
        self._profile = StatTestProfile.create(self.__id)
        self._result = None

    @property
    def profile(self) -> StatTestProfile:
        """Returns the statistical test profile."""
        return self._profile

    @property
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        n = len(self._data)

        # Conduct the two-sided ks test
        try:
            result = stats.kstest(
                rvs=self._data[self._a_name].values,
                cdf=self._data[self._b_name].values,
                alternative="two-sided",
            )
        except KeyError:
            result = stats.kstest(
                rvs=self._data[self._a_name].values,
                cdf=self._b_name,
                alternative="two-sided",
            )
        except Exception as e:  # pragma: no cover
            msg = f"Invalid arguments {self._a_name}, {self._b_name}\n{e}"
            self._logger.exception(msg)
            raise

        advisory = None
        if len(self._data[self._a_name]) < 50:
            advisory = "Note: The Kolmogorov-Smirnov Test requires a sample size N > 50. For smaller sample sizes, the Shapiro-Wilk test should be considered."
        if len(self._data[self._a_name]) > 1000:
            advisory = "Note: The Kolmogorov-Smirnov Test on large sample sizes may lead to rejections of the null hypothesis that are statistically significant, yet practically insignificant."

        # Create the result object.
        self._result = KSTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            value=result.statistic,
            pvalue=result.pvalue,
            a_name=self._a_name,
            b_name=self._b_name,
            data=self._data,
            n=n,
            advisory=advisory,
            alpha=self._alpha,
        )
