"""Test module for wtforglib package."""

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
"""  # noqa: WPS323

TEST_RESULT = """8.8.8.8           primary.google.com
2001:4860:4860:0:0:0:0:8888 primary.google.com
8.8.4.4           secondary.google.com
2001:4860:4860:0:0:0:0:8844 secondary.google.com

"""


def test_template_writer(tmpdir, fs):
    """Test template writer."""
    tmpl_path = tmpdir / "jinja_test.j2"
    out_path = tmpdir / "jinja_test.txt"
    fs.create_file(tmpl_path, contents=(TEST_JINJA))
    tmpl_info = {
        "dest": str(out_path),
        "src": str(tmpl_path),
    }
    tmpl_var = {
        "result": [
            ["8.8.8.8", "primary.google.com"],
            ["2001:4860:4860:0:0:0:0:8888", "primary.google.com"],
            ["8.8.4.4", "secondary.google.com"],
            ["2001:4860:4860:0:0:0:0:8844", "secondary.google.com"],
        ],
    }
    writer = TemplateWriter({"test": True})
    writer.generate("test_template", tmpl_info, tmpl_var)
    assert out_path.isfile()
    with open(out_path, "r") as iif:
        compare(iif.read(), TEST_RESULT)


def test_template_writer_dest_exists(tmpdir, fs):
    """Test template writer."""
    tmpl_path = tmpdir / "jinja_test.j2"
    out_path = tmpdir / "jinja_test.txt"
    fs.create_file(out_path, contents=(TEST_RESULT))
    fs.create_file(tmpl_path, contents=(TEST_JINJA))
    tmpl_info = {
        "dest": str(out_path),
        "src": str(tmpl_path),
    }
    tmpl_var = {
        "result": [
            ["8.8.8.8", "primary.google.com"],
            ["2001:4860:4860:0:0:0:0:8888", "primary.google.com"],
            ["8.8.4.4", "secondary.google.com"],
            ["2001:4860:4860:0:0:0:0:8844", "secondary.google.com"],
        ],
    }
    writer = TemplateWriter({"test": True})
    writer.generate("test_template", tmpl_info, tmpl_var)
    assert out_path.isfile()
    with open(out_path, "r") as iif:
        compare(iif.read(), TEST_RESULT)
