#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/stats/inferential/rank.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 12th 2024 04:00:36 pm                                                #
# Modified   : Thursday June 13th 2024 11:12:01 am                                                 #
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
class KruskalWallisHTestResult(StatTestResult):
    name: str = "Kruskal-Wallis H Test"
    dof: int = None
    data: pd.DataFrame = None
    a_name: str = None
    b_name: str = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        title = r"Kruskal-Wallis H Test of median {b_name} in {a_name}".format(
            b_name=self.b_name,
            a_name=self.a_name,
        )
        self.visualizer.boxplot(
            x=self.a_name, y=self.b_name, data=self.data, title=title
        )

    @property
    def report(self) -> str:
        if self.pvalue > self.alpha:  # pragma: no cover
            return r"The {name} Test found a non-significant difference in median {a_name} and {b_name}, H({dof})={statistic}, p>0.05.".format(
                name=self.name,
                a_name=self.a_name,
                b_name=self.b_name,
                dof=self.dof,
                statistic=round(self.value, 2),
            )
        else:  # pragma: no cover
            return r"The {name} Test found a significant difference in median {a_name} and {b_name}, H({dof})={statistic}, p>0.05.".format(
                name=self.name,
                a_name=self.a_name,
                b_name=self.b_name,
                dof=self.dof,
                statistic=round(self.value, 2),
            )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class KruskalWallisHTest(StatisticalTest):
    """Calculate the Kruskal-Wallis H Test for the medians of ranked samples of scores.

    The Kruskal-Wallis H-test tests the null hypothesis that the population median of
    all of the groups are equal. It is a non-parametric version of ANOVA. The test
    works on 2 or more independent samples, which may have different sizes. Note that
    rejecting the null hypothesis does not indicate which of the groups differs.
    Post hoc comparisons between groups are required to determine which groups are different.

    Args:
        a_name: (str): The column in the dataframe containing the ordinal or nominal variable.
        b_name: (str): The column in the dataframe containing the numeric variable.
        alpha (float): The level of statistical significance for inference.
        data (pd.DataFrame): The DataFrame containing the variables of interest.

    """

    __id = "kw"

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

        groups = [
            group[self._a_name].values for _, group in self._data.groupby(self._b_name)
        ]

        statistic, pvalue = stats.kruskal(*groups)

        dof = len(groups) - 1

        # Create the result object.
        self._result = KruskalWallisHTestResult(
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
