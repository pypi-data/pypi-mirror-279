#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.10                                                                             #
# Filename   : /explorify/eda/stats/descriptive/categorical.py                                     #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 8th 2023 02:56:56 am                                                  #
# Modified   : Sunday June 9th 2024 12:25:04 pm                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
import statistics
from dataclasses import dataclass
from typing import Union

import numpy as np
import pandas as pd

from explorify import DataClass


# ------------------------------------------------------------------------------------------------ #
@dataclass
class CategoricalStats(DataClass):
    name: str  # Name of variable
    length: int  # total  length of variable
    count: int  # number of non-null values
    size: float  # total number of bytes
    mode: Union[int, str]
    unique: int

    @classmethod
    def describe(cls, x: Union[pd.Series, np.ndarray], name: str = None) -> None:
        return cls(
            name=name,
            length=len(x),
            count=len(list(filter(None, x))),
            size=x.__sizeof__(),
            mode=statistics.mode(x),
            unique=len(np.unique(x)),
        )
