import unittest

from crimson.templator import (
    format_insert,
    format_indent,
)


class TestSafeGuard(unittest.TestCase):
    def test_no_safe_flag_insert(self):
        kwargs = {"arg1": None, "arg2": "It might be an integer."}
        template = r"What is arg1? Arg1 is \[arg1\]. It \[arg2\]"

        with self.assertRaises(Exception):
            format_insert(template, **kwargs, safe=False)

    def test_no_safe_flag_indent(self):
        kwargs = {"arg1": "I am in line1", "arg2": None}
        template = r"""
            \{arg1\}

            \{arg2\}
        """

        with self.assertRaises(Exception):
            format_indent(template, **kwargs, safe=False)

    def test_safe_flag_insert(self):
        kwargs = {"arg1": None, "arg2": "might be an integer."}
        template = r"What is arg1? Arg1 is \[arg1\]. It \[arg2\]"
        expected_formatted = "What is arg1? Arg1 is None. It might be an integer."

        formatted = format_insert(template, **kwargs, safe=True)

        self.assertEqual(expected_formatted, formatted)

    def test_safe_flag_indent(self):
        kwargs = {"arg1": "I am in line1", "arg2": None}
        template = r"""
    \{arg1\}

    \{arg2\}
"""
        expected_formatted = """
    I am in line1

    None
"""

        formatted = format_indent(template, **kwargs, safe=True)
        self.assertEqual(expected_formatted, formatted)


if __name__ == "__main__":
    unittest.main()
