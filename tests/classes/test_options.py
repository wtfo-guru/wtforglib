"""Test module for wtforglib package."""

from logging import WARNING

from wtforglib.options import Options, basic_options
from wtforglib.scribe import Scribe, log_level_name

# mypy: disable_error_code = var-annotated

DMESSAGE = "debug trace message"
VMESSAGE = "verbose trace message"
IMESSAGE = "info message"
WMESSAGE = "warning message"
EMESSAGE = "error message"


def test_options_default(capsys):
    """Test options default."""
    opts = Options()
    assert not opts.isdebug()
    assert not opts.istest()
    assert not opts.isverbose()
    opts.debug(DMESSAGE)
    opts.verbose(VMESSAGE)
    out, _err = capsys.readouterr()
    assert DMESSAGE not in out
    assert VMESSAGE not in out


def test_options_set(capsys):
    """Test basic set."""
    opts = Options(basic_options(True, True, True))
    assert opts.isdebug()
    assert opts.istest()
    assert opts.isverbose()
    opts.debug(DMESSAGE)
    opts.verbose(VMESSAGE)
    out, _err = capsys.readouterr()
    assert DMESSAGE in out
    assert VMESSAGE in out


def test_options_level(capsys):
    """Test options level."""
    opts = Options(basic_options(2, False, 1))
    assert opts.isdebug()
    assert opts.isverbose()
    opts.debug(DMESSAGE, 2)
    opts.verbose(VMESSAGE, 2)
    opts.info(IMESSAGE)
    out, _err = capsys.readouterr()
    assert "created instance of class Options" in out
    assert DMESSAGE in out
    assert VMESSAGE not in out


def test_options_xtra(capsys):
    """Test options xtra."""
    opts = Options()
    assert not opts.isnoop()
    assert not opts.isforce()


def test_options_scribe(capsys):
    """Test options with scribe."""
    opts = Options(basic_options(2, False, 2))
    opts.scribe = Scribe(screen=True)
    # opts.debug(DMESSAGE)
    opts.info(IMESSAGE)
    opts.warn(WMESSAGE)
    opts.error(EMESSAGE)
    opts.debug(DMESSAGE, 2)
    opts.verbose(VMESSAGE, 2)
    _out, err = capsys.readouterr()
    assert DMESSAGE not in err
    assert VMESSAGE in err
    assert IMESSAGE in err
    assert WMESSAGE in err
    assert IMESSAGE in err


def test_options_misc(capsys):
    """Test options with scribe."""
    opts = Options()
    opts.debug(DMESSAGE)
    opts.info(IMESSAGE)
    opts.warn(WMESSAGE)
    opts.error(EMESSAGE)
    out, _err = capsys.readouterr()
    # assert DMESSAGE not in out
    # assert VMESSAGE not in out
    assert WMESSAGE in out
    # assert IMESSAGE in out


def test_log_level_names():
    """Test log level names."""
    assert log_level_name(WARNING) == "warn"
    assert log_level_name(666) == "info"
    assert log_level_name(666, "debug") == "debug"
