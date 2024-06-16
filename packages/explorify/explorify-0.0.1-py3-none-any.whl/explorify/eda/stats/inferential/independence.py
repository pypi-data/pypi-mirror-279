#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/stats/inferential/independence.py                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday June 9th 2024 11:12:14 am                                                    #
# Modified   : Thursday June 13th 2024 11:11:50 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
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
class ChiSquareIndependenceTestResult(StatTestResult):
    name: str = f"X\u00b2 Test of Independence"  # noqa
    dof: int = None
    data: pd.DataFrame = None
    a_name: str = None
    b_name: str = None
    visualizer: Visualizer = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.x2testplot(
            statistic=self.value,
            dof=self.dof,
            result=self.result,
            alpha=self.alpha,
        )

    @property
    def report(self) -> str:
        return f"X\u00b2 Test of Independence\n{self.a_name.capitalize()} and {self.b_name.capitalize()}\nX\u00b2({self.dof}, N={self.data.shape[0]})={round(self.value,2)}, {self._report_pvalue(self.pvalue)}."


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class ChiSquareIndependenceTest(StatisticalTest):
    """Chi-Square Test of Independence

    The Chi-Square test of independence is used to determine if there is a significant relationship between two nominal (categorical) variables.  The frequency of each category for one nominal variable is compared across the categories of the second nominal variable.
    """

    __id = "x2ind"

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        a_name: str = None,
        b_name: str = None,
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._data = data
        self._a_name = a_name
        self._b_name = b_name
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

        obs = stats.contingency.crosstab(
            self._data[self._a_name], self._data[self._b_name]
        )

        statistic, pvalue, dof, exp = stats.chi2_contingency(obs[1])

        # Create the result object.
        self._result = ChiSquareIndependenceTestResult(
            H0=self._profile.H0,
            statistic="X\u00b2",
            hypothesis=self._profile.hypothesis,
            dof=dof,
            value=statistic,
            pvalue=pvalue,
            data=self._data,
            a_name=self._a_name,
            b_name=self._b_name,
            alpha=self._alpha,
        )
