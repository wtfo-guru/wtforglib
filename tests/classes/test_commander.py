"""Test module for wtforglib package."""

import platform
from datetime import datetime, timedelta
from typing import Tuple

from wtforglib.commander import Commander, FakedProcessResult


def test_date_command():
    """Test date command."""
    cmdr = Commander()
    args: Tuple[str, ...]
    if platform.system() == "Windows":
        args = (
            "powershell",
            "-noprofile",
            "[int](Get-Date -UFormat %s -Millisecond 0)",  # noqa: WPS323
        )
    else:
        args = ("date", "+%s")  # noqa: WPS323
    res = cmdr.run_command(args, always=True)  # noqa: WPS323
    # tstamp = datetime.now().timestamp()
    now = datetime.now()
    epoch = datetime(1970, 1, 1)
    tstamp = int((now - epoch) / timedelta(seconds=1))
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
