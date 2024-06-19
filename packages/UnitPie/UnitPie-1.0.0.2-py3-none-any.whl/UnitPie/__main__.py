import sys

from .data import required_python, version

if sys.version_info < (3, 9):
    raise ImportError(f"`UnitPy` requires python {required_python} and/or higher!")

if any(t for t in sys.argv if t in ['-v', '-version']):
    print(f"UnitPy, version: {version}")