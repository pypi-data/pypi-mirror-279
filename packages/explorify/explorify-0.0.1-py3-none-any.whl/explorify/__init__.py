#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/__init__.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Friday June 7th 2024 09:04:48 pm                                                    #
# Modified   : Sunday June 9th 2024 11:25:02 am                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
"""Application-Wide Objects Module"""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd

# ------------------------------------------------------------------------------------------------ #
IMMUTABLE_TYPES: tuple = (
    str,
    int,
    float,
    bool,
    np.int16,
    np.int32,
    np.int64,
    np.int8,
    np.float16,
    np.float32,
    np.float64,
    np.float128,
)
SEQUENCE_TYPES: tuple = (
    list,
    tuple,
)
# ------------------------------------------------------------------------------------------------ #
NUMERIC_TYPES = [
    "int16",
    "int32",
    "int64",
    "float16",
    "float32",
    "float64",
    "datetime",
    "datetime64",
    "datetime64[ns]",
    np.int16,
    np.int32,
    np.int64,
    np.int8,
    np.float16,
    np.float32,
    np.float64,
    np.float128,
    np.number,
    np.datetime64,
    int,
    float,
    complex,
]

# ------------------------------------------------------------------------------------------------ #
NON_NUMERIC_TYPES = ["category", "object", "string"]


# ------------------------------------------------------------------------------------------------ #
@dataclass
class DataClass(ABC):
    def __repr__(self) -> str:  # pragma: no cover tested, but missing in coverage
        s = "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                "{}={!r}".format(k, v)
                for k, v in self.__dict__.items()
                if type(v) in IMMUTABLE_TYPES
            ),
        )
        return s

    def __str__(self) -> str:
        width = 32
        breadth = width * 2
        s = f"\n\n{self.__class__.__name__.center(breadth, ' ')}"
        d = self.as_dict()
        for k, v in d.items():
            if type(v) in IMMUTABLE_TYPES:
                k = k.capitalize()
                s += f"\n{k.rjust(width,' ')} | {v}"
        s += "\n\n"
        return s

    def as_dict(self) -> dict:
        """Returns a dictionary representation of the the Config object."""
        return {
            k: self._export_config(v)
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        }

    @classmethod
    def _export_config(cls, v):  # pragma: no cover
        """Returns v with Configs converted to dicts, recursively."""
        if isinstance(v, IMMUTABLE_TYPES):
            return v
        elif isinstance(v, SEQUENCE_TYPES):
            return type(v)(map(cls._export_config, v))
        elif isinstance(v, datetime):
            return v
        elif isinstance(v, dict):
            return v
        elif hasattr(v, "as_dict"):
            return v.as_dict()
        else:
            """Else nothing. What do you want?"""

    def as_df(self) -> pd.DataFrame:
        """Returns the project in DataFrame format"""
        d = self.as_dict()
        return pd.DataFrame(data=d, index=[0])
