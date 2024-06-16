#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ================================================================================================ #
# Project    : Explorify                                                                           #
# Version    : 0.1.0                                                                               #
# Python     : 3.10.12                                                                             #
# Filename   : /explorify/__main__.py                                                              #
# ------------------------------------------------------------------------------------------------ #
# Author     : John James                                                                          #
# Email      : john@variancexplained.com                                                           #
# URL        : https://github.com/variancexplained/explorify                                       #
# ------------------------------------------------------------------------------------------------ #
# Created    : Thursday June 13th 2024 05:37:52 pm                                                 #
# Modified   : Friday June 14th 2024 08:28:29 pm                                                   #
# ------------------------------------------------------------------------------------------------ #
# License    : MIT License                                                                         #
# Copyright  : (c) 2024 John James                                                                 #
# ================================================================================================ #
import sys

from explorify.container import VisualizeContainer

# ------------------------------------------------------------------------------------------------ #
if __name__ == "__main__":  # pragma: no cover
    container = VisualizeContainer()
    container.init_resources()
    container.wire(modules=[sys.modules[__name__]], packages=["explorify"])
