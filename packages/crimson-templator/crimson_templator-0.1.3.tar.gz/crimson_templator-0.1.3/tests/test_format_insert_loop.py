import unittest
from pydantic import BaseModel
from typing import List, Dict

from crimson.templator import format_insert_loop_many, format_insert_loop_list
from crimson.templator.utils import (
    convert_list_to_dicts_list,
)


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
    expected_formatted = """{
    name : Amy,
    age : 25,
    address : Erlangen,
},
{
    name : Jone,
    age : 13,
    address : London,
},"""

    def test_loop_kwargs_list(self):

        formatted = format_insert_loop_many(template=self.template, kwargs_many=self.kwargs_many)

        self.assertEqual(formatted, self.expected_formatted)

    def test_format_loop_list(self):
        # Action
        formatted = format_insert_loop_list(template=self.template, kwargs_list=self.kwargs_list)
        print(formatted)

        # Assertion
        self.assertEqual(formatted, self.expected_formatted)


if __name__ == "__main__":
    unittest.main()
