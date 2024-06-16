#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/stats/inferential/association.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday September 29th 2023 11:52:02 pm                                              #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from dependency_injector.wiring import Provide, inject
from scipy import stats

from explorify.container import VisualizeContainer
from explorify.eda.stats.inferential.base import StatAnalyzer, StatTestResult
from explorify.eda.visualize.visualizer import Visualizer


# ================================================================================================ #
#                                       KENDALL'S TAU                                              #
# ================================================================================================ #
# ------------------------------------------------------------------------------------------------ #
#                                 KENDALL'S TAU MEASURE OF CORRELATION                             #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class KendallsTauTestResult(StatTestResult):
    name: str = f"Kendall's \u03c4"  # noqa
    data: pd.DataFrame = None
    a_name: str = None
    b_name: str = None
    n: int = None
    strength: str = None
    pvalue: float = None
    visualizer: Visualizer = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    def plot(self) -> None:  # pragma: no cover
        self.visualizer.kendallstau(
            data=self._data,
            a_name=self.a_name,
            b_name=self.b_name,
            value=self.value,
            thresholds=self.thresholds,
            interpretation=self.interpretation,
        )

    @property
    def report(self) -> str:
        significance = (
            "yet, non significant" if self.value > self.alpha else "and significant"
        )
        result = f"A Kendall's Tau Test was conducted to measure the strength of correlation between {self.a_name.capitalize()} and {self.b_name.capitalize()}."
        result += rf"The $t_b$ was {self._report_statistic(self.value)}, {self._report_pvalue(self.pvalue)} suggesting a {self.strength} {significance} correlation between {self.a_name.capitalize()} and {self.b_name.capitalize()}."
        return result


# ------------------------------------------------------------------------------------------------ #
#                                   CRAMERS V ANALYSIS                                             #
# ------------------------------------------------------------------------------------------------ #
class KendallsTauTest(StatAnalyzer):
    """Calculate Kendall's tau, a correlation measure for ordinal data.

    Kendall's tau is a measure of the correspondence between two rankings. Values close to 1 indicate
    strong agreement, and values close to -1 indicate strong disagreement. This implements two
    variants of Kendall's tau: tau-b (the default) and tau-c (also known as Stuart's tau-c).
    These differ only in how they are normalized to lie within the range -1 to 1; the hypothesis
    tests (their p-values) are identical. Kendall's original tau-a is not implemented separately
    because both tau-b and tau-c reduce to tau-a in the absence of ties.

    Args:
        data (pd.DataFrame): The DataFrame containing the variables of interest.
        a (str): The name of an ordinal variable in data.
        b (str): The name of an ordinal variable in data.

    """

    __id = "kendallstau"

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        a_name: str = None,
        b_name: str = None,
        variant: str = "c",
        alternative: str = "two-sided",
        ordinal_a: bool = False,
        ordinal_b: bool = False,
    ) -> None:
        super().__init__()
        self._data = data
        self._a_name = a_name
        self._b_name = b_name
        self._variant = variant
        self._alternative = alternative
        self._ordinal_a = ordinal_a
        self._ordinal_b = ordinal_b
        self._thresholds = np.array([-1, -0.5, -0.3, 0.0, 0.3, 0.5, 1.0])
        self._labels = [
            "Strong",
            "Moderate",
            "Weak",
            "Weak",
            "Moderate",
            "Strong",
        ]

    @property
    def result(self) -> KendallsTauTestResult:
        """Returns the Cramer's V Measure object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""
        data = self._data.copy()

        if self._ordinal_a:
            data[self._a_name] = data[self._a_name].sort_values()
        if self._ordinal_b:
            data[self._b_name] = data[self._b_name].sort_values()

        a = data[self._a_name].values
        b = data[self._b_name].values

        statistic, pvalue = stats.kendalltau(
            x=a, y=b, variant=self._variant, alternative=self._alternative
        )

        strength = self._labels[np.argmax(np.where(self._thresholds < statistic))]

        # Create the result object.
        self._result = KendallsTauTestResult(
            data=data,
            a_name=self._a_name,
            b_name=self._b_name,
            n=len(a),
            value=statistic,
            strength=strength,
            pvalue=pvalue,
        )


# ================================================================================================ #
#                                         CRAMER'S V                                               #
# ================================================================================================ #


# ------------------------------------------------------------------------------------------------ #
#                                 CRAMERS V MEASURE OF ASSOCIATION                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class CramersV(StatTestResult):
    name: str = "Cramer's V"
    strength: str = None
    data: pd.DataFrame = None
    a_name: str = None
    b_name: str = None
    n: int = None
    dof: int = None
    x2alpha: float = None
    x2: float = None
    x2dof: float = None
    pvalue: float = None
    expected_freq: np.array = None
    x2result: str = None
    visualizer: Visualizer = None

    @inject
    def __post_init__(
        self, visualizer: Visualizer = Provide[VisualizeContainer.visualizer]
    ) -> None:
        self.visualizer = visualizer

    @property
    def report(self) -> str:
        direction = "above" if self.x2 > self.alpha else "below"
        x2significance = "non significant" if self.x2 > self.alpha else "significant"
        cvsignificance = "non significant" if self.value > self.alpha else "significant"
        result = f"A X\u00b2 Test of Independence was conducted to measure the strength of association between {self.a_name.capitalize()} and {self.b_name.capitalize()}."
        result += f"The X\u00b2 was {self._report_statistic(self.x2)}, {direction} the alpha level of {self.alpha}, suggesting a {x2significance} association between {self.a_name.capitalize()} and {self.b_name.capitalize()}."
        result += f"Additionally, an effect size was calculated using Cramer's V, which was found to be {self._report_statistic(self.value)}."
        result += f"A {cvsignificance} result of {self.strength} in magnitude."
        return result


# ------------------------------------------------------------------------------------------------ #
#                                   CRAMERS V ANALYSIS                                             #
# ------------------------------------------------------------------------------------------------ #
class CramersVAnalyzer(StatAnalyzer):
    """Cramer's V Analyzer of the Association between two Nominal Variables.

    The CramersVAnalyzer class provides the association between two nominal variables.

    Args:
        data (pd.DataFrame): The DataFrame containing the variables of interest.
        a_name (str): Name of the nominal
        x (str): The name of the independent variable in data.
        y (str): The name of the dependent variable in data.
        alpha (float): The level of significance for the independence hypothesis test. Default = 0.05
    """

    __id = "cramersv"

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        a_name: str = None,
        b_name: str = None,
        alpha: float = 0.05,
        correction: bool = True,
        ordinal_a: bool = False,
        ordinal_b: bool = False,
    ) -> None:
        super().__init__()
        self._data = data
        self._a_name = a_name
        self._b_name = b_name
        self._alpha = alpha
        self._correction = correction
        self._ordinal_a = ordinal_a
        self._ordinal_b = ordinal_b
        self._thresholds = {
            1: [0.0, 0.1, 0.3, 0.5, 1.0],
            2: [0.0, 0.07, 0.21, 0.35, 1.0],
            3: [0.0, 0.06, 0.17, 0.29, 1.0],
            4: [0.0, 0.05, 0.15, 0.25, 1.0],
            5: [0.0, 0.04, 0.13, 0.22, 1.0],
            6: [0.0, 0.04, 0.13, 0.22, 1.0],
            7: [0.0, 0.04, 0.13, 0.22, 1.0],
            8: [0.0, 0.04, 0.13, 0.22, 1.0],
            9: [0.0, 0.04, 0.13, 0.22, 1.0],
            10: [0.0, 0.04, 0.13, 0.22, 1.0],
        }
        self._labels = ["Negligible", "Small", "Moderate", "Large"]

    @property
    def result(self) -> CramersV:
        """Returns the Cramer's V Result object."""
        return self._result

    def run(self) -> None:
        """Performs the statistical test and creates a result object."""

        data = self._data.copy()

        if self._ordinal_a:
            data[self._a_name] = data[self._a_name].sort_values()
        if self._ordinal_b:
            data[self._b_name] = data[self._b_name].sort_values()

        crosstab = pd.crosstab(data[self._a_name], data[self._b_name])

        statistic, pvalue, x2dof, exp = stats.chi2_contingency(crosstab.values)

        dof = min(crosstab.shape[0], crosstab.shape[1]) - 1

        cv = stats.contingency.association(
            crosstab.values, method="cramer", correction=self._correction
        )

        revised_dof = np.min(np.array([dof, 10]))

        thresholds = np.array(self._thresholds[revised_dof])

        strength = self._labels[np.argmax(np.where(thresholds < cv))]

        # Create the result object.
        self._result = CramersV(
            data=crosstab,
            a_name=self._a_name,
            b_name=self._b_name,
            dof=dof,
            value=cv,
            strength=strength,
            n=len(data),
            x2alpha=self._alpha,
            x2=statistic,
            x2dof=x2dof,
            pvalue=pvalue,
            expected_freq=exp,
        )
