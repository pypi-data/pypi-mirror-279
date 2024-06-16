#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/multivariate/cluster.py                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 08:32:12 pm                                                 #
# Modified   : Saturday June 15th 2024 03:52:38 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage
from sklearn.cluster import DBSCAN, KMeans

from explorify.eda.multivariate.base import MultivariateAnalyzer

# ------------------------------------------------------------------------------------------------ #


class KMeansAnalyzer(MultivariateAnalyzer):
    """
    A class to perform K-Means clustering analysis.

    Methods:
        analyze(n_clusters: int = 3, **kwargs) -> pd.DataFrame:
            Performs K-Means clustering.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data)

    def analyze(self, n_clusters: int = 3, **kwargs) -> pd.DataFrame:
        """
        Performs K-Means clustering.

        Args:
            n_clusters (int): The number of clusters to form. Defaults to 3.
            **kwargs: Additional arguments for KMeans.

        Returns:
            pd.DataFrame: The dataset with cluster labels.
        """
        model = KMeans(n_clusters=n_clusters, **kwargs)
        clusters = model.fit_predict(self._data)
        self._data["cluster"] = clusters
        return self._data


# ------------------------------------------------------------------------------------------------ #
class HierarchicalAnalyzer(MultivariateAnalyzer):
    """
    A class to perform Hierarchical clustering analysis.

    Methods:
        analyze(n_clusters: int = 3, method: str = 'ward', **kwargs) -> pd.DataFrame:
            Performs Hierarchical clustering.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data)

    def analyze(
        self, n_clusters: int = 3, method: str = "ward", **kwargs
    ) -> pd.DataFrame:
        """
        Performs Hierarchical clustering.

        Args:
            n_clusters (int): The number of clusters to form. Defaults to 3.
            method (str): The linkage method to use. Defaults to 'ward'.
            **kwargs: Additional arguments for linkage.

        Returns:
            pd.DataFrame: The dataset with cluster labels.
        """
        Z = linkage(self._data, method=method, **kwargs)
        self._data["cluster"] = fcluster(Z, n_clusters, criterion="maxclust")
        return self._data


# ------------------------------------------------------------------------------------------------ #
class DBSCANAnalyzer(MultivariateAnalyzer):
    """
    A class to perform DBSCAN clustering analysis.

    Methods:
        analyze(eps: float = 0.5, min_samples: int = 5, **kwargs) -> pd.DataFrame:
            Performs DBSCAN clustering.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        super().__init__(data)

    def analyze(self, eps: float = 0.5, min_samples: int = 5, **kwargs) -> pd.DataFrame:
        """
        Performs DBSCAN clustering.

        Args:
            eps (float): The maximum distance between two samples for one to be considered as in the neighborhood of the other. Defaults to 0.5.
            min_samples (int): The number of samples in a neighborhood for a point to be considered as a core point. Defaults to 5.
            **kwargs: Additional arguments for DBSCAN.

        Returns:
            pd.DataFrame: The dataset with cluster labels.
        """
        model = DBSCAN(eps=eps, min_samples=min_samples, **kwargs)
        self._data["cluster"] = model.fit_predict(self._data)
        return self._data
