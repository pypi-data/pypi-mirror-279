import unittest
from pydantic import BaseModel
from typing import List, Dict
from parameterized import parameterized

from crimson.templator import _format_insert_loop_many, _format_insert_loop_list


class TestFormatInsertLoop(unittest.TestCase):

    kwargs1 = {
        "name": "Amy",
        "age": "25",
        "address": "Erlangen",
    }

    kwargs2 = {
        "name": "Jone",
        "age": "13",
        "address": "London",
    }

    kwargs_list = [kwargs1, kwargs2]

    kwargs_many = {"name": ["Amy", "Jone"], "age": ["25", "13"], "address": ["Erlangen", "London"]}

    template = r"""{
    name : \\[name\\],
    age : \\[age\\],
    address : \\[address\\],
},"""
    expected_formatted_with_ends = """{
    name : Amy,
    age : 25,
    address : Erlangen,
},{
    name : Jone,
    age : 13,
    address : London,
},"""
    expected_formatted_without_ends = """    name : Amy,
    age : 25,
    address : Erlangen,
},{
    name : Jone,
    age : 13,
    address : London,"""

    def test_loop_kwargs_list(self):

        formatted = _format_insert_loop_many(template=self.template, kwargs_many=self.kwargs_many, cut_ends=True)

        self.assertEqual(formatted, self.expected_formatted_without_ends)

    def test_format_loop_list(self):
        # Action
        formatted = _format_insert_loop_list(template=self.template, kwargs_list=self.kwargs_list, cut_ends=True)

        # Assertion
        self.assertEqual(formatted, self.expected_formatted_without_ends)

    @parameterized.expand([
        (True, "expected_formatted_without_ends"),
        (False, "expected_formatted_with_ends"),
    ])
    def test_format_insert_loop_cut_ends(self, cut_ends, expected_attr):
        formatted = _format_insert_loop_list(
            template=self.template,
            kwargs_list=self.kwargs_list,
            cut_ends=cut_ends
        )

        expected = getattr(self, expected_attr)
        self.assertEqual(formatted, expected)


if __name__ == "__main__":
    unittest.main()
