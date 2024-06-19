import sys

import configparser

config = configparser.ConfigParser()
config.read_file(open(r'data.cfg'))
reqired_python = config.get('VERSION', "required_python")

if sys.version_info < (3, 9):
    raise ImportError(f"`UnitPy` requires python {reqired_python} and/or higher!")

from .FunctionTesting import main, test, ignore
from .SubClassManagement import TestCase