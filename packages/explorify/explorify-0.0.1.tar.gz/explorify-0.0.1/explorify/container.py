#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/container.py                                                             #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john.james.ai.studio@gmail.com                                                      #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Saturday August 26th 2023 09:31:46 am                                               #
# Modified   : Thursday June 13th 2024 06:21:52 pm                                                 #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2023 John James                                                                 #
# ================================================================================================ #
"""Framework Dependency Container"""
from dependency_injector import containers, providers

from explorify.eda.visualize.visualizer import SeabornCanvas, Visualizer


# ------------------------------------------------------------------------------------------------ #
#                                    VISUALIZER CONTAINER                                          #
# ------------------------------------------------------------------------------------------------ #
class VisualizeContainer(containers.DeclarativeContainer):

    canvas = providers.Factory(SeabornCanvas)
    visualizer = providers.Factory(Visualizer, canvas=canvas)
