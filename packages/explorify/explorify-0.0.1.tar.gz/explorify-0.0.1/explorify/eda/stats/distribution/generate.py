#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.11                                                                             #
# Filename   : /explorify/eda/stats/distribution/generate.py                                       #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday May 27th 2023 08:56:02 pm                                                  #
# Modified   : Thursday June 13th 2024 03:24:14 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Statistics Module"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
from scipy import stats

from explorify import DataClass

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------ #
NUM_POINTS = 5000
# ------------------------------------------------------------------------------------------------ #
#                                    SCIPY DISTRIBUTIONS                                           #
# ------------------------------------------------------------------------------------------------ #
DISTRIBUTIONS = {
    "beta": stats.beta,
    "norm": stats.norm,
    "X2": stats.chi2,
    "exponential": stats.expon,
    "f": stats.f,
    "gamma": stats.gamma,
    "logistic": stats.logistic,
    "lognorm": stats.lognorm,
    "uniform": stats.uniform,
    "weibull": stats.weibull_min,
}
# ------------------------------------------------------------------------------------------------ #
#                                    SCIPY CDF FUNCTIONS                                           #
# ------------------------------------------------------------------------------------------------ #
CDF = {
    "beta": stats.beta.cdf,
    "norm": stats.norm.cdf,
    "X2": stats.chi2.cdf,
    "exponential": stats.expon.cdf,
    "f": stats.f.cdf,
    "gamma": stats.gamma.cdf,
    "logistic": stats.logistic.cdf,
    "lognorm": stats.lognorm.cdf,
    "uniform": stats.uniform.cdf,
    "weibull": stats.weibull_min.cdf,
}


# ------------------------------------------------------------------------------------------------ #
#                                DISTRIBUTION DATACLASSES                                          #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Distribution(DataClass):
    name: str
    label: str
    formula: str
    params: str
    x: np.ndarray
    y: np.ndarray


# ------------------------------------------------------------------------------------------------ #
#                                   DATA GENERATORS                                                #
# ------------------------------------------------------------------------------------------------ #
def beta(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the beta distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    # Estimate parameters
    a, b, loc, scale = get_params(data=data, distribution="beta")

    name = "Beta Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = (
        r"$\alpha=$"
        + str(round(a, 2))
        + r", $\beta=$"
        + str(round(b, 2))
        + "\nloc = "
        + str(round(loc, 2))
        + ", scale = "
        + str(round(scale, 2))
    )
    formula = (
        r"$ f(x, \alpha, \beta) = \frac{\Gamma(\alpha+\beta) x^{\alpha-1} (1-x)^{\beta-1}} {\Gamma(\alpha) \Gamma(\beta)}$"
        + "\n"
        + r"where $\Gamma$ is the gamma function"
        + "\n"
        + "0 <= x <= 1"
        + "\n"
        + r"$\alpha$ > 0, $\beta$ > 0 are shape parameters"
    )

    size = size or len(data)

    # Random variate
    rvs = stats.beta.rvs(a, b, loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.beta.pdf(x=x_range, a=a, b=b, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.beta.cdf(x=x_range, a=a, b=b, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def norm(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the normal distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    # Estimate parameters
    loc, scale = get_params(data=data, distribution="norm")

    name = "Normal Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = "loc = " + str(round(loc, 2)) + ", scale = " + str(round(scale, 2))
    formula = (
        r"$ f(x) = \frac{\exp(-x^2/2)}{\sqrt{2\pi}}$" + "\n" + r"For real number x"
    )

    size = size or len(data)

    # Random variate
    rvs = stats.norm.rvs(loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.norm.pdf(x=x_range, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.norm.cdf(x=x_range, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def chi2(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the chi-squared distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    _, loc, scale = get_params(data=data, distribution="X2")
    df = len(data) - 1
    name = r"$\chi^2$ Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = "loc = " + str(round(loc, 2)) + ", scale = " + str(round(scale, 2))
    formula = (
        r"$ f(x, k) = \frac{1}{2^{k/2} \Gamma \left( k/2 \right)} x^{k/2-1} \exp \left( -x/2 \right)$"
        + "\n"
        + "for x>0 and k>0 (degrees of freedom)"
    )

    size = size or len(data)

    # Random variate
    rvs = stats.chi2.rvs(df=df, loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label=r"$\chi^2$ Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.chi2.pdf(x=x_range, df=df, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.chi2.cdf(x=x_range, df=df, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def exponential(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the exponential distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    loc, scale = get_params(data=data, distribution="exponential")
    rvs = stats.expon.rvs(loc=loc, scale=scale, size=size)
    name = "Exponential Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = "\nloc = " + str(round(loc, 2)) + ", scale = " + str(round(scale, 2))
    formula = r"$f(x) = \exp(-x)$" + "\n" + r"for x >= 0"

    size = size or len(data)

    # Random variate
    rvs = stats.expon.rvs(loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.expon.pdf(x=x_range, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.expon.cdf(x=x_range, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def f(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the f distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    dfn, dfd, loc, scale = get_params(data=data, distribution="f")
    name = "F Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = (
        r"$df_1=$"
        + str(round(dfn, 2))
        + r", $df_2$"
        + str(round(dfd, 2))
        + "\nloc = "
        + str(round(loc, 2))
        + ", scale = "
        + str(round(scale, 2))
    )
    formula = (
        r"$f(x, df_1, df_2) = \frac{df_2^{df_2/2} df_1^{df_1/2} x^{df_1 / 2-1}}{(df_2+df_1 x)^{(df_1+df_2)/2}B(df_1/2, df_2/2)}$"
        + "\n"
        + r"For x > 0 and parameters $df_1$, $df_2$ > 0"
    )

    size = size or len(data)

    # Random variate
    rvs = stats.f.rvs(dfn=dfn, dfd=dfd, loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.f.pdf(x=x_range, dfn=dfn, dfd=dfd, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.f.cdf(
        x=x_range,
        dfn=dfn,
        dfd=dfd,
        loc=loc,
        scale=scale,
    )
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def gamma(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the gamma distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    a, loc, scale = get_params(data=data, distribution="gamma")
    name = "Gamma Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = (
        "a ="
        + str(round(a, 2))
        + "\nloc = "
        + str(round(loc, 2))
        + ", scale = "
        + str(round(scale, 2))
    )
    formula = (
        r"$f(x, a) = \frac{x^{a-1} e^{-x}}{\Gamma(a)}$"
        + "\n"
        + r"For x >= 0, a > 0, and $\Gamma$ is the gamma function"
    )

    size = size or len(data)

    # Random variate
    rvs = stats.gamma.rvs(a, loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.gamma.pdf(x=x_range, a=a, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.gamma.cdf(x=x_range, a=a, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def logistic(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the logistic distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    loc, scale = get_params(data=data, distribution="logistic")
    name = "Logistic Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = "loc = " + str(round(loc, 2)) + ", scale = " + str(round(scale, 2))
    formula = r"$ f(x) = \frac{\exp(-x)}{(1+\exp(-x))^2}$"

    size = size or len(data)

    # Random variate
    rvs = stats.logistic.rvs(loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.logistic.pdf(x=x_range, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.logistic.cdf(x=x_range, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def lognorm(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the log normal distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    s, loc, scale = get_params(data=data, distribution="lognorm")
    name = "Lognorm Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = (
        "s ="
        + str(round(s, 2))
        + "\nloc = "
        + str(round(loc, 2))
        + ", scale = "
        + str(round(scale, 2))
    )
    formula = (
        r"$f(x, s) = \frac{1}{s x \sqrt{2\pi}}\exp\left(-\frac{\log^2(x)}{2s^2}\right)$"
        + "\n"
        + r"For x > 0, s > 0."
    )

    size = size or len(data)

    # Random variate
    rvs = stats.lognorm.rvs(s, loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.lognorm.pdf(x=x_range, s=s, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.lognorm.cdf(x=x_range, s=s, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def uniform(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the uniform distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    loc, scale = get_params(data=data, distribution="uniform")
    name = "Uniform Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = "loc = " + str(round(loc, 2)) + ", scale = " + str(round(scale, 2))
    formula = r"$ f(x) = \frac{1}{(b-a)}$" + "for a <= x <= b"

    size = size or len(data)

    # Random variate
    rvs = stats.uniform.rvs(loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.uniform.pdf(x=x_range, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.uniform.cdf(x=x_range, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def weibull(data: np.ndarray, size: int = None) -> np.ndarray:
    """Generates random variates for the uniform distribution

    Args:
        data (np.ndarray): 1D Numpy array of data from which parameters will be estimated.

    Returns:
        rvs: Random variate of the distribution
        pdf: Data from the probability density function
        cdf: Data from the cumulative distribution function
    """
    c, loc, scale = get_params(data=data, distribution="weibull")

    name = "Weibull Distribution"
    x_range = np.linspace(min(data), max(data), NUM_POINTS)
    params = (
        "c ="
        + str(round(c, 2))
        + "\nloc = "
        + str(round(loc, 2))
        + ", scale = "
        + str(round(scale, 2))
    )
    formula = r"$f(x, c) = c x^{c-1} \exp(-x^c)$" + "\n" + r"For x > 0, c > 0."
    size = size or len(data)
    # Random variate
    rvs = stats.weibull_min.rvs(c, loc=loc, scale=scale, size=size)
    rvs = Distribution(
        name=name,
        label="Random Variate",
        x=x_range,
        y=rvs,
        params=params,
        formula=formula,
    )

    # Probability density function
    pdf = stats.weibull_min.pdf(x=x_range, c=c, loc=loc, scale=scale)
    pdf = Distribution(
        name=name,
        label="Probability Density Function",
        formula=formula,
        params=params,
        x=x_range,
        y=pdf,
    )

    # Cumulative density function
    cdf = stats.weibull_min.cdf(x=x_range, c=c, loc=loc, scale=scale)
    cdf = Distribution(
        name=name,
        label="Cumulative Density Function",
        params=params,
        formula=formula,
        x=x_range,
        y=cdf,
    )

    return rvs, pdf, cdf


def get_params(data: np.ndarray, distribution: str) -> tuple:
    """Obtains the distribution parameters estimated from the data."""
    try:
        return DISTRIBUTIONS[distribution].fit(data)
    except AttributeError as e:  # pragma: no cover
        msg = f"{distribution.capitalize()} has no fit attribute."
        logger.error(msg)
        raise e


# ------------------------------------------------------------------------------------------------ #
#                               DISTRIBUTION GENERATOR                                             #
# ------------------------------------------------------------------------------------------------ #
class RVSDistribution:
    """Random variates for various distributions. Parameters estimated from data.

    The parameters for the specified distribution will be estimated from the data provided.
    It returns an array of data from the designated distribution, equal in length
    to the data provided.

    This is used by goodness of fit tests to evaluate the degree to which a distribution
    matches an hypothesized distribution.

    Args:
        _data (pd.DataFrame): Data from which distribution parameters are estimated.
    """

    __DISTRIBUTIONS = {
        "beta": beta,
        "norm": norm,
        "X2": chi2,
        "exponential": exponential,
        "f": f,
        "gamma": gamma,
        "logistic": logistic,
        "lognorm": lognorm,
        "uniform": uniform,
        "weibull": weibull,
        # "pareto": pareto,
    }

    def __init__(self) -> None:
        self._rvs = None
        self._pdf = None
        self._cdf = None
        self._distribution = None

    @property
    def data(self) -> np.ndarray:
        return self._data

    @property
    def rvs(self) -> Distribution:
        """Returns the random variate"""
        return self._rvs

    @property
    def pdf(self) -> Distribution:
        """Returns the random variate"""
        return self._pdf

    @property
    def cdf(self) -> Distribution:
        """Returns the random variate"""
        return self._cdf

    def __call__(
        self, data: np.ndarray, distribution: str, size: int = None
    ) -> np.ndarray:
        """Returns random values of the designated distribution

        Args:
            data (np.ndarray): The data from which the distribution parameters are estimated
            distribution (str): One of the supported distributions. See the README.
        """
        self._data = data
        self._distribution = distribution

        try:
            self._rvs, self._pdf, self._cdf = self.__DISTRIBUTIONS[distribution](
                data=data, size=size
            )
        except KeyError as e:  # pragma: no cover
            msg = f"{distribution} is not supported.\n{e}"
            logger.debug(msg)
            raise NotImplementedError(msg)
        return self
