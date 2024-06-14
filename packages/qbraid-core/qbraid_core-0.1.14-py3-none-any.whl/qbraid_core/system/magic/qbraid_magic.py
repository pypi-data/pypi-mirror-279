# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining custom qBraid IPython magic commands.

"""

import os
import shlex
import subprocess
import sys
from pathlib import Path

from IPython.core.magic import Magics, line_magic, magics_class


@magics_class
class SysMagics(Magics):
    """
    Custom IPython Magics class to allow running
    qBraid-CLI commands from within Jupyter notebooks.

    """

    @line_magic
    def qbraid(self, line):
        """
        Executes qBraid-CLI command using the sys.executable
        from a Jupyter Notebook kernel.

        """
        original_path = os.environ["PATH"]
        yes_values = {"true", "1", "t", "y", "yes"}
        show_progress = os.getenv("QBRAID_CLI_SHOW_PROGRESS", "true").lower() in yes_values
        python_dir = str(Path(sys.executable).parent)

        try:
            # Prepend the Python interpreter's directory to PATH
            os.environ["PATH"] = python_dir + os.pathsep + original_path
            os.environ["QBRAID_CLI_SHOW_PROGRESS"] = "false"

            # Call your main script
            command = ["qbraid"] + shlex.split(line)
            subprocess.run(command, check=True)

        finally:
            # Restore the original PATH after the script completes
            os.environ["PATH"] = original_path
            os.environ["QBRAID_CLI_SHOW_PROGRESS"] = show_progress


def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(SysMagics)
