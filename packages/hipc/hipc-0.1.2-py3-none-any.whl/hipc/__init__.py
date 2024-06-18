# read version from installed package
from importlib.metadata import version
__version__ = version("hipc")

from .sync import Port
from .job import Parameters
