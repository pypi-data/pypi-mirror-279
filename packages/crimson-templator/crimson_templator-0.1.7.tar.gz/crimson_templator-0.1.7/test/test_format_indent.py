import pytest
from crimson.templator import format_indent


def test_no_safe_flag_indent():
    kwargs = {
        "arg1": """\
I want to write very long lines
1
2
3
even 4!\
"""
    }
    template = r"""
    \{arg1\}
"""
    expected_formatted = """
    I want to write very long lines
    1
    2
    3
    even 4!
"""

    formatted = format_indent(template, open=r"\{", close=r"\}", safe=True, **kwargs)

    assert expected_formatted == formatted


def test_one_line_only_one_indent():
    kwargs = {"arg1": "I am just a line."}
    template = r"""
    \{arg1\} Additional text with indent will cause an error.
"""

    with pytest.raises(Exception):
        format_indent(template, **kwargs, safe=True)
