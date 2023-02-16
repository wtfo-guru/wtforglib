"""Top-level module for Wtforg Library."""

import subprocess
import sys
from typing import Tuple, Union

from wtforglib.options import Options


class FakedProcessResult(object):
    """Faked process result."""

    stdout: str
    stderr: str
    returncode: int

    def __init__(self, stdout: str = "", stderr: str = "", returncode: int = 0) -> None:
        """Creates a fake process result.

        Parameters
        ----------
        stdout : str
            Fake stdout
        stderr : str
            Fake stderr
        returncode : int
            Fake returcode
        """
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode


if sys.version_info >= (3, 9):
    CommanderResult = Union[subprocess.CompletedProcess[str], FakedProcessResult]
else:
    CommanderResult = Union[subprocess.CompletedProcess, FakedProcessResult]


class Commander(Options):
    """Base class for subprocess management."""

    def run_command(
        self,
        args: Tuple[str, ...],
        **kwargs: bool,
    ) -> CommanderResult:
        """Runs commands specified by args."""
        always = kwargs.get("always", False)
        check = kwargs.get("check", True)
        cmd_str = "{0}".format(" ".join(args))
        if not always and self.isnoop():
            print("noex: {0}".format(cmd_str))
            return FakedProcessResult()
        self.verbose("ex: {0}".format(cmd_str), 2)
        return subprocess.run(
            args,
            check=check,
            shell=False,  # noqa: S603
            capture_output=True,
            encoding="utf-8",
        )
