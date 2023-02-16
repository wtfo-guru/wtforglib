"""Test module for wtforglib package."""

from datetime import datetime

from wtforglib.commander import Commander, FakedProcessResult


def test_date_command():
    """Test date command."""
    cmdr = Commander()
    res = cmdr.run_command(("date", "+%s"), always=True)  # noqa: WPS323
    tstamp = datetime.now().timestamp()
    assert res.returncode == 0
    assert tstamp - int(res.stdout.strip()) <= 1


def test_fake_result():
    """Test fake result."""
    res = FakedProcessResult("stdout", "stderr", 3)
    assert res.stdout.strip() == "stdout"
    assert res.stderr.strip() == "stderr"
    assert res.returncode == 3


def test_noex(capsys):
    """Test date command."""
    cmdr = Commander({"noop": True})
    res = cmdr.run_command(("date", "+%s"), check=True)  # noqa: WPS323
    assert res.returncode == 0
    out, _err = capsys.readouterr()
    assert "noex: date +%s" in out  # noqa: WPS323
