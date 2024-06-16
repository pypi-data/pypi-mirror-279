#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /explorify/eda/stats/inferential/centrality.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 11:41:00 pm                                                 #
# Modified   : Thursday June 13th 2024 11:10:23 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from dataclasses import dataclass

import numpy as np
import pandas as pd
from dependency_injector.wiring import Provide, inject
from scipy import stats

from explorify.container import VisualizeContainer
from explorify.eda.stats.descriptive.continuous import ContinuousStats
from explorify.eda.stats.inferential.base import StatisticalTest, StatTestResult
from explorify.eda.stats.inferential.profile import StatTestProfile
from explorify.eda.visualize.visualizer import Visualizer


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class TTestResult(StatTestResult):
    name: str = "Student's t-test"
    dof: int = None
    homoscedastic: bool = None
    a_data: np.ndarray = None
    a_name: str = None
    b_data: np.ndarray = None
    b_name: str = None
    varname: str = None
    a_stats: ContinuousStats = None
    b_stats: ContinuousStats = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        title = self.result()
        self.visualizer.ttestplot(
            statistic=self.value, dof=self.dof, alpha=self.alpha, title=title
        )

    @property
    def report(self) -> str:
        result = f"A Student's T-Test was conducted to test the mean {self.varname} between {self.a_name} and {self.b_name}"
        significance = "non significant" if self.pvalue > self.alpha else "significant"
        lower_var = (
            self.a_name if self.a_stats.mean < self.b_stats.mean else self.b_name
        )
        lower_mean = (
            self.a_stats.mean
            if self.a_stats.mean < self.b_stats.mean
            else self.b_stats.mean
        )
        lower_std = (
            np.std(self.a_data)
            if self.a_stats.mean < self.b_stats.mean
            else np.std(self.b_data)
        )
        higher_var = (
            self.a_name if self.a_stats.mean > self.b_stats.mean else self.b_name
        )
        higher_mean = (
            self.a_stats.mean
            if self.a_stats.mean > self.b_stats.mean
            else self.b_stats.mean
        )
        higher_std = (
            np.std(self.a_data)
            if self.a_stats.mean > self.b_stats.mean
            else np.std(self.b_data)
        )

        return (
            result
            + f"A {significance} difference in mean {self.varname} was detected for {higher_var} (M={higher_mean}, SD={higher_std}) and {lower_var} (M={lower_mean}, SD={lower_std})"
        )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class TTest(StatisticalTest):
    """Calculate the T-test for the means of two independent samples of scores.

    This is a test for the null hypothesis that 2 independent samples have identical average
    (expected) values. This test assumes that the populations have identical variances by default.

    Args:
        a_name (str): Name of the first independent sample
        a_data (np.ndarray): An array containing the first of two independent samples.
        b_name (str): Name of the second independent sample
        b_data (np.ndarray): An array containing the second of two independent samples.
        varname (str): The name of the variable being evaluated.
        alpha (float): The level of statistical significance for inference.
        homoscedastic (bool): If True, perform a standard independent 2 sample test t
            hat assumes equal population variances. If False, perform Welch's
            t-test, which does not assume equal population variance.

    """

    __id = "t2"

    def __init__(
        self,
        a_name: str,
        a_data: np.ndarray,
        b_name: str,
        b_data: np.ndarray,
        varname: str,
        alpha: float = 0.05,
        homoscedastic: bool = True,
    ) -> None:
        super().__init__()
        self._a_name = a_name
        self._a_data = a_data
        self._b_name = b_name
        self._b_data = b_data
        self._varname = varname
        self._alpha = alpha
        self._homoscedastic = homoscedastic
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
        """Executes the TTest."""

        statistic, pvalue = stats.ttest_ind(
            a=self._a_data, b=self._b_data, equal_var=self._homoscedastic
        )

        a_stats = ContinuousStats.describe(x=self._a_data)
        b_stats = ContinuousStats.describe(x=self._b_data)

        dof = len(self._a_data) + len(self._b_data) - 2

        # Create the result object.
        self._result = TTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            homoscedastic=self._homoscedastic,
            varname=self._varname,
            dof=dof,
            value=np.abs(statistic),
            alpha=self._alpha,
            pvalue=pvalue,
            a_name=self._a_name,
            a_data=self._a_data,
            b_name=self._b_name,
            b_data=self._b_data,
            a_stats=a_stats,
            b_stats=b_stats,
        )


# ------------------------------------------------------------------------------------------------ #
#                                     ANOVA RESULT                                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class AnovaOneWayTestResult(StatTestResult):
    name: str = "One-Way Anova"
    a_name: str = None
    b_name: str = None
    data: pd.DataFrame = None
    alpha: float = 0.05
    statistic: str = "F statistic"
    dof_between: float = 0.0
    dof_within: float = 0.0
    value: float = 0.0
    pvalue: float = 0.0

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        title = r"One-Way Anova Test of average {b_name} in {a_name}".format(
            b_name=self.b_name,
            a_name=self.a_name,
        )
        self.visualizer.boxplot(
            x=self.a_name, y=self.b_name, data=self.data, title=title
        )

    @property
    def report(self) -> str:
        if self.pvalue > self.alpha:
            return r"The {name} Test found a non-significant difference in average {b_name} within {a_name}, F({dof_between},{dof_within})={statistic}, p>0.05.".format(
                name=self.name,
                b_name=self.b_name,
                a_name=self.a_name,
                dof_between=self.dof_between,
                dof_within=self.dof_within,
                statistic=round(self.value, 2),
            )  # pragma: no cover
        else:
            return r"The {name} Test found a significant difference in average {b_name} within {a_name}, F({dof_between},{dof_within})={statistic}, p<0.05.".format(
                name=self.name,
                b_name=self.b_name,
                a_name=self.a_name,
                dof_between=self.dof_between,
                dof_within=self.dof_within,
                statistic=round(self.value, 2),
            )  # pragma: no cover


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class AnovaOneWayTest(StatisticalTest):
    """Calculate the Anova One-Way test for means of three or more categories.

    This is a test for the null hypothesis that there is no difference in means between
     groups.

    Args:
        a: (str): Name of column containing the categorical variable.
        b: (str): Name of column containing the numeric variable.
        alpha (float): The level of statistical significance for inference.

    """

    __id = "anova1"

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
        """Executes the TTest."""

        groups = [
            group[self._b_name].values for _, group in self._data.groupby(self._a_name)
        ]

        statistic, pvalue = stats.f_oneway(*groups)

        dof_between = len(groups) - 1
        dof_within = len(self._data) - len(groups)

        # Create the result object.
        self._result = AnovaOneWayTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            a_name=self._a_name,
            b_name=self._b_name,
            data=self._data,
            dof_between=dof_between,
            dof_within=dof_within,
            value=statistic,
            alpha=self._alpha,
            pvalue=pvalue,
        )


# ------------------------------------------------------------------------------------------------ #
#                                MANN WHITNEY U TEST RESULT                                        #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class MannWhitneyUTestResult(StatTestResult):
    name: str = "Mann-Whitney U Test"
    a_name: str = None
    a_mdn: float = None
    a_data: np.ndarray = (None,)
    b_name: str = None
    b_mdn: float = None
    b_data: np.ndarray = (None,)
    varname: str = None
    alternative: str = None
    alpha: float = 0.05
    statistic: str = "U statistic"
    value: float = 0.0
    pvalue: float = 0.0

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        title = f"Mann-Whitney U Test {self.alternative} of {self.varname} between {self.a_name} and {self.b_name}"
        self.visualizer.boxplot(x=self.a, y=self.b, data=self.data, title=title)

    @property
    def report(self) -> str:
        if self.pvalue < self.alpha:  # pragma: no cover
            if self.a_mdn > self.b_mdn:  # pragma: no cover
                return f"The {self.name} {self.alternative} found that {self.a_name} (Mdn={self.a_mdn}) had a higher median {self.varname} than {self.b_name} (Mdn={self.b_mdn}) (U={round(self.value,2)}, p={round(self.pvalue,3)}) a value less than the alpha significance of {self._report_alpha()}."
            else:  # pragma: no cover
                return f"The {self.name} {self.alternative} found that {self.b_name} (Mdn={self.b_mdn}) had a higher median {self.varname} than {self.a_name} (Mdn={self.a_mdn}) (U={round(self.value,2)}, p={round(self.pvalue,3)}) a value less than the alpha significance of {self._report_alpha()}."
        else:  # pragma: no cover
            return f"The {self.name} {self.alternative} found no signficant difference in {self.varname} between {self.a_name} (Mdn={self.a_mdn}) and {self.b_name} (Mdn={self.b_mdn}) (U={round(self.value,2)}, p={round(self.pvalue,3)}) a value greater than the alpha significance of {self._report_alpha()}."


# ------------------------------------------------------------------------------------------------ #
#                                    MANN WHITNEY U TEST                                           #
# ------------------------------------------------------------------------------------------------ #
class MannWhitneyUTest(StatisticalTest):
    """Calculate the Mann-Whitney U Test between two independent samples.

    The Mann-Whitney U test is a nonparametric test of the null hypothesis that the
    distribution underlying sample x is the same as the distribution
    underlying sample y. It is often used as a test of difference in location
    between distributions.

    Args:
        a_name (str): Name of one of the two independent groups.
        a (np.ndarray): Data for the a
        b_name (str): Name of the other of the two independent groups.
        b (np.ndarray): Data for the b
        varname (str): Name of the variable being tested.
        alpha (float): The level of statistical significance for inference.
        alternative (str):  Defines the alternative hypothesis. Default is 'two-sided'.
            In the following, let d represent the difference between the paired samples: d = x - y
            if both x and y are provided, or d = x otherwise.

            'two-sided': the distribution underlying d is not symmetric about zero.
            'less': the distribution underlying d is stochastically less than a distribution symmetric about zero.
            'greater': the distribution underlying d is stochastically greater than a distribution symmetric about zero.

    """

    __id = "mwu"

    def __init__(
        self,
        a_name: str,
        a_data: np.ndarray,
        b_name: str,
        b_data: np.ndarray,
        varname: str,
        alternative: str = "two-sided",
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._a_name = a_name
        self._a_data = a_data
        self._b_name = b_name
        self._b_data = b_data
        self._varname = varname
        self._alternative = alternative
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
        """Executes the TTest."""

        statistic, pvalue = stats.mannwhitneyu(
            x=self._a_data,
            y=self._b_data,
            alternative=self._alternative,
            method="auto",
        )

        # Create the result object.
        self._result = MannWhitneyUTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            a_name=self._a_name,
            a_mdn=np.median(self._a_data),
            a_data=self._a_data,
            b_name=self._b_name,
            b_mdn=np.median(self._b_data),
            b_data=self._b_data,
            varname=self._varname,
            alternative=self._alternative,
            value=statistic,
            alpha=self._alpha,
            pvalue=pvalue,
        )


# ------------------------------------------------------------------------------------------------ #
#                              WILCOXON SIGNED RANK TEST RESULT                                    #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class WilcoxonSignedRankTestResult(StatTestResult):
    name: str = "Wilcoxon Signed-Rank Test"
    a_name: str = None
    a_mdn: float = None
    a_data: np.ndarray = (None,)
    b_name: str = None
    b_mdn: float = None
    b_data: np.ndarray = (None,)
    varname: str = None
    alternative: str = None
    correction: bool = False
    alpha: float = 0.05
    statistic: str = "Wilcoxon Signed-Rank Test Statistic"
    value: float = 0.0
    zstat: float = None
    pvalue: float = 0.0

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        title = f"{self.name} {self.alternative} of {self.varname} between {self.a_name} and {self.b_name}"
        self.visualizer.boxplot(x=self.a, y=self.b, data=self.data, title=title)

    @property
    def report(self) -> str:
        if self.pvalue < self.alpha:  # pragma: no cover
            if self.a_mdn > self.b_mdn:  # pragma: no cover
                return f"The {self.name} {self.alternative} found that {self.a_name} (Mdn={self.a_mdn}) had a higher median {self.varname} than {self.b_name} (Mdn={self.b_mdn}) (U={round(self.value,2)}, p={round(self.pvalue,3)}) a value less than the alpha significance of {self._report_alpha()}."
            else:  # pragma: no cover
                return f"The {self.name} {self.alternative} found that {self.b_name} (Mdn={self.b_mdn}) had a higher median {self.varname} than {self.a_name} (Mdn={self.a_mdn}) (U={round(self.value,2)}, p={round(self.pvalue,3)}) a value less than the alpha significance of {self._report_alpha()}."
        else:  # pragma: no cover
            return f"The {self.name} {self.alternative} found no signficant difference in {self.varname} between {self.a_name} (Mdn={self.a_mdn}) and {self.b_name} (Mdn={self.b_mdn}) (U={round(self.value,2)}, p={round(self.pvalue,3)}) a value greater than the alpha significance of {self._report_alpha()}."


# ------------------------------------------------------------------------------------------------ #
#                                    MANN WHITNEY U TEST                                           #
# ------------------------------------------------------------------------------------------------ #
class WilcoxonSignedRankTest(StatisticalTest):
    """Calculate the Wilcoxon signed-rank test.

    The Wilcoxon signed-rank test tests the null hypothesis that two related paired samples come
    from the same distribution. In particular, it tests whether the distribution of the differences
    x - y is symmetric about zero. It is a non-parametric version of the paired T-test.

    Args:
        a_name (str): Name of the column containing the first sample
        b_name (str): Name of the column containing the second sample
        data (pd.DataFrame): DataFrame containing both samples
        correction (bool): If True, apply continuity correction by adjusting the Wilcoxon rank
            statistic by 0.5 towards the mean value when computing the z-statistic if a normal
            approximation is used. Default is False.
        alternative (str):  Defines the alternative hypothesis. Default is 'two-sided'.
            In the following, let d represent the difference between the paired samples: d = x - y
            if both x and y are provided, or d = x otherwise.

            'two-sided': the distribution underlying d is not symmetric about zero.
            'less': the distribution underlying d is stochastically less than a distribution symmetric about zero.
            'greater': the distribution underlying d is stochastically greater than a distribution symmetric about zero.

        alpha (float): The level of statistical significance for inference. Default = 0.05

    """

    __id = "wilcoxon"

    def __init__(
        self,
        a_data: np.ndarray,
        a_name: str,
        b_data: np.ndarray,
        b_name: str,
        varname: str,
        correction: bool = True,
        alternative: str = "two-sided",
        alpha: float = 0.05,
    ) -> None:
        super().__init__()
        self._a_data = a_data
        self._a_name = a_name
        self._b_data = b_data
        self._b_name = b_name
        self._varname = varname
        self._correction = correction
        self._alternative = alternative
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
        """Executes the TTest."""
        zstatistic = None

        if self._correction:
            statistic, pvalue = stats.wilcoxon(
                x=self._a_data,
                y=self._b_data,
                alternative=self._alternative,
                method="approx",
                correction=self._correction,
            )
        else:
            statistic, pvalue = stats.wilcoxon(
                x=self._a_data,
                y=self._b_data,
                alternative=self._alternative,
                method="auto",
                correction=self._correction,
            )

        # Create the result object.
        self._result = WilcoxonSignedRankTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            a_name=self._a_name,
            a_mdn=np.median(self._a_data),
            a_data=self._a_data,
            b_name=self._b_name,
            b_mdn=np.median(self._b_data),
            b_data=self._b_data,
            alternative=self._alternative,
            correction=self._correction,
            value=statistic,
            zstat=zstatistic,
            alpha=self._alpha,
            pvalue=pvalue,
        )
