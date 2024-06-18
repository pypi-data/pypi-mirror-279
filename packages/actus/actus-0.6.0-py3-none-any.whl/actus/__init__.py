"""
Actus
-----

A logging library for python development

Includes:
- `info`
- `warn`
- `error`
- `LogSection`
- `Style`
- `highlight`
"""

__version__ = "0.6.0"
__all__ = [
    "info",
    "warn",
    "error",
    "LogSection",
    "Style",
    "highlight"
]

from colex import (
    SEA_GREEN as _DEFAULT_INFO_COLOR,
    ORANGE as _DEFAULT_WARN_COLOR,
    CRIMSON as _DEFAULT_ERROR_COLOR,
)

from ._log_section import LogSection
from ._style import Style
from ._highlighting import highlight


info = LogSection("Info", style=Style(
    label=_DEFAULT_INFO_COLOR
))
warn = LogSection("Warning", style=Style(
    label=_DEFAULT_WARN_COLOR
))
error = LogSection("Error", style=Style(
    label=_DEFAULT_ERROR_COLOR
))
