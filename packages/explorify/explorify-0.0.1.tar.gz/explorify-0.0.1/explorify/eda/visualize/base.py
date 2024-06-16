#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/visualize/base.py                                                    #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 06:22:05 am                                               #
# Modified   : Sunday June 9th 2024 11:26:30 am                                                    #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union

import pandas as pd
import seaborn as sns

from explorify import DataClass
from explorify.utils.string import proper


# ------------------------------------------------------------------------------------------------ #
#                                           COLORS                                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Colors(DataClass):
    cool_black: str = "#002B5B"
    police_blue: str = "#2B4865"
    teal_blue: str = "#256D85"
    pale_robin_egg_blue: str = "#8FE3CF"
    russian_violet: str = "#231955"
    dark_cornflower_blue: str = "#1F4690"
    meat_brown: str = "#E8AA42"
    peach: str = "#FFE5B4"
    dark_blue: str = "#002B5B"
    blue: str = "#1F4690"
    orange: str = "#E8AA42"
    crimson: str = "#BA0020"

    def __post_init__(self) -> None:
        return


# ------------------------------------------------------------------------------------------------ #
#                                           CANVAS                                                 #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Canvas(DataClass):  # pragma: no
    """Namespace for Canvas subclasses"""


# ------------------------------------------------------------------------------------------------ #
#                                       VISUALIZER                                                 #
# ------------------------------------------------------------------------------------------------ #
class Visualizer(ABC):  # pragma: no cover
    """Wrapper for Seaborn visualizations.


    Args:
        canvas (Canvas): A dataclass containing the configuration of the canvas
            for the visualization.
    """

    @abstractmethod
    def __init__(self, canvas: Canvas, *args, **kwargs) -> None:  # pragma: no cover
        """Defines the construction requirement for Visualizers"""
        self._canvas = canvas
        self._data = None
        sns.set_style(style=self._canvas.style)
        sns.set_palette(palette=self._canvas.palette)

    @property
    def data(self) -> pd.DataFrame:
        return self._data

    @data.setter
    def data(self, data: pd.DataFrame) -> None:
        self._data = data

    @property
    def canvas(self) -> Canvas:
        return self._canvas

    @canvas.setter
    def canvas(self, canvas: Canvas) -> None:
        self._canvas = canvas
        sns.set_style(style=canvas.style)
        sns.set_palette(canvas.palette)

    @abstractmethod
    def lineplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def boxplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def kdeplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def ecdfplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def histogram(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def scatterplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def barplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def violinplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def ttestplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    @abstractmethod
    def x2testplot(self, *args, **kwargs) -> None:  # pragma: no cover
        """Renders the plot"""

    def autotitle(self, x: str, y: str = None) -> Union[str, None]:
        """Creates an automatic plot title based upon values of x and y.

        If x and y are not None, the title is in the format of y by x.
        If x or y is not None, the title is the proper form
        of the non-Null dimension. Otherwise, None
        is returned.

        Args:
            x (str): The x variable
            y (str): Variable to plotted on y axis.
        """
        if x and y:
            return f"{proper(y)} by {proper(x)}"
        elif x:
            return f"{proper(x)}"
        elif y:
            return f"{proper(y)}"
        else:
            return None
