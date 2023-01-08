import logging
import re

from wtforglib.scribe import Scribe

# mypy: disable_error_code = var-annotated

RECORD = "I am a log record."
SYSLOG_RECORD = "I am a syslog record."


def test_screen_logger(capsys):
    """Test screen logger."""
    scribe = Scribe(level="debug")
    scribe.logger.debug(RECORD)
    captured = capsys.readouterr()
    assert re.search(r"DEBUG:\s+I am a log record.", captured.err)
    assert scribe.handlers_nbr == 1


def test_bad_level(capsys):
    """Test screen logger."""
    scribe = Scribe(level="dunno")
    scribe.logger.info(RECORD)
    captured = capsys.readouterr()
    assert re.search(r"INFO:\s+I am a log record.", captured.err)
    assert scribe.handlers_nbr == 1


def test_screen_logger_warn(capsys):
    """Test screen logger."""
    scribe = Scribe(level="warn")
    scribe.logger.debug(RECORD)
    scribe.logger.warning(RECORD)
    captured = capsys.readouterr()
    assert not re.search(r"DEBUG:\s+I am a log record.", captured.err)
    assert re.search(r"WARNING:\s+I am a log record.", captured.err)
    assert scribe.handlers_nbr == 1


def test_file_logger(caplog, tmp_path_factory):
    """Test file logger."""
    fn = tmp_path_factory.mktemp("wtforg") / "scribe.log"
    caplog.set_level(logging.DEBUG, logger="wtfscribe")
    scribe = Scribe(level="debug", logfn=fn)
    scribe.logger.debug(RECORD)
    assert re.match(
        r"DEBUG\s+wtfscribe:test_scribe.py:\d+\sI am a log record.",
        caplog.text,
    )
    assert scribe.handlers_nbr == 1


def test_syslog_logger(caplog):
    """Test syslog logger."""
    caplog.set_level(logging.DEBUG, logger="wtfscribe")
    scribe = Scribe(level="debug", syslognm="wtfo")
    # TODO: find out why call to syslog handle raised exception
    assert scribe.handlers_nbr == 1


def test_all_handlers(caplog, tmp_path_factory):
    """Test all logger."""
    fn = tmp_path_factory.mktemp("wtforg") / "scribe.log"
    caplog.set_level(logging.DEBUG, logger="wtfscribe")
    scribe = Scribe(
        level="debug",
        syslognm="wtfo",
        logfn=fn,
        screen=True,
    )
    # TODO: find out why call to syslog handle raised exception
    assert scribe.handlers_nbr == 3
