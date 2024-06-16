#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/eda/visualize/visualizer.py                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 06:25:27 am                                               #
# Modified   : Saturday June 15th 2024 05:10:17 am                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Wrapper for several Seaborn plotting functions."""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import List, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.gridspec import GridSpec
from scipy import stats
from wordcloud import WordCloud

from explorify import DataClass
from explorify.eda.visualize.base import Canvas, Colors
from explorify.eda.visualize.base import Visualizer as VisualizerABC

# ------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------ #
#                                            PALETTES                                              #
# ------------------------------------------------------------------------------------------------ #
@dataclass
class Palettes(DataClass):
    blues: str = "Blues"
    blues_r: str = "Blues_r"
    mako: str = "mako"
    bluegreen: str = "crest"
    paired: str = "Paired"
    dark: str = "dark"
    colorblind: str = "colorblind"
    darkblue = sns.dark_palette("#69d", reverse=False, as_cmap=False)
    darkblue_r = sns.dark_palette("#69d", reverse=True, as_cmap=False)
    winter_blue = sns.color_palette(
        [
            Colors.cool_black,
            Colors.police_blue,
            Colors.teal_blue,
            Colors.pale_robin_egg_blue,
        ],
        as_cmap=True,
    )
    blue_orange = sns.color_palette(
        [
            Colors.russian_violet,
            Colors.dark_cornflower_blue,
            Colors.meat_brown,
            Colors.peach,
        ],
        as_cmap=True,
    )


# ------------------------------------------------------------------------------------------------ #
#                                            CANVAS                                                #
# ------------------------------------------------------------------------------------------------ #


@dataclass
class SeabornCanvas(Canvas):
    """SeabornCanvas class encapsulating figure level configuration."""

    width: int = 12  # The maximum width of the canvas
    height: int = 4  # The height of a single row.
    maxcols: int = 2  # The maximum number of columns in a multi-plot visualization.
    color = Colors().dark_blue
    palette = Palettes().blues_r  # Seaborn palette or matplotlib colormap
    style: str = "whitegrid"  # A Seaborn aesthetic
    saturation: float = 0.5
    fontsize: int = 10
    fontsize_title: int = 16
    colors: Colors = Colors()
    palettes: Palettes = Palettes()

    def get_figaxes(
        self, nplots: int = 1, figsize: tuple = None
    ) -> SeabornCanvas:  # pragma: no cover
        """Configures the figure and axes objects.

        Args:
            nplots (int): The number of plots to be rendered on the canvas.
            figsize (tuple[int,int]): Plot width and row height.
        """
        figsize = figsize or (self.width, self.height)

        if nplots == 1:
            fig, axes = plt.subplots(figsize=figsize)
        else:
            nrows = math.ceil(nplots / self.maxcols)
            ncols = min(self.maxcols, nplots)

            fig = plt.figure(layout="constrained", figsize=figsize)
            gs = GridSpec(nrows=nrows, ncols=ncols, figure=fig)

            axes = []
            for idx in range(nplots):
                row = int(idx / ncols)
                col = idx % ncols

                if idx < nplots - 1:
                    ax = fig.add_subplot(gs[row, col])
                else:
                    ax = fig.add_subplot(gs[row, col:])
                axes.append(ax)

        return fig, axes


# ------------------------------------------------------------------------------------------------ #
class Visualizer(VisualizerABC):  # pragma: no cover
    """Wrapper for Seaborn plotizations."""

    def __init__(self, canvas: SeabornCanvas = SeabornCanvas()):
        super().__init__(canvas)

    def lineplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Draw a line plot with possibility of several semantic groupings.

        The relationship between x and y can be shown for different subsets of the data using the
        hue, size, and style parameters. These parameters control what visual semantics are used to
        identify the different subsets. It is possible to show up to three dimensions independently
        by using all three semantic types, but this style of plot can be hard to interpret and is
        often ineffective. Using redundant semantics (i.e. both hue and style for the same variable)
        can be helpful for making graphics more accessible.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        palette = self._canvas.palette if hue is not None else None
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.lineplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def scatterplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Draw a scatter plot with possibility of several semantic groupings.

        The relationship between x and y can be shown for different subsets of the data using the
        hue, size, and style parameters. These parameters control what visual semantics are used to
        identify the different subsets. It is possible to show up to three dimensions independently
        by using all three semantic types, but this style of plot can be hard to interpret and is
        often ineffective. Using redundant semantics (i.e. both hue and style for the same variable)
        can be helpful for making graphics more accessible.

        Args: Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        palette = self._canvas.palette if hue is not None else None
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.scatterplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def histogram(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        stat: str = "density",
        element: str = "bars",
        fill: bool = True,
        annotate: bool = False,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> None:
        """Draw a scatter plot with possibility of several semantic groupings.

        The relationship between x and y can be shown for different subsets of the data using the
        hue, size, and style parameters. These parameters control what visual semantics are used to
        identify the different subsets. It is possible to show up to three dimensions independently
        by using all three semantic types, but this style of plot can be hard to interpret and is
        often ineffective. Using redundant semantics (i.e. both hue and style for the same variable)
        can be helpful for making graphics more accessible.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            annotate (bool): Whether to annotate the plot with min, max, and mean values.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            stat (str): Aggregate statistics for each bin. Optional. Default is 'density'.
                See https://seaborn.pydata.org/generated/seaborn.histplot.html for valid values.
            element (str): Visual representation of the histogram statistic. Only relevant with univariate data. Optional. Default is 'bars'. fill (bool): If True, fill in the space under the histogram. Only relevant with univariate data.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        palette = self._canvas.palette if hue is not None else None
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.histplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            stat=stat,
            element=element,
            fill=fill,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )

        if annotate:
            ax = self._annotate(ax=ax, data=data, x=x)

        if title is not None:
            _ = ax.set_title(title)

        return ax

    def boxplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        ax: plt.Axes = None,
        figsize: bool = (12, 4),
        **kwargs,
    ) -> plt.Axes:
        """Draw a box plot to show distributions with respect to categories.

        A box plot (or box-and-whisker plot) shows the distribution of quantitative data in a way
        that facilitates comparisons between variables or across levels of a categorical variable.
        The box shows the quartiles of the dataset while the whiskers extend to show the rest of the
        distribution, except for points that are determined to be “outliers” using a method that is
        a function of the inter-quartile range.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        palette = self._canvas.palette if hue is not None else None
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.boxplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def countplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        orient: str = None,
        order_by_count: bool = False,
        plot_counts: bool = False,
        title: str = None,
        figsize: bool = (12, 4),
        rotate_ticks: Tuple[str, int] = None,
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Show the counts of observations in each categorical bin using bars.

        A count plot can be thought of as a histogram across a categorical, instead of quantitative, variable. The basic API and options are identical to those for barplot(), so you can compare counts across nested variables.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or
                numeric, although color mapping will behave differently in latter case.
            orient (str): 'v' or 'h'. Orientation of the plot (vertical or horizontal). This is usually
                inferred based on the type of the input variables, but it can be used to resolve ambiguity
                when both x and y are numeric or when plotting wide-form data.
            order_by_count (bool): If True, bars are ordered by counts.
            plot_counts (bool): If True, the bars are annotated with absolute and relative counts. Default = False
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            rotate_ticks (Tuple[str,int]): Tuple containing the axis and degrees of rotation. Default is None
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.

        """

        palette = self._canvas.palette if hue is not None else "Blues_r"
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)
        total = len(data)
        if orient is None:
            if x is None and y is not None:
                orient = "h"
            else:
                orient = "v"

        if order_by_count:
            col = x if x is not None else y
            order = data[col].value_counts().index
        else:
            order = None

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.countplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            order=order,
            palette=palette,
            *args,
            **kwargs,
        )

        if plot_counts:
            if orient == "v":
                for p in ax.patches:
                    x = p.get_bbox().get_points()[:, 0]
                    y = p.get_bbox().get_points()[1, 1]
                    ax.annotate(
                        text=f"{round(y,0)}\n({round(y/total*100,1)}%)",
                        xy=(x.mean(), y),
                        ha="center",
                        va="bottom",
                    )
            else:
                for p in ax.patches:
                    x = p.get_x() + p.get_width()
                    y = p.get_y() + p.get_height() / 2
                    ax.annotate(
                        text=f"{round(p.get_width(),0)} ({round(p.get_width()/total*100,1)}%)",
                        xy=(x, y),
                        va="center",
                    )

        if rotate_ticks is not None:
            try:
                ax = self._rotate_ticks(
                    ax=ax, axis=rotate_ticks[0], rotate=rotate_ticks[1]
                )
            except IndexError as ie:
                raise IndexError(
                    f"rotate_ticks parameter is malformed. Must be Tuple[str,int]. \n{ie}"
                )

        if title is not None:
            _ = ax.set_title(title)

        return ax

    def barplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        orient: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        rotate_ticks: Tuple[str, int] = None,
        palette: str = None,
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Show point estimates and errors as rectangular bars.

        A bar plot represents an estimate of central tendency for a numeric variable with the height of each
        rectangle and provides some indication of the uncertainty around that estimate using error bars. Bar
        plots include 0 in the quantitative axis range, and they are a good choice when 0 is a meaningful
        value for the quantitative variable, and you want to make comparisons against it.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            orient (str): 'v' or 'h'. Orientation of the plot (vertical or horizontal). This is usually
                inferred based on the type of the input variables, but it can be used to resolve ambiguity
                when both x and y are numeric or when plotting wide-form data.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            rotate_ticks (Tuple[str,int]): Tuple containing the axis and degrees of rotation. Default is None
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.

        """
        palette = self._canvas.palette if hue is not None else None
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            fig, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.barplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            orient=orient,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )

        if rotate_ticks is not None:
            try:
                ax = self._rotate_ticks(
                    ax=ax, axis=rotate_ticks[0], rotate=rotate_ticks[1]
                )
            except IndexError as ie:
                raise IndexError(
                    f"rotate_ticks parameter is malformed. Must be Tuple[str,int]. \n{ie}"
                )

        if title is not None:
            _ = ax.set_title(title)

        if hue is not None:
            plt.legend(loc="upper right")

        return ax

    def pareto(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray],
        cum_column: str,
        n: str = 10,
        x: str = None,
        y: str = None,
        hue: str = None,
        orient: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        rotate_ticks: Tuple[str, int] = None,
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Show a pareto plot with frequency counts and a cumulative proportion line.

        Takes a dataframe containing counts and cumulative proportions, sorted to plot.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            cum_column: The name of the column containing cumulative proportions.
            n (int): The number of rows to plot from the top.
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            orient (str): 'v' or 'h'. Orientation of the plot (vertical or horizontal). This is usually
                inferred based on the type of the input variables, but it can be used to resolve ambiguity
                when both x and y are numeric or when plotting wide-form data.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            rotate_ticks (Tuple[str,int]): Tuple containing the axis and degrees of rotation. Default is None
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.

        """
        palette = self._canvas.palette if hue is not None else "Blues_r"
        title = title or f"Pareto Plot\nTop {n} {x} Categories."

        if ax is None:
            fig, ax = self._canvas.get_figaxes(figsize=figsize)

        # Prepare the data
        data = data.iloc[0:n, :]

        # Plot the barplot of frequencies.
        ax = sns.barplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            orient=orient,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )

        # Plot the cumulative proportions.
        ax2 = ax.twinx()
        ax2 = sns.lineplot(
            data=data,
            x=x,
            y=data[cum_column],
            color="r",
            markers="o",
            linestyle="-",
            linewidth=2,
            ax=ax2,
        )
        ax2.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda y, _: "{:.0%}".format(y))
        )
        ax2.set_ylabel("Cumulative Percentage")

        if rotate_ticks is not None:
            try:
                ax = self._rotate_ticks(
                    ax=ax, axis=rotate_ticks[0], rotate=rotate_ticks[1]
                )
            except IndexError as ie:
                raise IndexError(
                    f"rotate_ticks parameter is malformed. Must be Tuple[str,int]. \n{ie}"
                )

        if title is not None:
            _ = ax.set_title(title)

        if hue is not None:
            plt.legend(loc="upper right")

        return ax

    def kdeplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Plot univariate or bivariate distributions using kernel density estimation.

        A kernel density estimate (KDE) plot is a method for visualizing the distribution of
        observations in a dataset, analogous to a histogram. KDE represents the data using a
        continuous probability density curve in one or more dimensions.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        palette = self._canvas.palette if hue is not None else "Blues_r"
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.kdeplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def kdebox_one(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        annotate: bool = True,
        **kwargs,
    ) -> plt.Axes:
        """A figure level visualization for univariate distributions.

        A kernel density estimate (KDE) and boxen plot used as a method for visualizing
        the distribution of observations in a dataset, analogous to a histogram.
        KDE represents the data using a continuous probability density curve in one.
        The boxen plot represents the distribution as a box plot.

        Note: This method only supports one-dimensional data along
        the x axis. Therefore, no hue or grouping functionality is provided.
        If multiple dimensions are being analyzed, use kdeplot.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x (str): Keys in data.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            annotate (bool): Whether to annotate plot with min, max, and mean


        """
        palette = "Blues_r"
        data = data if data is not None else self._data
        title = title or self.autotitle(x)

        fig, axes = plt.subplots(
            nrows=2,
            ncols=1,
            gridspec_kw={"height_ratios": [3, 1]},
            figsize=figsize,
            sharex=True,
        )

        # Density Plot
        axes[0] = sns.kdeplot(
            data=data,
            x=x,
            ax=axes[0],
            palette=palette,
            *args,
            **kwargs,
        )

        # Annotations
        if annotate:
            ax = self._annotate(ax=axes[0], data=data, x=x)

        # Boxen Plot
        axes[1] = sns.boxenplot(data=data, x=x, orient="h")

        if title is not None:
            _ = fig.suptitle(title, weight="bold")

        plt.tight_layout()
        return ax

    def ecdfplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> None:
        """Plot empirical cumulative distribution functions.

        An ECDF represents the proportion or count of observations falling below each unique value
        in a dataset. Compared to a histogram or density plot, it has the advantage that each
        observation is visualized directly, meaning that there are no binning or smoothing
        parameters that need to be adjusted. It also aids direct comparisons between multiple
        distributions. A downside is that the relationship between the appearance of the plot and
        the basic properties of the distribution (such as its central tendency, variance, and the
        presence of any bimodality) may not be as intuitive.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.

        """
        palette = self._canvas.palette if hue is not None else "Blues_r"
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.ecdfplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def violinplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Draw a combination of boxplot and kernel density estimate.

        A violin plot plays a similar role as a box and whisker plot. It shows the distribution of
        quantitative data across several levels of one (or more) categorical variables such that those
        distributions can be compared. Unlike a box plot, in which all of the plot components correspond to
        actual datapoints, the violin plot features a kernel density estimation of the underlying
        distribution.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        palette = self._canvas.palette if hue is not None else "Blues_r"
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.violinplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            ax=ax,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def regplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Plot data and a linear regression model fit.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        if ax is None:
            fig, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.regplot(
            data=data,
            x=x,
            y=y,
            ax=ax,
            fit_reg=True,
            color=self._canvas.colors.dark_blue,
            *args,
            **kwargs,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def pdfcdfplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        **kwargs,
    ) -> plt.Figure:
        """Renders a combination of the probabiity density and cumulative distribution functions.

        This visualization provides the probability density function and cumulative distribution
        function in a single plot with shared x-axis.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
        """
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        fig, ax1 = self._canvas.get_figaxes(figsize=figsize)

        ax1 = sns.kdeplot(
            data=data,
            x=x,
            y=y,
            color=self._canvas.colors.dark_blue,
            ax=ax1,
            label="Probability Density Function",
            legend=True,
        )
        ax2 = ax1.twinx()
        ax2 = sns.kdeplot(
            data=data,
            x=x,
            y=y,
            cumulative=True,
            ax=ax2,
            color=self._canvas.colors.orange,
            label="Cumulative Distribution Function",
            legend=True,
        )
        title = "Probability Density Function and Cumulative Distribution Function"

        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()

        ax1.legend(handles=h1 + h2, labels=l1 + l2, loc="upper left")
        fig.suptitle(title, fontsize=self._canvas.fontsize_title)
        fig.tight_layout()

        plt.close()

        return fig

    def pairplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        include: list = None,
        hue: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        **kwargs,
    ) -> sns.PairGrid:
        """Plot pairwise relationships in a dataset.

        By default, this function will create a grid of Axes such that each numeric variable in data
        will by shared across the y-axes across a single row and the x-axes across a single column.
        The diagonal plots are treated differently: a univariate distribution plot is drawn to show
        the marginal distribution of the data in each column.

        It is also possible to show a subset of variables or plot different variables on the rows
        and columns.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure.
                Either a long-form collection of vectors that can be assigned to named variables or
                a wide-form dataset that will be internally reshaped
            include (list): Variables within data to use, otherwise use every column with a numeric datatype. Optional, if not provided all numeric columns will be included.
            hue (str): Grouping variable that will produce lines with different colors. Can be
            either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.


        """
        palette = self._canvas.palette if hue is not None else "Blues_r"
        data = data if data is not None else self._data

        g = sns.pairplot(
            data=data,
            vars=include,
            hue=hue,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            g.figure.suptitle(title)
        g.tight_layout()

        return g

    def jointplot(
        self,
        *args,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        y: str = None,
        hue: str = None,
        title: str = None,
        figsize: bool = (12, 4),
        **kwargs,
    ) -> sns.JointGrid:
        """Draw a plot of two variables with bivariate and univariate graphs.

        Args:
            data (Union[pd.DataFrame, np.ndarray]): Input data structure. Either a long-form
                collection of vectors that can be assigned to named variables or a wide-form dataset
                that will be internally reshaped
            x,y (str): Keys in data.
            hue (str): Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.


        """

        palette = self._canvas.palette if hue is not None else "Blues_r"
        data = data if data is not None else self._data
        title = title or self.autotitle(x, y)

        g = sns.jointplot(
            data=data,
            x=x,
            y=y,
            hue=hue,
            palette=palette,
            *args,
            **kwargs,
        )
        if title is not None:
            g.figure.suptitle(title)
        g.figure.tight_layout()

        return g

    def ttestplot(
        self,
        *args,
        statistic: float,
        dof: int,
        alpha: float = 0.05,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Draw the results of a t-test with the statistic and reject regions.

        Args:
            statistic (float): The student's t test statistic
            dof (int): Degrees of freedom
            alpha (float): The statistical significance. Default is 0.05.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        # Render the probability distribution
        x = np.linspace(stats.t.ppf(0.001, dof), stats.t.ppf(0.999, dof), 500)
        y = stats.t.pdf(x, dof)
        ax = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=ax)

        # Compute reject region
        lower = x[0]
        upper = x[-1]
        lower_alpha = alpha / 2
        upper_alpha = 1 - (alpha / 2)
        lower_critical = stats.t.ppf(lower_alpha, dof)
        upper_critical = stats.t.ppf(upper_alpha, dof)

        # Fill lower tail
        xlower = np.arange(lower, lower_critical, 0.001)
        ax.fill_between(
            x=xlower,
            y1=0,
            y2=stats.t.pdf(xlower, dof),
            color=self._canvas.colors.orange,
        )

        # Fill Upper Tail
        xupper = np.arange(upper_critical, upper, 0.001)
        ax.fill_between(
            x=xupper,
            y1=0,
            y2=stats.t.pdf(xupper, dof),
            color=self._canvas.colors.orange,
        )

        # Plot the statistic
        line = ax.lines[0]
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        statistic = round(statistic, 4)

        try:
            idx = np.where(xdata > statistic)[0][0]
            x = xdata[idx]
            y = ydata[idx]
            _ = sns.regplot(
                x=np.array([x]),
                y=np.array([y]),
                scatter=True,
                fit_reg=False,
                marker="o",
                scatter_kws={"s": 100},
                ax=ax,
                color=self._canvas.colors.dark_blue,
            )
            ytext = 10
            if np.isclose(statistic, 0, atol=1e-1):
                ytext *= -2

            ax.annotate(
                f"t = {str(statistic)}",
                (x, y),
                textcoords="offset points",
                xytext=(0, ytext),
                ha="center",
            )
        except IndexError:
            pass

        ax.annotate(
            "Critical Value",
            (lower_critical, 0),
            textcoords="offset points",
            xytext=(20, 15),
            ha="left",
            arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
        )

        ax.annotate(
            "Critical Value",
            (upper_critical, 0),
            xycoords="data",
            textcoords="offset points",
            xytext=(-20, 15),
            ha="right",
            arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
        )

        _ = ax.set_title(
            f"{title}",
            fontsize=self._canvas.fontsize_title,
        )

        plt.tight_layout()

        return ax

    def x2testplot(
        self,
        *args,
        statistic: float,
        dof: int,
        alpha: float = 0.05,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        # Render the probability distribution
        x = np.linspace(stats.chi2.ppf(0.01, dof), stats.chi2.ppf(0.99, dof), 100)
        y = stats.chi2.pdf(x, dof)
        ax = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=ax)

        # Compute reject region
        upper = x[-1]
        upper_alpha = 1 - alpha
        critical = stats.chi2.ppf(upper_alpha, dof)

        # Fill Upper Tail
        x = np.arange(critical, upper, 0.001)
        ax.fill_between(
            x=x,
            y1=0,
            y2=stats.chi2.pdf(x, dof),
            color=self._canvas.colors.orange,
        )

        # Plot the statistic
        line = ax.lines[0]
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        statistic = round(statistic, 4)
        try:
            idx = np.where(xdata > statistic)[0][0]
            x = xdata[idx]
            y = ydata[idx]
            _ = sns.regplot(
                x=np.array([x]),
                y=np.array([y]),
                scatter=True,
                fit_reg=False,
                marker="o",
                scatter_kws={"s": 100},
                ax=ax,
                color=self._canvas.colors.dark_blue,
            )
            ax.annotate(
                rf"$X^2$ = {str(statistic)}",
                (x, y),
                textcoords="offset points",
                xytext=(0, 20),
                ha="center",
            )
        except IndexError:
            pass

        ax.annotate(
            "Critical Value",
            (critical, 0),
            xycoords="data",
            textcoords="offset points",
            xytext=(-20, 15),
            ha="right",
            arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
        )

        _ = ax.set_title(
            f"{title}",
            fontsize=self._canvas.fontsize_title,
        )

        ax.set_xlabel(r"$X^2$")
        ax.set_ylabel("Probability Density")
        plt.tight_layout()

        return ax

    def kstestplot(
        self,
        *args,
        statistic: float,
        n: int,
        alpha: float = 0.05,
        title: str = None,
        figsize: bool = (12, 4),
        ax: plt.Axes = None,
        **kwargs,
    ) -> plt.Axes:
        """Draw the results of a t-test with the statistic and reject regions.

        Args:
            statistic (float): The student's t test statistic
            dof (int): Degrees of freedom
            alpha (float): The statistical significance. Default is 0.05.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            ax: (plt.Axes): A matplotlib Axes object. Optional. If not provide, one will be obtained from the canvas.


        """
        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        # Render the probability distribution
        x = np.linspace(stats.kstwo.ppf(0.001, n), stats.kstwo.ppf(0.999, n), 500)
        y = stats.kstwo.pdf(x, n)
        ax = sns.lineplot(x=x, y=y, markers=False, dashes=False, sort=True, ax=ax)

        # Compute reject region
        lower = x[0]
        upper = x[-1]
        lower_alpha = alpha / 2
        upper_alpha = 1 - (alpha / 2)
        lower_critical = stats.kstwo.ppf(lower_alpha, n)
        upper_critical = stats.kstwo.ppf(upper_alpha, n)

        # Fill lower tail
        xlower = np.arange(lower, lower_critical, 0.001)
        ax.fill_between(
            x=xlower,
            y1=0,
            y2=stats.kstwo.pdf(xlower, n),
            color=self._canvas.colors.orange,
        )

        # Fill Upper Tail
        xupper = np.arange(upper_critical, upper, 0.001)
        ax.fill_between(
            x=xupper,
            y1=0,
            y2=stats.kstwo.pdf(xupper, n),
            color=self._canvas.colors.orange,
        )

        # Plot the statistic
        line = ax.lines[0]
        xdata = line.get_xydata()[:, 0]
        ydata = line.get_xydata()[:, 1]
        statistic = round(statistic, 4)

        try:
            idx = np.where(xdata > statistic)[0][0]
            x = xdata[idx]
            y = ydata[idx]
            _ = sns.regplot(
                x=np.array([x]),
                y=np.array([y]),
                scatter=True,
                fit_reg=False,
                marker="o",
                scatter_kws={"s": 100},
                ax=ax,
                color=self._canvas.colors.dark_blue,
            )
            ytext = 10
            if np.isclose(statistic, 0, atol=1e-1):
                ytext *= -2

            ax.annotate(
                f"t = {str(statistic)}",
                (x, y),
                textcoords="offset points",
                xytext=(0, ytext),
                ha="center",
            )
        except IndexError:
            pass

        ax.annotate(
            "Critical Value",
            (lower_critical, 0),
            textcoords="offset points",
            xytext=(20, 15),
            ha="left",
            arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
        )

        ax.annotate(
            "Critical Value",
            (upper_critical, 0),
            xycoords="data",
            textcoords="offset points",
            xytext=(-20, 15),
            ha="right",
            arrowprops={"width": 2, "headwidth": 4, "shrink": 0.05},
        )

        _ = ax.set_title(
            f"{title}",
            fontsize=self._canvas.fontsize_title,
        )

        plt.tight_layout()

        return ax

    def heatmap(
        self,
        *args,
        data: pd.DataFrame,
        vmin: float = None,
        vmax: float = None,
        cmap: str = "crest",
        robust: bool = False,
        annot: bool = True,
        fmt: str = ".2f",
        annot_kws: dict = None,
        cbar: bool = True,
        cbar_kws: dict = None,
        cbar_ax: plt.Axes = None,
        square: bool = True,
        xticklabels: Union["str", "bool", list, int] = "auto",
        yticklabels: Union["str", "bool", list, int] = "auto",
        mask: bool = None,
        ax: plt.Axes = None,
        title: str = None,
        figsize: bool = (12, 4),
        **kwargs,
    ) -> plt.Axes:
        """Plot rectangular data as a color-encoded matrix.

        Args:
            _data (pd.DataFrame): 2D Dataset that can be coerced into an ndarray.
                If a Pandas DataFrame is provided, the index/column information
                will be used to label the columns and rows
            vmin, vmax: Values to anchor the colormap, otherwise they are inferred from the data and other keyword arguments.

            cmap (matplotlib colormap): The mapping from data values to color space.
            robust (bool): If True and vmin or vmax are absent, the colormap range is computed with robust quantiles instead of the extreme values.
            annot (bool): If True, write the data value in each cell. If an array-like with the same shape as data, then use this to annotate the heatmap instead of the data. Note that DataFrames will match on position, not index.
            fmt (str): String formatting code to use when adding annotations. Default = ".2f"
            annot_kws (dict): Keyword arguments for matplotlib.axes.Axes.text() when annot is True.
            cbar (bool): Whether to draw a colorbar.
            cbar_kws (dict): Keyword arguments for matplotlib.figure.Figure.colorbar().
            cbar_ax (matplotlib.Axes): Axes in which to draw the colorbar, otherwise take space from the main Axes.
            square (bool): If True, set the Axes aspect to “equal” so each cell will be square-shaped.
            xticklabels, yticklabels (Union['str', 'bool', list, int]): f True, plot the column names of the dataframe. If False, don't plot the column names. If list-like, plot these alternate labels as the xticklabels. If an integer, use the column names but plot only every n label. If “auto”, try to densely plot non-overlapping labels.
            mask (bool): If passed, data will not be shown in cells where mask is True. Cells with missing values are automatically masked.
            ax (matplotlib.Axes): Axes in which to draw the plot, otherwise use the currently-active Axes.
            title (str): Title for the plot. Optional
            figsize (tuple): Size of figure in inches. Ignored if ax is provided.
            kwargs (dict): All other keyword arguments are passed to matplotlib.axes.Axes.pcolormesh().

        Returns: ax (matplotlib.Axes): Axes object with the heatmap.

        """

        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        ax = sns.heatmap(
            data=data,
            vmin=vmin,
            vmax=vmax,
            cmap=cmap,
            robust=robust,
            annot=annot,
            fmt=fmt,
            annot_kws=annot_kws,
            cbar=cbar,
            cbar_kws=cbar_kws,
            cbar_ax=cbar_ax,
            square=square,
            xticklabels=xticklabels,
            yticklabels=yticklabels,
            mask=mask,
            ax=ax,
        )
        if title is not None:
            _ = ax.set_title(title)

        return ax

    def top_n_wordcloud(
        self,
        data: Union[pd.DataFrame, np.ndarray] = None,
        x: str = None,
        n: int = 100,
        width: int = 800,
        height: int = 400,
        title: str = None,
        ax: plt.Axes = None,
        figsize: bool = (12, 4),
        **kwargs,
    ) -> WordCloud:
        """Wordcloud is a figure level plot for the top n categories by count.

        Args:
           data (Union[pd.DataFrame, np.ndarray]): Input data structure.
               Either a long-form collection of vectors that can be assigned to named variables or
               a wide-form dataset that will be internally reshaped
           x (str): Variable to count
           n (int): Number of rows from the top to include. Default = 100
           width (int): Width of wordcloud. Default = 800
           height (int): Height of wordcloud. Default = 400
           title (str): Title for the plot. Optional
           ax (plt.Axes): Matplotlib Axes object. Default is None
           figsize (tuple): Size of figure in inches. Ignored if ax is provided.


        """
        if ax is None:
            _, ax = self._canvas.get_figaxes(figsize=figsize)

        # Set the title
        title = title or f"Top {n} {x} Word Cloud"

        # Set the data
        data = data if data is not None else self._data

        # Calculate value counts and sort in descending order
        value_counts_sorted = data[x].value_counts().sort_values(ascending=False)

        # Select top N most frequent values
        top_n_values = value_counts_sorted.head(n)

        # Convert to dictionary for WordCloud
        word_freq_dict = top_n_values.to_dict()

        # Generate WordCloud
        wordcloud = WordCloud(
            width=width, height=height, background_color="white"
        ).generate_from_frequencies(word_freq_dict)

        # Plot WordCloud on the specified Axes object
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(title)

        return ax

    def _wrap_ticklabels(
        self, axis: str, axes: List[plt.Axes], fontsize: int = 8
    ) -> List[plt.Axes]:
        """Wraps long tick labels"""
        if axis.lower() == "x":
            for i, ax in enumerate(axes):
                xlabels = [label.get_text() for label in ax.get_xticklabels()]
                xlabels = [label.replace(" ", "\n") for label in xlabels]
                ax.set_xticklabels(xlabels, fontdict={"fontsize": fontsize})
                ax.tick_params(axis="x", labelsize=fontsize)

        if axis.lower() == "y":
            for i, ax in enumerate(axes):
                ylabels = [label.get_text() for label in ax.get_yticklabels()]
                ylabels = [label.replace(" ", "\n") for label in ylabels]
                ax.set_yticklabels(ylabels, fontdict={"fontsize": fontsize})
                ax.tick_params(axis="y", labelsize=fontsize)

        return axes

    def _annotate(
        self, ax: plt.Axes, data: Union[pd.DataFrame, np.ndarray], x: str
    ) -> plt.Axes:
        """Annotates an axis with min, max, and mean lines and text annotations."""
        # If x is not None, we assume a dataframe.
        if x is not None:
            x_min = np.min(data[x])
            x_mean = np.mean(data[x])
            x_max = np.max(data[x])
        else:
            x_min = np.min(data)
            x_mean = np.mean(data)
            x_max = np.max(data)

        # Get y limits which will be used to designated
        # Text position
        bottom, top = ax.get_ylim()

        # Get x_range and y_range, a we will be needed them to plot
        # the text
        x_range = x_max - x_min
        y_range = top - bottom

        # Determines distance between vertical line and left and right
        # text positions. x_range is the distance between the max and min
        # values. Text is positioned some fraction f of x_range
        # to the right of the vertical line.
        f = 1 / 60

        text_shift_x_right = f * x_range

        # The y-coordinates for Min, Mean, and Max will be 0.25, 0.5, and 0.75
        # of the y_range, respectively
        text_y_min_factor = 0.25
        text_y_mean_factor = 0.5
        text_y_max_factor = 0.75

        # Set x, y values for min, max, and mean text annotations
        text_min_x = x_min + text_shift_x_right
        text_min_y = bottom + y_range * text_y_min_factor

        text_mean_x = x_mean + text_shift_x_right
        text_mean_y = bottom + y_range * text_y_mean_factor

        text_max_x = x_max + text_shift_x_right
        text_max_y = bottom + y_range * text_y_max_factor

        # Draw min,mean, and max vertical lines
        ax.axvline(x=x_min, ls=":", lw=2, color="black")
        ax.axvline(x=x_mean, ls=":", lw=2, color="black")
        ax.axvline(x=x_max, ls=":", lw=2, color="black")

        # Draw text annotations
        ax.text(
            x=text_min_x,
            y=text_min_y,
            s=f"min: {round(x_min,1)}",
            size=8,
            color="black",
            weight="bold",
        )
        ax.text(
            x=text_mean_x,
            y=text_mean_y,
            s=f"mean: {round(x_mean,1)}",
            size=8,
            color="black",
            weight="bold",
        )
        ax.text(
            x=text_max_x,
            y=text_max_y,
            s=f"max: {round(x_max,1)}",
            size=8,
            color="black",
            weight="bold",
        )

        return ax

    def _rotate_ticks(
        self, ax: plt.Axes, axis: str = "x", rotate: int = 45
    ) -> plt.Axes:
        """Rotates ticks on x or y axis."""
        if axis == "x":
            _ = ax.set_xticks(
                ax.get_xticks(),
                ax.get_xticklabels(),
                rotation=rotate,
                ha="right",
            )
        elif axis == "y":
            _ = ax.set_yticks(
                ax.get_yticks(),
                ax.get_yticklabels(),
                rotation=rotate,
                va="center",
            )
        else:
            raise ValueError(
                f"Value for axis = {axis} is invalid. It must be 'x' or 'y'."
            )

        return ax
