"""
Core definitions to support functional programming in Python.
Especially aimed at educational and not at industrial application.

Copyright (c) 2024 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""
from .basics import *
from .tracing import trace
from .laziness import *
from .fixpoints import *

# Sphinx needs __all__ for its automodule functionality
from .basics import __all__ as basics_all
from .laziness import __all__ as laziness_all
from .fixpoints import __all__ as fixpoints_all

__all__ = basics_all + ["trace"] + laziness_all + fixpoints_all
