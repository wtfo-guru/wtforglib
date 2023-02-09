"""Top-level module for Aguada Tools Library."""

from typing import Dict, Optional, Union

OptionsDict = Dict[str, Union[str, int, bool]]

OPTIONS_DEBUG = "debug"
OPTIONS_TEST = "test"
OPTIONS_VERBOSE = "verbose"


def basic_options(
    debug: Union[bool, int],
    test: bool,
    verbose: Union[bool, int],
) -> OptionsDict:
    """Return a dictionary of basic options.

    Parameters
    ----------
    debug : Union[bool, int]
        Sets debug: int in the returned dictionary
    test : bool
        Sets test: bool in the returned dictionary
    verbose : Union[bool, int]
        Sets verbose: int in the returned dictionary

    Returns
    -------
    OptionsDict
        Options dictionary
    """
    od: OptionsDict = {}
    od["debug"] = int(debug) if isinstance(debug, bool) else debug
    od["test"] = test
    od["verbose"] = int(verbose) if isinstance(verbose, bool) else verbose
    return od


class Options(object):
    """A class to handle Options."""

    options: OptionsDict

    def __init__(self, opts: Optional[OptionsDict] = None) -> None:
        """Options constructor.

        Class to manage options for the module.

        Parameters
        ----------
        opts : OptionsDict Optional
            Options to merge with defaults
        """
        self.options = {OPTIONS_DEBUG: 0, OPTIONS_VERBOSE: 0, OPTIONS_TEST: False}
        self.errors = 0
        if opts is not None:
            self.options.update(opts)
        if int(self.options[OPTIONS_DEBUG]) > 1:
            print(  # noqa: WPS421
                "created instance of class {0}".format(self.__class__.__name__),
            )

    def isdebug(self) -> bool:
        """Returns True if debug > 0."""
        return int(self.options[OPTIONS_DEBUG]) > 0

    def isverbose(self) -> bool:
        """Returns True if verbose > 0."""
        return int(self.options[OPTIONS_VERBOSE]) > 0

    def istest(self) -> bool:
        """Returns value of test flag."""
        return bool(self.options[OPTIONS_TEST])

    def trace(self, message: str) -> None:
        """Utility trace method."""
        print(message)  # noqa: WPS421

    def debug(self, message: str, level: int = 1) -> None:
        """Utility debug method."""
        dl: int = int(self.options[OPTIONS_DEBUG])
        if self.options[OPTIONS_TEST] or dl >= level:
            self.trace(message)

    def verbose(self, message: str, level: int = 1) -> None:
        """Utility verbose method."""
        vl: int = int(self.options[OPTIONS_VERBOSE])
        if self.options[OPTIONS_TEST] or vl >= level:
            self.trace(message)
