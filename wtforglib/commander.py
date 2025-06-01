"""Top-level module for Wtforg Library."""

import subprocess
from typing import Tuple, Union

from wtforglib.options import Options


class FakedProcessResult:
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


CommanderResult = Union[subprocess.CompletedProcess[str], FakedProcessResult]


class Commander(Options):
    """Base class for subprocess management."""

    def run_command(
        self,
        args: Tuple[str, ...],
        **kwargs: bool,
    ) -> CommanderResult:
        """
        Runs a command.

        Parameters
        ----------
        args : Tuple[str, ...]
            Command and arguments to run
        **kwargs : bool
            Keyword arguments

        Keyword Arguments
        -----------------
        always : bool
            If set to True, command will be run even if we are in noexec mode.
            (default: False)
        check : bool
            If set to True, will check the return code of the command and
            raise a CalledProcessError if it is not 0.
            (default: True)

        Returns
        -------
        CommanderResult
            CompletedProcess or FakedProcessResult
        """
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
