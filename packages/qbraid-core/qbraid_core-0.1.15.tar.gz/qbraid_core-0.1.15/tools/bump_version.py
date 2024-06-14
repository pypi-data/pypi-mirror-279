# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Script to bump the major, minor, or patch version in pyproject.toml.

"""
import pathlib
import sys

from qbraid_core.system.versions import bump_version, extract_version, update_version_in_pyproject

if __name__ == "__main__":

    bump_type = sys.argv[1]
    root = pathlib.Path(__file__).parent.parent.resolve()
    pyproject_toml_path = root / "pyproject.toml"
    old_version = extract_version(pyproject_toml_path)
    new_version = bump_version(old_version, bump_type)
    update_version_in_pyproject(pyproject_toml_path, new_version)
    print(new_version)
