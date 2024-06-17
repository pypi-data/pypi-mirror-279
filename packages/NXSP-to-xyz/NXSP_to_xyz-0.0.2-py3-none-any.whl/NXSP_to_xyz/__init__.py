print(r'The tools for Sampled condition from NX to .xyz')

import sys
if sys.version_info < (3, 8):
    raise ImportError("Python version 3.8 or above is required for PyFastPaper.")
del sys

__docformat__ = "restructuredtext"

# Let users know if they're missing any of our hard dependencies
_hard_dependencies = (
	"numpy",
	"pandas",
	"ase",
)
_missing_dependencies = []

for _dependency in _hard_dependencies:
    try:
        __import__(_dependency)
    except ImportError as _e:  # pragma: no cover
        _missing_dependencies.append(f"{_dependency}: {_e}")

if _missing_dependencies:  # pragma: no cover
    raise ImportError(
        "Unable to import required dependencies:\n" + "\n".join(_missing_dependencies)
    )
del _hard_dependencies, _dependency, _missing_dependencies

from .NXSP_to_xyz import (
    NX_to_xyz
)

from ase import units
import pandas as pd


__version__ = '0.0.1'

# module level doc-string
__doc__ = """
### 主要功能：
- 1. Sampled condition from NX to .xyz；

"""

# Use __all__ to let type checkers know what is part of the public API.

