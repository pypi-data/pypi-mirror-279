import sys

import configparser

config = configparser.ConfigParser()
config.read_file(open(r'data.cfg'))
reqired_python = config.get('VERSION', "required_python")
VERSION = config.get('VERSION', "version")

if sys.version_info < (3, 9):
    raise ImportError(f"`UnitPy` requires python {reqired_python} and/or higher!")

if any(t for t in sys.argv if t in ['-v', '-version']):
    print(f"UnitPy, version: {VERSION}")