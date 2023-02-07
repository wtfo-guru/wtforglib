"""Test module for wtforglib package."""
from wtforglib.options import Options, basic_options

# mypy: disable_error_code = var-annotated

DMESSSAGE = "debug trace message"
VMESSAGE = "verbose trace message"


def test_options_default(capsys):
    """Test screen logger."""
    opts = Options()
    assert not opts.isdebug()
    assert not opts.istest()
    assert not opts.isverbose()
    opts.debug(DMESSSAGE)
    opts.verbose(VMESSAGE)
    out, _err = capsys.readouterr()
    assert DMESSSAGE not in out
    assert VMESSAGE not in out


def test_options_set(capsys):
    """Test screen logger."""
    opts = Options(basic_options(True, True, True))
    assert opts.isdebug()
    assert opts.istest()
    assert opts.isverbose()
    opts.debug(DMESSSAGE)
    opts.verbose(VMESSAGE)
    out, _err = capsys.readouterr()
    assert DMESSSAGE in out
    assert VMESSAGE in out


def test_options_level(capsys):
    """Test screen logger."""
    opts = Options(basic_options(2, False, 1))
    assert opts.isdebug()
    assert opts.isverbose()
    opts.debug(DMESSSAGE, 2)
    opts.verbose(VMESSAGE, 2)
    out, _err = capsys.readouterr()
    assert "created instance of class Options" in out
    assert DMESSSAGE in out
    assert VMESSAGE not in out
