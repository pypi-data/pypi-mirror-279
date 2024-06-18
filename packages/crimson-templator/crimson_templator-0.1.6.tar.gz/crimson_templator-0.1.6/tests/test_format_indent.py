import unittest

from crimson.templator import (
    format_indent,
)


class TestSafeGuard(unittest.TestCase):
    def test_no_safe_flag_indent(self):
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

        formatted = format_indent(template, **kwargs)

        self.assertAlmostEqual(expected_formatted, formatted)

    def test_one_line_only_one_indent(self):
        kwargs = {"arg1": "I am just a line."}
        template = r"""
    \{arg1\} Additional text with indent will cause an error.
"""

        with self.assertRaises(Exception):
            format_indent(template, **kwargs, safe=True)


if __name__ == "__main__":
    unittest.main()
