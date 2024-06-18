"""Does Python not have enough features? MorePy is here to change that!"""

import sys

if sys.version_info < (3, 10):
    raise ImportError("The `MorePy` library requires python version 3.10 or higher!")

try:
    import numpy
except ModuleNotFoundError as e:
    raise ModuleNotFoundError("The `numpy` library is required for MorePy!")

from .ErrorSuppressor import ErrorSuppressor, CreateErrorSuppressor
from . import MoreTypes
from .MoreTypes import HashMaps, Matrixes
from .MoreTypes.HashMaps import HashMap
from .MoreTypes.Matrixes import Matrix, ColumnTypes, Column
from .Sums import *
from . import MoreConsole as Console
from .MoreConsole import *