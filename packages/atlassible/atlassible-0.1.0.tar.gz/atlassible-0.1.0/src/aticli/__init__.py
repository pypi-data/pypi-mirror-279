""" atlassible/src/aticli/__init__.py

the command line interface tool for atlassible
use the same version as the atlassible package 
"""

# read version from installed package
from importlib.metadata import version

__version__ = version("atlassible")


from aticli.main import app

app_name = "aticli"


def run():
    app(prog_name=app_name)

## end of file