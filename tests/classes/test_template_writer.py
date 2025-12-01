"""Test module for wtforglib package."""

import sys
from pathlib import Path

import pytest
from jinja2 import Environment
from testfixtures import compare  # type: ignore

from wtforglib.tmplwrtr import TemplateWriter

TEXT = """Four score and seven years ago our fathers brought forth, upon this
continent, a new nation, conceived in liberty, and dedicated to the
proposition that all men are created equal. Now we are engaged in a
great civil war, testing whether that nation, or any nation so
conceived, and so dedicated, can long endure.
"""

TEST_JINJA = """{% if 'result' in template_dict -%}
{% for entry in template_dict["result"] -%}
{{ "%-17s" | format(entry[0]) }} {{ entry[1] }}
{% endfor %}
{% endif %}
"""

TEST_RESULT = """8.8.8.8           primary.google.com
2001:4860:4860:0:0:0:0:8888 primary.google.com
8.8.4.4           secondary.google.com
2001:4860:4860:0:0:0:0:8844 secondary.google.com

"""

TEMPLATE_VAR = {
    "result": [
        ["8.8.8.8", "primary.google.com"],
        ["2001:4860:4860:0:0:0:0:8888", "primary.google.com"],
        ["8.8.4.4", "secondary.google.com"],
        ["2001:4860:4860:0:0:0:0:8844", "secondary.google.com"],
    ],
}

TEMPLATE_NAME = "test_template"
K_DEST = "dest"
KSRC = "src"
TEMPLATE_DICT = {
    "whitelist": [
        "101.87.124.17/32",
        "101.89.83.33/32",
        "[2605:aaaa:6208:bbbb::]/64",
    ],
}


def test_template_writer(tmpdir, fs):
    """Test template writer."""
    tmpl_path = tmpdir / "jinja_test.j2"
    # out_path: Path = Path(tmp_path / "jinja_test.txt")
    out_path = tmpdir / "jinja_test.txt"
    fs.create_file(tmpl_path, contents=(TEST_JINJA))
    assert tmpl_path.isfile()
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    assert out_path.isfile()
    with open(out_path, "r") as iif:
        compare(iif.read(), TEST_RESULT)


def test_template_writer_dest_exists(tmpdir, fs):
    """Test template writer."""
    tmpl_path = tmpdir / "jinja_test.j2"
    out_path = tmpdir / "jinja_test.txt"
    fs.create_file(tmpl_path, contents=(TEST_JINJA))
    fs.create_file(out_path, contents=(TEST_RESULT))
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    assert out_path.isfile()
    with open(out_path, "r") as iif:
        compare(iif.read(), TEST_RESULT)


def test_template_writer_src_missing(tmpdir, capsys):
    """Test template writer."""
    tmpl_path = tmpdir / "tw_missing_src.j2"
    out_path = tmpdir / "tw_missing_src.txt"
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    out, err = capsys.readouterr()
    assert "ERROR: Template src '{0}' not found!!".format(str(tmpl_path)) in err


def test_template_writer_src_not_file(tmpdir, fs, capsys):
    """Test template writer."""
    tmpl_path = tmpdir / "tw_dir_src.j2"
    out_path = tmpdir / "tw_dir_src.txt"
    fs.create_dir(tmpl_path)
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    out, err = capsys.readouterr()
    assert "ERROR: Template src '{0}' not a file!!".format(str(tmpl_path)) in err


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Windows file permissions frustrating.",
)
def test_template_writer_src_not_readable(tmpdir, fs, capsys):
    """Test template writer."""
    tmpl_path = tmpdir / "tw_dir_src.j2"
    out_path = tmpdir / "tw_dir_src.txt"
    fs.create_file(tmpl_path)
    tmpl_path.chmod(0o333)
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    out, err = capsys.readouterr()
    assert "ERROR: Template src '{0}' not readable!!".format(str(tmpl_path)) in err


def test_template_writer_tgt_dir_not_dir(tmpdir, fs, capsys):
    """Test template writer."""
    tmpl_path = tmpdir / "tw_dir_src.j2"
    out_parent = tmpdir / "output"
    fs.create_file(tmpl_path)
    fs.create_file(out_parent)
    out_path = out_parent / "tw_dir_src.txt"
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    out, err = capsys.readouterr()
    assert "ERROR: '{0}' is not a directory".format(str(out_parent)) in err


def test_template_writer_tgt_not_file(tmpdir, fs, capsys):
    """Test template writer."""
    tmpl_path = tmpdir / "tw_dir_dest.j2"
    out_path = tmpdir / "tw_dir_dest.txt"
    fs.create_file(tmpl_path)
    fs.create_dir(out_path)
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    out, err = capsys.readouterr()
    assert "ERROR: Template dest '{0}' not a file!!".format(str(out_path)) in err


def test_template_writer_tgt_not_writable(tmpdir, fs, capsys):
    """Test template writer."""
    tmpl_path = tmpdir / "tw_not_write_dest.j2"
    out_path = tmpdir / "tw_not_write_dest.txt"
    fs.create_file(tmpl_path)
    fs.create_file(out_path)
    out_path.chmod(0o444)
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(tmpl_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    out, err = capsys.readouterr()
    assert "ERROR: Template dest '{0}' not writable!!".format(str(out_path)) in err


def test_template_writer_bad_info(tmpdir, capsys):
    """Test template writer."""
    out_path = tmpdir / "badinfo_test.txt"
    tmpl_info = {
        K_DEST: str(out_path),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_VAR)
    out, err = capsys.readouterr()
    assert (
        "ERROR: Template {0} does not have a {1} key!!".format(TEMPLATE_NAME, KSRC)
        in err
    )


def test_template_writer_default_env(tmpdir, capsys):
    """Test template writer."""
    out_path = tmpdir / "mynetworks.txt"
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(
            Path(__file__).parent.parent.resolve() / "data" / "postfix-mynetworks.j2"
        ),
    }
    writer = TemplateWriter({"test": True})
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_DICT)
    out, err = capsys.readouterr()
    with open(out_path, "r") as iif:
        rendered = iif.read()
        reversed = rendered[::-1]  # noqa: WPS478
        lines_at_end = 0
        for char in reversed:
            if char == "\n":
                lines_at_end += 1
            else:
                break
        assert lines_at_end == 0


def test_template_writer_custom_env(tmpdir, capsys):
    """Test template writer."""
    out_path = tmpdir / "mynetworks.txt"
    tmpl_info = {
        K_DEST: str(out_path),
        KSRC: str(
            Path(__file__).parent.parent.resolve() / "data" / "postfix-mynetworks.j2"
        ),
    }
    writer = TemplateWriter({"test": True}, Environment(keep_trailing_newline=True))
    writer.generate(TEMPLATE_NAME, tmpl_info, TEMPLATE_DICT)
    out, err = capsys.readouterr()
    with open(out_path, "r") as iif:
        rendered = iif.read()
        reversed = rendered[::-1]  # noqa: WPS478
        lines_at_end = 0
        for char in reversed:
            if char == "\n":
                lines_at_end += 1
            else:
                break
        assert lines_at_end == 1
