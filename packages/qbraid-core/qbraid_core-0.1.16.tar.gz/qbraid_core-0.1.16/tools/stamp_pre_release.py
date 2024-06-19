# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Script for getting/bumping the next pre-release version.

"""
import pathlib

from qbraid_core.system.versions import get_prelease_version

if __name__ == "__main__":

    PACKAGE = "qbraid_core"
    root = pathlib.Path(__file__).parent.parent.resolve()
    version = get_prelease_version(root, PACKAGE)
    print(version)
