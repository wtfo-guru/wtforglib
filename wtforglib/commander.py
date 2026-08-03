"""Top-level module for Wtforg Library."""

import subprocess

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


CommanderResult = subprocess.CompletedProcess[str] | FakedProcessResult


class Commander(Options):
    """Base class for subprocess management."""

    def run_command(
        self,
        args: tuple[str, ...],
        **kwargs: bool,
    ) -> CommanderResult:
        """
        Run a command.

        Parameters
        ----------
        args : Tuple[str, ...]
            List of arguments to pass to subprocess
        kwargs : bool
            Keyword arguments, see below

        Keyword Arguments
        -----------------
        always : bool
            If True, always run the command, even if isnoop() returns True
            (default: False)
        check : bool
            If True, check the return code of the command and raise
            CalledProcessError if it is not 0 (default: True)

        Returns
        -------
        CommanderResult
            CompletedProcess or FakedProcessResult
        """
        always = kwargs.get("always", False)
        check = kwargs.get("check", True)
        cmd_str = "{}".format(" ".join(args))
        if not always and self.isnoop():
            print(f"noex: {cmd_str}")
            return FakedProcessResult()
        self.verbose(f"ex: {cmd_str}", 2)
        return subprocess.run(
            args,
            check=check,
            shell=False,
            capture_output=True,
            encoding="utf-8",
        )
