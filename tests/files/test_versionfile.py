import os
import shutil
import tempfile

import pytest

from wtforglib.versionfile import version_file

GETTYSBURG_ADDRESS = """Four score and seven years ago our fathers brought forth on this
continent, a new nation, conceived in Liberty, and dedicated to the proposition
that all men are created equal.

Now we are engaged in a great civil war, testing whether that nation, or any nation
so conceived and so dedicated, can long endure. We are met on a great battle-field of
that war. We have come to dedicate a portion of that field, as a final resting place
for those who here gave their lives that that nation might live. It is altogether
fitting and proper that we should do this.

But, in a larger sense,
we can not dedicate -- we can not consecrate -- we can not hallow -- this ground.
The brave men, living and dead, who struggled here, have consecrated it, far above
our poor power to add or detract. The world will little note, nor long remember what
we say here, but it can never forget what they did here. It is for us the living,
rather, to be dedicated here to the unfinished work which they who fought here have
thus far so nobly advanced. It is rather for us to be here dedicated to the great
task remaining before us -- that from these honored dead we take increased devotion
to that cause for which they gave the last full measure of devotion -- that we here
highly resolve that these dead shall not have died in vain -- that this nation, under
God, shall have a new birth of freedom -- and that government of the people, by the
people, for the people, shall not perish from the earth.

Abraham Lincoln
November 19, 1863
"""

TRES = 3

# TODO: use pyfakefs to test logic


def test_version_file_copy_mode(tmp_path):
    """Test copy mode."""
    td, tnm = tempfile.mkstemp(suffix=".wtf", text=True)
    os.write(td, GETTYSBURG_ADDRESS.encode("utf-8"))
    os.close(td)
    for idx in range(1, 5):
        slot = "{0}.{1}".format(tnm, idx)
        test_result = version_file(tnm, "copy", TRES)
        assert os.path.isfile(tnm)
        if idx < 4:
            assert os.path.isfile(slot)
        else:
            assert not os.path.isfile(slot)
        assert test_result == 0
    for idx in range(4):
        if idx == 0:
            slot = tnm
        else:
            slot = "{0}.{1}".format(tnm, idx)
        if os.path.isfile(slot):
            os.unlink(slot)


def test_version_file_rename_mode():
    """Test rename mode."""
    td, tnm = tempfile.mkstemp(suffix=".wtf", text=True)
    os.write(td, GETTYSBURG_ADDRESS.encode("utf-8"))
    os.close(td)
    for idx in range(1, 4):
        slot = "{0}.{1}".format(tnm, idx)
        test_result = version_file(tnm, "rename", TRES)
        assert not os.path.isfile(tnm)
        if idx < 4:
            assert os.path.isfile(slot)
        assert test_result == 0
        with open(tnm, "w") as tfile:
            tfile.write(GETTYSBURG_ADDRESS)
    for idx in range(4):
        if idx == 0:
            slot = tnm
        else:
            slot = "{0}.{1}".format(tnm, idx)
        if os.path.isfile(slot):
            os.unlink(slot)


def test_version_file_missing():
    """Test version missing file."""
    tnm = tempfile.mkdtemp()
    missing = os.path.join(tnm, "missing.txt")
    version_file(missing, "copy", TRES)
    assert not os.path.isfile(missing)
    shutil.rmtree(tnm)


def test_version_file_numbered_ext():
    """Test version file with numbered extension."""
    tnm = tempfile.mkdtemp()
    numbered = os.path.join(tnm, "missing.txt.9")
    with open(numbered, "w") as nfile:
        nfile.write("wtf\n")
    with pytest.raises(ValueError):
        version_file(numbered, "copy", TRES)
    shutil.rmtree(tnm)
