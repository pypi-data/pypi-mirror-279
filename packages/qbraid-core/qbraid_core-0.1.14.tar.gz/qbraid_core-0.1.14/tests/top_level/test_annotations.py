# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for annotations (i.e. decorators).

"""
import pytest

from qbraid_core.annotations import deprecated


@deprecated
def mock_deprecated_function() -> None:
    """A mock function that does nothing."""
    pass


def test_deprecated_decorator():
    """Test that the deprecated decorator emits a warning."""
    with pytest.warns(
        DeprecationWarning, match="Call to deprecated function mock_deprecated_function."
    ):
        mock_deprecated_function()
