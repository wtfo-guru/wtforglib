"""Test module for wtforglib package."""

import filecmp

from wtforglib.tmplwrtr import TemplateWriter

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
    anchor_path = tmpdir / "anchor.txt"
    fs.create_file(tmpl_path, contents=(TEST_JINJA))
    fs.create_file(anchor_path, contents=(TEST_RESULT))
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
    writer = TemplateWriter()
    writer.generate("test_template", tmpl_info, tmpl_var)
    assert out_path.isfile()
    assert anchor_path.isfile()
    assert filecmp.cmp(out_path, anchor_path)
