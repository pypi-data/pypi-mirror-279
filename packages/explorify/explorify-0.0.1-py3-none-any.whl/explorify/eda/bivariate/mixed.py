#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/bivariate/mixed.py                                                   #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Wednesday June 12th 2024 03:56:32 pm                                                #
# Modified   : Friday June 14th 2024 10:54:40 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Mixed Categorical / Numeric Bivariate Analyzer Module"""
import pandas as pd

from explorify.eda.bivariate.base import BivariateCategoricalNumericAnalyzer


# ------------------------------------------------------------------------------------------------ #
#                               EFFECT SIZE ANALYSIS                                               #
# ------------------------------------------------------------------------------------------------ #
class BivariateEffectSizeAnalyzer(BivariateCategoricalNumericAnalyzer):
    """
    Computes the effect size (Eta squared) for the relationship between the categorical and numeric variables.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data=data)

    def analyze(self, a_name: str, b_name: str) -> float:
        """
        Computes the effect size (Eta squared) for the relationship between the categorical and numeric variables.

        Args:
            a (str): The name of the categorical variable.
            b (str): The name of the numeric variable.

        Returns:
            float: The Eta squared effect size.

        Example:
            >>> analysis = BivariateCategoricalNumericAnalyzer(data)
            >>> eta_sq = analysis.effect_size('Category', 'Value')
            >>> print(eta_sq)
        """
        self.validate_input(a_name=a_name, b_name=b_name)
        group_means = self._data.groupby(a_name)[b_name].mean()
        overall_mean = self._data[b_name].mean()
        ss_between = sum(
            self._data.groupby(a_name).size() * (group_means - overall_mean) ** 2
        )
        ss_total = sum((self._data[b_name] - overall_mean) ** 2)
        eta_squared = ss_between / ss_total
        return eta_squared
