#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/bivariate/categorical.py                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Sunday June 9th 2024 10:52:53 am                                                    #
# Modified   : Saturday June 15th 2024 05:25:32 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Module for Categorical Analyzer"""
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mutual_info_score

from explorify.eda.bivariate.base import BivariateCategoricalAnalyzer


# ------------------------------------------------------------------------------------------------ #
#                              CONTINGENCY TABLE ANALYSIS                                          #
# ------------------------------------------------------------------------------------------------ #
class ContingencyTableAnalyzer(BivariateCategoricalAnalyzer):
    """
    Computes the contingency table for two categorical variables.

    Inherits from BivariateCategoricalAnalyzer.

    Attributes
    ----------
    _data : pd.DataFrame
        The input data containing the variables.

    Methods
    -------
    __init__(self, data: pd.DataFrame):
        Initializes the ContingencyTableAnalyzer instance.

    analyze(self, a_name: str, b_name: str) -> pd.DataFrame:
        Computes the contingency table for the specified categorical variables.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the ContingencyTableAnalyzer instance.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the variables.
        """
        super().__init__(data)

    def analyze(self, a_name: str, b_name: str) -> pd.DataFrame:
        """
        Computes the contingency table for two categorical variables.

        Parameters
        ----------
        a_name : str
            The name of the first categorical variable.
        b_name : str
            The name of the second categorical variable.

        Returns
        -------
        pd.DataFrame
            Contingency table of the two variables.
        """
        self.validate_input(a_name, b_name)
        return pd.crosstab(self._data[a_name], self._data[b_name])


# ------------------------------------------------------------------------------------------------ #
#                                MUTUAL INFORMATION ANALYSIS                                       #
# ------------------------------------------------------------------------------------------------ #


class MutualInformationAnalyzer(BivariateCategoricalAnalyzer):
    """
    Computes the mutual information between two categorical variables.

    Inherits from BivariateCategoricalAnalyzer.

    Attributes
    ----------
    _data : pd.DataFrame
        The input data containing the variables.

    Methods
    -------
    __init__(self, data: pd.DataFrame):
        Initializes the MutualInformationAnalyzer instance.

    analyze(self, a_name: str, b_name: str, a_type: str = "nominal", b_type: str = "nominal") -> float:
        Computes the mutual information score between the specified categorical variables.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the MutualInformationAnalyzer instance.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the variables.
        """
        super().__init__(data)

    def analyze(
        self, a_name: str, b_name: str, a_type: str = "nominal", b_type: str = "nominal"
    ) -> float:
        """
        Computes the mutual information between two categorical variables.

        Parameters
        ----------
        a_name : str
            The name of the first categorical variable.
        b_name : str
            The name of the second categorical variable.
        a_type : str, optional
            The type of the first variable ('nominal' or 'ordinal'). Defaults to 'nominal'.
        b_type : str, optional
            The type of the second variable ('nominal' or 'ordinal'). Defaults to 'nominal'.

        Returns
        -------
        float
            Mutual information score between the two variables.
        """
        self.validate_input(a_name=a_name, b_name=b_name)
        # Assign ranks to the ordinal values
        if a_type == "ordinal":
            a_data = self._data[a_name].rank(method="dense")
        else:
            a_data = self._data[a_name]
        if b_type == "ordinal":
            b_data = self._data[b_name].rank(method="dense")
        else:
            b_data = self._data[b_name]

        self.validate_input(a_name, b_name)
        return mutual_info_score(a_data, b_data)


# ------------------------------------------------------------------------------------------------ #
#                                PHI COEFFICIENT ANALYSIS                                          #
# ------------------------------------------------------------------------------------------------ #
class PhiCoefficientAnalyzer(BivariateCategoricalAnalyzer):
    """
    Computes the Phi coefficient for two nominal variables (for 2x2 tables).

    Inherits from BivariateCategoricalAnalyzer.

    Attributes
    ----------
    _data : pd.DataFrame
        The input data containing the variables.

    Methods
    -------
    __init__(self, data: pd.DataFrame):
        Initializes the PhiCoefficientAnalyzer instance.

    analyze(self, a_name: str, b_name: str) -> float:
        Computes the Phi coefficient for the specified nominal variables.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the PhiCoefficientAnalyzer instance.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the variables.
        """
        super().__init__(data)

    def analyze(self, a_name: str, b_name: str) -> float:
        """
        Computes the Phi coefficient for two nominal variables (for 2x2 tables).

        Parameters
        ----------
        a_name : str
            The name of the first nominal variable.
        b_name : str
            The name of the second nominal variable.

        Returns
        -------
        float
            Phi coefficient.

        Raises
        ------
        ValueError
            If the contingency table is not 2x2.
        """
        self.validate_input(a_name, b_name)
        contingency_table = pd.crosstab(self._data[a_name], self._data[b_name])

        if contingency_table.shape != (2, 2):
            raise ValueError(
                "Phi coefficient can only be computed for 2x2 contingency tables."
            )

        chi2, _, _, _ = stats.chi2_contingency(contingency_table)
        n = self._data.shape[0]
        return np.sqrt(chi2 / n)


# ------------------------------------------------------------------------------------------------ #
#                           CONTINGENCY COEFFICIENT ANALYSIS                                       #
# ------------------------------------------------------------------------------------------------ #
class ContingencyCoefficientAnalyzer(BivariateCategoricalAnalyzer):
    """
    Computes the contingency coefficient for two nominal variables.

    Inherits from BivariateCategoricalAnalyzer.

    Attributes
    ----------
    _data : pd.DataFrame
        The input data containing the variables.

    Methods
    -------
    __init__(self, data: pd.DataFrame):
        Initializes the ContingencyCoefficientAnalyzer instance.

    analyze(self, a_name: str, b_name: str, a_type: str = "nominal", b_type: str = "nominal") -> float:
        Computes the contingency coefficient for the specified nominal variables.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the ContingencyCoefficientAnalyzer instance.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the variables.
        """
        super().__init__(data)

    def analyze(
        self, a_name: str, b_name: str, a_type: str = "nominal", b_type: str = "nominal"
    ) -> float:
        """
        Computes the contingency coefficient for two nominal variables.

        Parameters
        ----------
        a_name : str
            The name of the first nominal variable.
        b_name : str
            The name of the second nominal variable.
        a_type : str, optional
            The type of the first variable ('nominal' or 'ordinal'). Defaults to 'nominal'.
        b_type : str, optional
            The type of the second variable ('nominal' or 'ordinal'). Defaults to 'nominal'.

        Returns
        -------
        float
            Contingency coefficient.

        Notes
        -----
        The contingency coefficient is a measure of association for nominal variables,
        computed as sqrt(chi2 / (chi2 + n)), where chi2 is the chi-squared statistic
        and n is the total number of observations.

        Raises
        ------
        ValueError
            If there is an issue with input validation or contingency table computation.
        """
        self.validate_input(a_name=a_name, b_name=b_name)
        # Sort ordinal variables
        if a_type == "ordinal":
            self._data[a_name] = self._data[a_name].sort_values()
        if b_type == "ordinal":
            self._data[b_name] = self._data[b_name].sort_values()

        self.validate_input(a_name, b_name)
        contingency_table = pd.crosstab(self._data[a_name], self._data[b_name])

        try:
            chi2, _, _, _ = stats.chi2_contingency(contingency_table)
            n = self._data.shape[0]
            return np.sqrt(chi2 / (chi2 + n))
        except ValueError as e:  # pragma: no cover
            raise ValueError("Failed to compute contingency coefficient.") from e


# ------------------------------------------------------------------------------------------------ #
#                           LAMBDA COEFFICIENT ANALYSIS                                            #
# ------------------------------------------------------------------------------------------------ #
class LambdaCoefficientAnalyzer(BivariateCategoricalAnalyzer):
    """
    Computes the lambda coefficient for two nominal variables or a mix of nominal and ordinal variables.

    Inherits from BivariateCategoricalAnalyzer.

    Attributes
    ----------
    _data : pd.DataFrame
        The input data containing the variables.

    Methods
    -------
    __init__(self, data: pd.DataFrame):
        Initializes the LambdaCoefficientAnalyzer instance.

    analyze(self, a_name: str, b_name: str, a_type: str = "nominal", b_type: str = "nominal") -> float:
        Computes the lambda coefficient for the specified variables.

    _analyze_nominal(self, a_name: str, b_name: str) -> float:
        Computes the lambda coefficient for two nominal variables.

    _analyze_mixed(self, a_name: str, b_name: str) -> float:
        Computes the lambda coefficient for a mix of nominal and ordinal variables.
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the LambdaCoefficientAnalyzer instance.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the variables.
        """
        super().__init__(data)

    def analyze(
        self, a_name: str, b_name: str, a_type: str = "nominal", b_type: str = "nominal"
    ) -> float:
        """
        Computes the lambda coefficient for two nominal variables or a mix of nominal and ordinal variables.

        Parameters
        ----------
        a_name : str
            The name of the first variable.
        b_name : str
            The name of the second variable.
        a_type : str, optional
            The type of the first variable ('nominal' or 'ordinal'). Defaults to 'nominal'.
        b_type : str, optional
            The type of the second variable ('nominal' or 'ordinal'). Defaults to 'nominal'.

        Returns
        -------
        float
            Lambda coefficient.

        Raises
        ------
        ValueError
            If there is an issue with input validation or contingency table computation.
        """
        self.validate_input(a_name=a_name, b_name=b_name)
        if a_type == "nominal" and b_type == "nominal":
            return self._analyze_nominal(a_name=a_name, b_name=b_name)
        else:
            return self._analyze_mixed(a_name=a_name, b_name=b_name)

    def _analyze_nominal(self, a_name: str, b_name: str) -> float:
        """
        Computes the lambda coefficient for two nominal variables.

        Parameters
        ----------
        a_name : str
            The name of the first nominal variable.
        b_name : str
            The name of the second nominal variable.

        Returns
        -------
        float
            Lambda coefficient.
        """
        self.validate_input(a_name, b_name)
        contingency_table = pd.crosstab(self._data[a_name], self._data[b_name])
        chi2, _, _, _ = stats.chi2_contingency(contingency_table)
        n = self._data.shape[0]
        return np.sqrt(chi2 / (n * min(contingency_table.shape)))

    def _analyze_mixed(self, a_name: str, b_name: str) -> float:
        """
        Computes the lambda coefficient for a mix of nominal and ordinal variables.

        Parameters
        ----------
        a_name : str
            The name of the nominal or ordinal variable.
        b_name : str
            The name of the nominal or ordinal variable.

        Returns
        -------
        float
            Lambda coefficient.
        """
        self.validate_input(a_name, b_name)
        contingency_table = pd.crosstab(self._data[a_name], self._data[b_name])
        n = contingency_table.sum().sum()  # Total number of observations

        # Calculate the marginal proportions
        row_marginals = contingency_table.sum(axis=1) / n
        col_marginals = contingency_table.sum(axis=0) / n

        # Calculate the observed agreement
        observed_agreement = 0
        for i in range(contingency_table.shape[0]):
            for j in range(contingency_table.shape[1]):
                observed_agreement += (
                    contingency_table.iloc[i, j]
                    * row_marginals.iloc[i]
                    * col_marginals.iloc[j]
                )

        # Calculate the expected agreement under independence assumption
        expected_agreement = 0
        for i in range(contingency_table.shape[0]):
            for j in range(contingency_table.shape[1]):
                expected_agreement += row_marginals.iloc[i] * col_marginals.iloc[j]

        return (observed_agreement - expected_agreement) / (1 - expected_agreement)


# ------------------------------------------------------------------------------------------------ #
#                            GAMMA COEFFICIENT ANALYSIS                                            #
# ------------------------------------------------------------------------------------------------ #


class GammaCoefficientAnalyzer(BivariateCategoricalAnalyzer):
    """
    Computes the Gamma coefficient for a nominal and an ordinal variable or vice versa.

    Inherits from BivariateCategoricalAnalyzer.

    Attributes
    ----------
    _data : pd.DataFrame
        The input data containing the variables.

    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the GammaCoefficientAnalyzer instance.

        Parameters
        ----------
        data : pd.DataFrame
            The input data containing the variables.
        """
        super().__init__(data)

    def analyze(
        self, a_name: str, b_name: str, a_type: str = "ordinal", b_type: str = "nominal"
    ) -> float:
        """
        Computes the Gamma coefficient for a nominal and an ordinal variable or vice versa.

        Parameters
        ----------
        a_name : str
            The name of the first variable.
        b_name : str
            The name of the second variable.
        a_type : str, optional
            The type of the first variable ('ordinal' or 'nominal'). Defaults to 'ordinal'.
        b_type : str, optional
            The type of the second variable ('nominal' or 'ordinal'). Defaults to 'nominal'.

        Returns
        -------
        float
            Gamma coefficient.

        Raises
        ------
        ValueError
            If there is an issue with input validation or contingency table computation.
        """
        self.validate_input(a_name=a_name, b_name=b_name)
        if a_type == "ordinal" and b_type == "nominal":
            return self._analyze(a_name=a_name, b_name=b_name)
        elif a_type == "nominal" and b_type == "ordinal":
            return self._analyze(b_name=b_name, a_name=a_name)
        elif a_type == "ordinal" and b_type == "ordinal":
            return self._analyze_ordinal(a_name=a_name, b_name=b_name)

    def _analyze(self, a_name: str, b_name: str) -> float:
        """
        Computes the Gamma coefficient for a nominal and an ordinal variable.

        Parameters
        ----------
        a_name : str
            The name of the ordinal variable.
        b_name : str
            The name of the nominal variable.

        Returns
        -------
        float
            Gamma coefficient.
        """
        self.validate_input(a_name, b_name)
        contingency_table = pd.crosstab(self._data[a_name], self._data[b_name])

        # Sort the ordinal variable
        a_data = self._data[a_name].sort_values()
        b_data = self._data[b_name]

        # Compute the ranks for the ordinal variable
        ranks = a_data.rank(method="dense")

        # Calculate the differences in ranks for concordant and discordant pairs
        concordant_pairs = 0
        discordant_pairs = 0
        for i in range(len(self._data)):
            for j in range(i + 1, len(self._data)):
                if a_data[i] != a_data[j]:
                    if (ranks[i] - ranks[j]) * (
                        contingency_table.loc[a_data[i], b_data[j]]
                        - contingency_table.loc[a_data[j], b_data[i]]
                    ) > 0:
                        concordant_pairs += 1
                    else:
                        discordant_pairs += 1

        return (concordant_pairs - discordant_pairs) / (
            concordant_pairs + discordant_pairs
        )

    def _analyze_ordinal(self, a_name: str, b_name: str) -> float:
        """
        Computes the Gamma coefficient for two ordinal variables.

        Parameters
        ----------
        a_name : str
            The name of the first ordinal variable.
        b_name : str
            The name of the second ordinal variable.

        Returns
        -------
        float
            Gamma coefficient.
        """
        self.validate_input(a_name, b_name)

        # Sort the ordinal variables
        a_data = self._data[a_name].sort_values()
        b_data = self._data[b_name].sort_values()

        # Compute the ranks for the ordinal variables
        ranks_a = a_data.rank(method="dense")
        ranks_b = b_data.rank(method="dense")

        # Calculate the differences in ranks for concordant and discordant pairs
        concordant_pairs = 0
        discordant_pairs = 0
        for i in range(len(self._data)):
            for j in range(i + 1, len(self._data)):
                if a_data[i] != a_data[j] and b_data[i] != b_data[j]:
                    if (ranks_a[i] - ranks_a[j]) * (ranks_b[i] - ranks_b[j]) > 0:
                        concordant_pairs += 1
                    else:
                        discordant_pairs += 1

        return (concordant_pairs - discordant_pairs) / (
            concordant_pairs + discordant_pairs
        )


# ------------------------------------------------------------------------------------------------ #
#                            THEIL'S U COEFFICIENT ANALYSIS                                        #
# ------------------------------------------------------------------------------------------------ #


class ThielsUCoefficientAnalyzer(BivariateCategoricalAnalyzer):
    """
    Computes Theil's U coefficient for a nominal and an ordinal variable.

    Inherits from BivariateCategoricalAnalyzer.

    Args:
        _data (pd.DataFrame): The input data containing the variables.

    Attributes:
        _data (pd.DataFrame): The input data containing the variables.

    """

    def __init__(self, data: pd.DataFrame):
        """
        Initializes the ThielsUCoefficientAnalyzer instance.

        Args:
            data (pd.DataFrame): The input data containing the variables.
        """
        super().__init__(data=data)

    def analyze(self, a_name: str, b_name: str) -> float:
        """
        Computes Theil's U coefficient for a nominal and an ordinal variable.

        Args:
            a_name (str): The name of the nominal variable.
            b_name (str): The name of the ordinal variable. Note, ordinal
                variables must be in lexicographical order. For instance
                "0_low_income", "1_moderate_income", etc...

        Returns:
            float: Theil's U coefficient.
        """
        self.validate_input(a_name, b_name)

        # Calculate the marginal probabilities
        p_x = self._data[a_name].value_counts(normalize=True)
        p_y_given_x = self._data.groupby(a_name)[b_name].value_counts(normalize=True)

        # Compute Theil's U coefficient
        u = 0
        for x in p_x.index:
            for y in p_y_given_x[x].index:
                p_xy = p_y_given_x[x][y]
                u += p_xy * np.log(p_xy / p_x[x])

        return u
