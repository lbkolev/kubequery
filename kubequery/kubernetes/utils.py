# mypy: ignore-errors

import functools
from typing import Any


def rgetattr(obj, attr: Any, *args) -> Any:
    """Get a nested attribute from an object."""

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj, *attr.split(".")])
