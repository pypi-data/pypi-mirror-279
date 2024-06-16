#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/base.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 10:26:48 pm                                                 #
# Modified   : Saturday June 15th 2024 03:24:32 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
from abc import ABC

import pandas as pd
from dependency_injector.wiring import Provide, inject

from explorify.container import VisualizeContainer
from explorify.eda.visualize.visualizer import Visualizer


# ------------------------------------------------------------------------------------------------ #
class Analyzer(ABC):
    """Abstract base class for all analyses"""

    @inject
    def __init__(
        self,
        data: pd.DataFrame,
        visualizer: Visualizer = Provide[VisualizeContainer.visualizer],
    ) -> None:
        super().__init__()
        self._data = data
        self._visualizer = visualizer
