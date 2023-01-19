from os import getegid, geteuid

import pytest

from wtforglib.fstats import set_owner_group_perms
from wtforglib.ugpw import get_user_groups, get_user_name

# mypy: disable_error_code = var-annotated


def test_set_owner_group_perms(tmp_path):
    """Test set_owner_group_perms."""
    tfp = tmp_path / "uno.txt"
    with open(tfp, "w") as tf:
        print("wtf?", file=tf)
        tf.close()
    assert set_owner_group_perms(tfp, None, None, "0666")
    assert set_owner_group_perms(tfp, None, None, "664")
    assert not set_owner_group_perms(tfp, None, None, "664")


def test_set_owner_group_perms_bad_mode(tmp_path):
    """Test set_owner_group_perms."""
    tfp = tmp_path / "dos.txt"
    with open(tfp, "w") as tf:
        print("wtf?", file=tf)
        tf.close()
    with pytest.raises(ValueError):
        set_owner_group_perms(tfp, None, None, "66")
    with pytest.raises(ValueError):
        set_owner_group_perms(tfp, None, None, "66667")
    with pytest.raises(ValueError):
        set_owner_group_perms(tfp, None, None, "966")


def test_set_owner_group_perms_effective(tmp_path):
    """Test set_owner_group_perms."""
    tfp = tmp_path / "tres.txt"
    with open(tfp, "w") as tf:
        print("wtf?", file=tf)
        tf.close()
    euid = geteuid()
    egid = getegid()
    assert set_owner_group_perms(tfp, euid, egid, "0666")
    assert set_owner_group_perms(tfp, euid, egid, "664")
    assert not set_owner_group_perms(tfp, euid, egid, "664")


def test_set_owner_group(tmp_path):
    """Test set_owner_group_perms."""
    tfp = tmp_path / "quatro.txt"
    with open(tfp, "w") as tf:
        print("wtf?", file=tf)
        tf.close()
    eusr = get_user_name(geteuid())
    groups = get_user_groups(eusr)
    assert groups
    assert set_owner_group_perms(tfp, eusr, groups[0], "0666")
    assert set_owner_group_perms(tfp, eusr, groups[0], "664")
    assert not set_owner_group_perms(tfp, eusr, groups[0], "664")
