# get the version
from importlib.metadata import version
__version__ = version('dalab')

from . import utils
from .visual import (
    set_style,
    showfig,
    closefig,
    savefig,
)

from .dart import DART
