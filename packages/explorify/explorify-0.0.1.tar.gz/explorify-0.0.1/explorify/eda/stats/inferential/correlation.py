#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /explorify/eda/stats/inferential/correlation.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.a_namei.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 7th 2023 08:15:08 pm                                                 #
# Modified   : Friday June 14th 2024 07:51:25 pm                                                   #
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

# ================================================================================================ #
#                                  PEARSON'S CORRELATION                                           #
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class PearsonCorrelationTestResult(StatTestResult):
    name: str = "Pearson Correlation Coefficient"
    data: pd.DataFrame = None
    a_name: str = None
    b_name: str = None
    dof: float = None
    strength: str = None
    low_ci: float = None
    high_ci: float = None
    interpret: str = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.regplot(
            data=self._data, x=self.a_name, y=self.b_name, title=self.result
        )

    @property
    def report(self) -> str:
        report = f"Pearson's correlation was computed to assess the relationship between {self.a_name} and {self.b_name}. "
        if self.pvalue > self.alpha:  # pragma: no cover
            return (
                report
                + f"There was a {self.interpret} between the two variables, r({self.dof})={self._report_statistic(self.value)},  {self._report_pvalue(self.pvalue)}."
            )
        else:  # pragma: no cover
            return (
                report
                + f"There was a non-signficant {self.interpret} between the two variables, r({self.dof})={self._report_statistic(self.value)},  {self._report_pvalue(self.pvalue)}."
            )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class PearsonCorrelationTest(StatisticalTest):
    """Pearson correlation coefficient and p-value for testing non-correlation.

    The Pearson correlation coefficient [1] measures the linear relationship between two
    datasets. Like other correlation coefficients, this one varies between -1 and +1 with 0
    implying no correlation. Correlations of -1 or +1 imply an exact linear relationship.
    Positive correlations imply that as x increases, so does y. Negative correlations imply
    that as x increases, y decreases.

    This function also performs a test of the null hypothesis that the distributions underlying
    the samples are uncorrelated and normally distributed. (See Kowalski [3] for a discussion of
    the effects of non-normality of the input on the distribution of the correlation coefficient.)
    The p-value roughly indicates the probability of an uncorrelated system producing datasets
    that have a Pearson correlation at least as extreme as the one computed from these datasets.

    Args:
        a_name (str): Name of first numeric variable
        b_name (str): Name of second numeric variable
        data (pd.DataFrame): DataFrame containing both variables.
        alpha (float): The test significance level. Default=0.05
        **kwargs
    """

    __id = "pearson"

    def __init__(
        self,
        a_name: str,
        b_name: str,
        data: pd.DataFrame,
        alpha: float = 0.05,
        **kwargs,
    ) -> None:
        super().__init__()
        self._a_name = a_name
        self._b_name = b_name
        self._data = data
        self._alpha = alpha
        self._kwargs = kwargs
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

        try:
            pearson_result = stats.pearsonr(
                x=self._data[self._a_name].values,
                y=self._data[self._b_name].values,
                **self._kwargs,
            )
        except Exception as e:  # pragma: no cover
            msg = f"Unable to calculate pearson correlation.\n{e}"
            self._logger.exception(msg)
            raise

        r = pearson_result.statistic
        pvalue = pearson_result.pvalue
        confidence_interval = pearson_result.confidence_interval(self._alpha)
        self._logger.debug(pearson_result)
        self._logger.debug(confidence_interval)

        dof = len(self._data) - 2

        # Create the result object.
        self._result = PearsonCorrelationTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            strength=self._interpret_r(r=r).capitalize(),
            low_ci=confidence_interval.low,
            high_ci=confidence_interval.high,
            value=r,
            dof=dof,
            pvalue=pvalue,
            data=self._data,
            a_name=self._a_name,
            b_name=self._b_name,
            alpha=self._alpha,
            interpret=self._interpret_r(r),
        )

    def _interpret_r(self, r: float) -> str:  # pragma: no cover
        """Interprets the value of the correlation[1]_

        .. [1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research. Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.


        """

        if r < 0:
            direction = "negative"
        else:
            direction = "positive"

        r = abs(r)
        if r >= 0.9:
            return f"very high {direction} correlation."
        elif r >= 0.70:
            return f"high {direction} correlation."
        elif r >= 0.5:
            return f"moderate {direction} correlation."
        elif r >= 0.3:
            return f"low {direction} correlation."
        else:
            return "negligible correlation."


# ================================================================================================ #
#                                SPEARMAN'S CORRELATION                                            #
# ================================================================================================ #
# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class SpearmanCorrelationResult(StatTestResult):
    name: str = "Spearman Rank Correlation Coefficient"
    strength: str = None
    data: pd.DataFrame = None
    a_name: str = None
    b_name: str = None
    dof: float = None
    n: int = None
    interpret: str = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.regplot(
            data=self._data, x=self.a_name, y=self.b_name, title=self.result
        )

    @property
    def report(self) -> str:
        report = f"Spearman's rank correlation was computed to assess the relationship between {self.a_name} and {self.b_name}. "
        if self.pvalue > self.alpha:  # pragma: no cover
            return (
                report
                + f"There was a {self.interpret} between the two variables, r({self.dof})={self._report_statistic(self.value)},  {self._report_pvalue(self.pvalue)}."
            )
        else:  # pragma: no cover
            return (
                report
                + f"There was a non-signficant {self.interpret} between the two variables, r({self.dof})={self._report_statistic(self.value)},  {self._report_pvalue(self.pvalue)}."
            )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class SpearmanCorrelationTest(StatisticalTest):
    __id = "spearman"

    def __init__(
        self, data: pd.DataFrame, a_name=str, b_name=str, alpha: float = 0.05
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

        r, pvalue = stats.spearmanr(
            a=self._data[self._a_name].values,
            b=self._data[self._b_name].values,
            alternative="two-sided",
            nan_policy="omit",
        )

        dof = len(self._data) - 2

        # Create the result object.
        self._result = SpearmanCorrelationResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            strength=self._interpret_r(r).capitalize(),
            value=r,
            pvalue=pvalue,
            dof=dof,
            data=self._data,
            a_name=self._a_name,
            b_name=self._b_name,
            alpha=self._alpha,
            n=len(self._data),
            interpret=(self._interpret_r(r)),
        )

    def _interpret_r(self, r: float) -> str:  # pragma: no cover
        """Interprets the value of the correlation[1]_

        .. [1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research. Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.


        """

        if r < 0:
            direction = "negative"
        else:
            direction = "positive"

        r = abs(r)
        if r >= 0.9:
            return f"very high {direction} correlation"
        elif r >= 0.70:
            return f"high {direction} correlation"
        elif r >= 0.5:
            return f"moderate {direction} correlation"
        elif r >= 0.3:
            return f"low {direction} correlation"
        else:
            return "negligible correlation"


# ================================================================================================ #
#                                  PEARSON'S CORRELATION                                           #
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#                                     TEST RESULT                                                  #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class PointBiserialCorrelationTestResult(StatTestResult):
    name: str = "Pearson Correlation Coefficient"
    data: pd.DataFrame = None
    a_name: str = None
    b_name: str = None
    dof: float = None
    strength: str = None
    interpret: str = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:  # pragma: no cover
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.regplot(
            data=self._data, x=self.a_name, y=self.b_name, title=self.result
        )

    @property
    def report(self) -> str:  # pragma: no cover
        report = f"Point Biserial Correlation was computed to assess the relationship between {self.a_name} and {self.b_name}. "
        if self.pvalue > self.alpha:  # pragma: no cover
            return (
                report
                + f"There was a {self.interpret} between the two variables, r({self.dof})={self._report_statistic(self.value)},  {self._report_pvalue(self.pvalue)}."
            )
        else:  # pragma: no cover
            return (
                report
                + f"There was a non-signficant {self.interpret} between the two variables, r({self.dof})={self._report_statistic(self.value)},  {self._report_pvalue(self.pvalue)}."
            )


# ------------------------------------------------------------------------------------------------ #
#                                          TEST                                                    #
# ------------------------------------------------------------------------------------------------ #
class PointBiserialCorrelationTest(StatisticalTest):
    """Calculate a point biserial correlation coefficient and its p-value.

    The point biserial correlation is used to measure the relationship between a binary
    variable, x, and a continuous variable, y. Like other correlation coefficients,
    this one varies between -1 and +1 with 0 implying no correlation. Correlations of
    -1 or +1 imply a determinative relationship.

    This function may be computed using a shortcut formula but produces the
     same result as pearsonr.

    Args:
        a_name (str): Name of binary variable
        b_name (str): Name of continuous variable
        data (pd.DataFrame): DataFrame containing both variables.
        alpha (float): The test significance level. Default=0.05
        **kwargs
    """

    __id = "pbc"

    def __init__(
        self,
        a_name: str,
        b_name: str,
        data: pd.DataFrame,
        alpha: float = 0.05,
        **kwargs,
    ) -> None:
        super().__init__()
        self._a_name = a_name
        self._b_name = b_name
        self._data = data
        self._alpha = alpha
        self._kwargs = kwargs
        self._profile = StatTestProfile.create(self.__id)
        self._result = None

    @property
    def profile(self) -> StatTestProfile:  # pragma: no cover
        """Returns the statistical test profile."""
        return self._profile

    @property
    def result(self) -> StatTestResult:
        """Returns a Statistical Test Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        try:
            result = stats.pointbiserialr(
                x=self._data[self._a_name].values,
                y=self._data[self._b_name].values,
                **self._kwargs,
            )
        except Exception as e:  # pragma: no cover
            msg = f"Unable to calculate pearson correlation.\n{e}"
            self._logger.exception(msg)
            raise

        r = result.statistic
        pvalue = result.pvalue
        dof = len(self._data) - 1

        # Create the result object.
        self._result = PearsonCorrelationTestResult(
            H0=self._profile.H0,
            statistic=self._profile.statistic,
            hypothesis=self._profile.hypothesis,
            strength=self._interpret_r(r=r).capitalize(),
            value=r,
            dof=dof,
            pvalue=pvalue,
            data=self._data,
            a_name=self._a_name,
            b_name=self._b_name,
            alpha=self._alpha,
            interpret=self._interpret_r(r),
        )

    def _interpret_r(self, r: float) -> str:  # pragma: no cover
        """Interprets the value of the correlation[1]_

        .. [1] Mukaka MM. Statistics corner: A guide to appropriate use of correlation coefficient in medical research. Malawi Med J. 2012 Sep;24(3):69-71. PMID: 23638278; PMCID: PMC3576830.


        """

        if r < 0:
            direction = "negative"
        else:
            direction = "positive"

        r = abs(r)
        if r >= 0.9:
            return f"very high {direction} correlation."
        elif r >= 0.70:
            return f"high {direction} correlation."
        elif r >= 0.5:
            return f"moderate {direction} correlation."
        elif r >= 0.3:
            return f"low {direction} correlation."
        else:
            return "negligible correlation."
