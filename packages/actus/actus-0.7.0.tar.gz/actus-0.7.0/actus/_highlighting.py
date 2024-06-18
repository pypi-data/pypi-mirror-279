import re as _re
from functools import partial as _partial

from ._style import Style as _Style

import colex as _colex


_BRACKET_CONTENT_PATTERN = _re.compile(r"\$\[([^]]+)\]")


def _replace_match(
    match: _re.Match[str],
    /,
    *,
    style: _Style | None = None
) -> str:
    if style is None:
        return match.group(1)
    return style.highlight + match.group(1) + style.text


def highlight(
    string: str,
    /,
    *,
    style: _Style | None = None
) -> str:
    partial_replace_match = _partial(_replace_match, style=style)
    replaced = _BRACKET_CONTENT_PATTERN.sub(partial_replace_match, string)
    if style is None:
        return replaced
    return (
        style.text
        + replaced
        + _colex.RESET
    )
