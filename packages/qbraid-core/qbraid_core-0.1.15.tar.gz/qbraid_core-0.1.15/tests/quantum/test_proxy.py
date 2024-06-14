# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Unit tests for checking the quantum jobs proxy state.

"""

from importlib.metadata import PackageNotFoundError
from unittest.mock import MagicMock, patch

import pytest

from qbraid_core.services.quantum.proxy import SUPPORTED_QJOB_LIBS, quantum_lib_proxy_state
from qbraid_core.services.quantum.proxy_braket import _check_proxy_braket

qjobs_libs = list(SUPPORTED_QJOB_LIBS.keys())


@pytest.mark.parametrize("device_lib", qjobs_libs)
def test_proxy_state_no_packages_installed(device_lib):
    """Test checking proxy state when none of the required packages are installed."""
    with patch(
        "qbraid_core.services.quantum.proxy_braket.distribution", side_effect=PackageNotFoundError
    ):
        result = quantum_lib_proxy_state(device_lib)
        assert result == {"supported": False, "enabled": False}


def test_proxy_state_raises_for_unsupported_library():
    """Test checking proxy state when an unsupported library is specified."""
    with pytest.raises(ValueError):
        quantum_lib_proxy_state("unsupported_library")


@pytest.mark.parametrize("dependency", ["amazon-braket-sdk", "boto3", "botocore"])
def test_braket_proxy_package_not_installed(dependency):
    """Test checking proxy state when a required package is not installed."""

    def side_effect(package_name):
        if package_name == dependency:
            raise PackageNotFoundError(f"No package named {package_name}")
        return MagicMock(metadata={})

    with patch("qbraid_core.services.quantum.proxy_braket.distribution", side_effect=side_effect):
        result = _check_proxy_braket()
        assert result == (False, False)


def test_braket_proxy_native_botocore():
    """Test checking proxy state when all required packages are installed but botocore is not the qBraid fork."""

    def mock_distribution(package_name):
        if package_name == "botocore":
            return MagicMock(metadata={"Home-page": "https://github.com/boto/botocore"})
        else:
            return MagicMock(metadata={})  # Default metadata for other packages

    with patch(
        "qbraid_core.services.quantum.proxy_braket.distribution", side_effect=mock_distribution
    ):
        result = _check_proxy_braket()
        assert result == (True, False)


def test_braket_proxy_qbraid_botocore():
    """Test checking proxy state when botocore is installed from the qBraid fork."""

    def mock_distribution(package_name):
        if package_name == "botocore":
            return MagicMock(metadata={"Home-page": "https://github.com/qBraid/botocore"})
        else:
            return MagicMock(metadata={})  # Default metadata for other packages

    with patch(
        "qbraid_core.services.quantum.proxy_braket.distribution", side_effect=mock_distribution
    ):
        result = _check_proxy_braket()
        assert result == (True, True)
