#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /explorify/eda/stats/inferential/variance.py                                        #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 11:41:00 pm                                                 #
# Modified   : Thursday June 13th 2024 11:12:14 am                                                 #
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
class LeveneTestResult(StatTestResult):
    name: str = "Levene's Test of Equal Variances"
    a_name: str = None
    b_name: str = None
    data: pd.DataFrame = None
    dof: tuple = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        title = f"Levene test of equal variance of {self.b_name} within {self.a_name}"
        self.visualizer.boxplot(x=self.a, y=self.b, data=self.data, title=title)

    @property
    def report(self) -> str:
        if self.pvalue > self.alpha:  # pragma: no cover
            return f"{self.name} was conducted to test homogeniety of {self.b_name} variances among {self.a_name}. {self.name} found that {self.a_name} violated the assumption of homogeniety for the the {self.b_name} variable {self.statistic}({self.dof})={self.value},p={round(self.pvalue,4)}"
        else:
            return f"{self.name} was conducted to test homogeniety of {self.b_name} variances among {self.a_name}. {self.name} found that {self.a_name} was homogeneous among the {self.b_name} variable {self.statistic}({self.dof})={self.value},p={round(self.pvalue,4)}"


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class LeveneTest(StatisticalTest):
    """Perform Levene test for equal variances.

    The Levene test tests the null hypothesis that all input samples are from populations with
    equal variances.  Levene's test is an alternative to Bartlett's test bartlett in the case where
    there are significant deviations from normality.

    Args:
        a_name: (str): Name of a categorical variable representing groups.
        b_name: (str): Name of a numeric variable to be tested.
        data (pd.DataFrame): DataFrame containing the columns a and b.
        alpha (float): The level of statistical significance for inference.
    """

    __id = "levene"

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
        """Executes the Test."""
        data_clean = self._data.dropna(subset=[self._a_name, self._b_name])[
            [self._a_name, self._b_name]
        ]
        grouped_data = data_clean.groupby(self._a_name)[self._b_name]
        groups = [group for _, group in grouped_data]

        statistic, pvalue = stats.levene(*groups)

        dof = (
            len(groups) - 1,
            len(self._data) - len(groups),
        )

        # Create the result object.
        self._result = LeveneTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            a_name=self._a_name,
            b_name=self._b_name,
            data=self._data,
            dof=dof,
            value=statistic,
            alpha=self._alpha,
            pvalue=pvalue,
        )
