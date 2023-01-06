"""Top-level module scribe for wtforglib."""


import logging
import logging.handlers
import sys

from wtforglib.kinds import Fspec


LOG_LEVELS = {
    "crit": logging.CRITICAL,
    "error": logging.ERROR,
    "warn": logging.WARN,
    "info": logging.INFO,
    "debug": logging.DEBUG,
}


class Scribe(object):
    def __init__(self, level: str, logfn: str="", syslognm: str="", screen: bool=False) -> None:

        self.log = logging.getLogger("wtfscribe")

        if level not in LOG_LEVELS:
            log_level = logging.INFO
        else:
            log_level = LOG_LEVELS[level]
        basic_configured = False
        basic_format = "%(asctime)s %(levelname)s: %(message)s",
        date_format = "%Y-%m-%d %H:%M:%S"
        if logfn:
            logging.basicConfig(
                filename=logfn, format=basic_format, datefmt=date_format, level=log_level,
            )
            basic_configured = True

        if syslognm:
            syslog = logging.handlers.SysLogHandler(address="/dev/log")
            syslog.setFormatter(logging.Formatter("[{0}] %(levelname)8s: %(message)s").format(syslognm))
            syslog.setLevel(log_level)
            self.log.addHandler(syslog)

        if screen:
            console = logging.StreamHandler()
            console.setLevel(level)
            # set a format which is simpler for console use
            formatter = logging.Formatter("%(levelname)8s: %(message)s")
            # tell the handler to use this format
            console.setFormatter(formatter)
            self.log.addHandler(console)

