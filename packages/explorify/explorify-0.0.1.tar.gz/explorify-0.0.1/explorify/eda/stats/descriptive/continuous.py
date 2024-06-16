#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /explorify/eda/stats/descriptive/continuous.py                                      #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 8th 2023 02:56:56 am                                                  #
# Modified   : Sunday June 9th 2024 12:25:15 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import logging
from dataclasses import dataclass
from typing import Union

import numpy as np
import pandas as pd
from scipy import stats

from explorify import DataClass

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------ #
@dataclass
class ContinuousStats(DataClass):
    name: str  # Name of the variable
    length: int  # total  length of variable
    count: int  # number of non-null values
    size: int  # total number of bytes
    min: float
    q25: float
    mean: float
    median: float
    q75: float
    max: float
    range: float
    std: float
    var: float
    skew: float
    kurtosis: float

    @classmethod
    def describe(cls, x: Union[pd.Series, np.ndarray], name: str = None) -> None:
        return cls(
            name=name,
            length=len(x),
            count=len(list(filter(None, x))),
            size=x.__sizeof__(),
            mean=np.mean(x),
            std=np.std(x),
            var=np.var(x),
            min=np.min(x),
            q25=np.percentile(x, q=25),
            median=np.median(x),
            q75=np.percentile(x, q=75),
            max=np.max(x),
            range=np.max(x) - np.min(x),
            skew=stats.skew(x),
            kurtosis=stats.kurtosis(x, bias=False),
        )
