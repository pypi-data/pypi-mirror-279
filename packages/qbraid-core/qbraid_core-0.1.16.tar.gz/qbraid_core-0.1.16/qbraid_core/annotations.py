# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining function annotations (e.g. decorators) used in qbraid-core.

"""
import functools
import warnings
from typing import Any


def deprecated(func: Any) -> Any:
    """
    This decorator is used to mark functions as deprecated.
    It will result in a warning being emitted when the function is used.

    """

    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter("always", DeprecationWarning)
        warnings.warn(
            f"Call to deprecated function {func.__name__}.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        warnings.simplefilter("default", DeprecationWarning)
        return func(*args, **kwargs)

    return new_func
