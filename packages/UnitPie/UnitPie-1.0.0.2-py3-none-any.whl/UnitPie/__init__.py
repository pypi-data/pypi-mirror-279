import sys

from .data import required_python

if sys.version_info < (3, 9):
    raise ImportError(f"`UnitPy` requires python {required_python} and/or higher!")

from .FunctionTesting import main, test, ignore
from .SubClassManagement import TestCase