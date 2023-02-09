import os
import shutil
import tempfile

import pytest

from wtforglib.errors import raise_filenotfound_if


def test_version_file_missing():
    """Test version missing file."""
    tnm = tempfile.mkdtemp()
    missing = os.path.join(tnm, "missing.txt")
    with pytest.raises(FileNotFoundError):
        raise_filenotfound_if(missing)
    shutil.rmtree(tnm)


def test_version_file_numbered_ext():
    """Test version file with numbered extension."""
    tnm = tempfile.mkdtemp()
    found = os.path.join(tnm, "not-missing.txt")
    with open(found, "w") as nfile:
        nfile.write("wtf\n")
    try:
        raise_filenotfound_if(found)
    except FileNotFoundError:
        pytest.fail("raise_filenotfound_if({0})".format(str(found)))
    shutil.rmtree(tnm)
