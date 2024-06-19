# SPDX-FileCopyrightText: (C) 2023 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

"""Utility collection for scotty-test."""

import subprocess
import os
import tempfile
from typing import Tuple


class Utils():
    """Utils for scotty-test."""

    @staticmethod
    def run_interactive(*args, **kwargs) -> int:
        """Run a command in interactive mode."""
        p = subprocess.Popen(*args, shell=True, **kwargs)
        while True:
            try:
                p.communicate()
            except KeyboardInterrupt:
                pass
            else:
                break

        return p.poll()

    @staticmethod
    def run(*args, **kwargs) -> bool:
        """Run a command and return the exit status."""
        try:
            subprocess.check_call(*args, **kwargs)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def run_output(*args, **kwargs) -> Tuple[bool, str]:
        """Run a command and return the output."""
        try:
            return (True, subprocess.check_output(*args, universal_newlines=True, stderr=subprocess.STDOUT, **kwargs))
        except subprocess.CalledProcessError as e:
            return (False, e.stdout)

    @staticmethod
    def do_in_tempdir(func, *args, **kwargs) -> None:
        """Run code from a temporary directory."""
        ccwd = os.getcwd()
        with tempfile.TemporaryDirectory() as t:
            os.chdir(t)
            func(*args, **kwargs)
        os.chdir(ccwd)
