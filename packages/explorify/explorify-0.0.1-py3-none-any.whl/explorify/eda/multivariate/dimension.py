#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/multivariate/dimension.py                                            #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 08:35:16 pm                                                 #
# Modified   : Saturday June 15th 2024 03:53:32 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from explorify.eda.multivariate.base import MultivariateAnalyzer


# ------------------------------------------------------------------------------------------------ #
class PCAAnalyzer(MultivariateAnalyzer):
    """
    A class to perform Principal Component Analyzer (PCA) for dimensionality reduction.

    Methods:
        analyze(n_components: int = 2, **kwargs) -> pd.DataFrame:
            Performs PCA.
    """

    def analyze(self, n_components: int = 2, **kwargs) -> pd.DataFrame:
        """
        Performs Principal Component Analyzer (PCA).

        Args:
            n_components (int): Number of components to keep. Defaults to 2.
            **kwargs: Additional arguments for PCA.

        Returns:
            pd.DataFrame: The dataset with reduced dimensions.
        """
        model = PCA(n_components=n_components, **kwargs)
        reduced_data = model.fit_transform(self._data)
        return pd.DataFrame(
            reduced_data, columns=[f"PC{i+1}" for i in range(n_components)]
        )


# ------------------------------------------------------------------------------------------------ #
class TSNEAnalyzer(MultivariateAnalyzer):
    """
    A class to perform t-Distributed Stochastic Neighbor Embedding (t-SNE) for dimensionality reduction.

    Methods:
        analyze(n_components: int = 2, perplexity: float = 30.0, **kwargs) -> pd.DataFrame:
            Performs t-SNE.
    """

    def analyze(
        self, n_components: int = 2, perplexity: float = 30.0, **kwargs
    ) -> pd.DataFrame:
        """
        Performs t-Distributed Stochastic Neighbor Embedding (t-SNE).

        Args:
            n_components (int): Number of components to keep. Defaults to 2.
            perplexity (float): Perplexity parameter. Defaults to 30.0.
            **kwargs: Additional arguments for t-SNE.

        Returns:
            pd.DataFrame: The dataset with reduced dimensions.
        """
        model = TSNE(n_components=n_components, perplexity=perplexity, **kwargs)
        reduced_data = model.fit_transform(self._data)
        return pd.DataFrame(
            reduced_data, columns=[f"Dim{i+1}" for i in range(n_components)]
        )
