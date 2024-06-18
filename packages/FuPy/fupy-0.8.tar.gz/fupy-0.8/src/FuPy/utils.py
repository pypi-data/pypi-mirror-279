"""
Utilities to support functional programming in Python.

Copyright (c) 2024 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""
import inspect
from typing import Any, Callable

__all__ = [
    "count_required_args",
    "indent_lines",
    "show_value", "show_args",
]


def count_required_args(f: Callable[..., Any]) -> int:
    """Count the minimum number of required non-keyword arguments of f.
    Does not work for built-in functions (use parameter r to bypass this).
    """
    from FuPy.basics import Func
    if isinstance(f, Func):
        return 1

    sig = inspect.signature(f)

    def parameter_is_required(p: inspect.Parameter) -> bool:
        return p.default is inspect.Parameter.empty and p.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )

    return sum(parameter_is_required(p) for p
               in sig.parameters.values())


def indent_lines(line: str, indentation: str = '', k: int = 0) -> str:
    """Indent each line by n spaces, except for the first k lines.
    """
    lines = line.split('\n')
    return '\n'.join([f"{'' if index < k else indentation}{line}" for index, line in enumerate(lines)])


def show_value(value) -> str:
    """Show value, quoting strings.
    """
    # print(f"show_value(repr={value!r}, str={value!s})")
    if isinstance(value, tuple) and not value:
        return "_"
    elif isinstance(value, str):
        return repr(value)
    else:
        return str(value)


def show_args(args: tuple[Any, ...]) -> str:
    """Show tuple as a string, with strings quoted, without trailing comma if singleton.

    N.B. The singleton case does not occur in case of auto-(un)packing of arguments.
    """
    if not args:
        return "_"
    elif len(args) == 1:
        from FuPy.basics import Func
        arg = args[0]
        if isinstance(arg, Func):
            return arg.str('.')
        else:
            return show_value(arg)
    else:
        return f"({', '.join(show_value(arg) for arg in args)})"
