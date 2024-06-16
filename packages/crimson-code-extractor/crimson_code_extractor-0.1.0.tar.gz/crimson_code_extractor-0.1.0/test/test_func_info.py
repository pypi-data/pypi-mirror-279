import unittest
from typing import Dict, Tuple, Optional
import inspect
from crimson.code_extractor.func_info import (
    extract_return_type,
    extract_arg_info,
    extract_return_info,
)


class A:
    pass  # Placeholder class for demonstration


def example_func(
    arg1: int = 1, arg2: Dict[str, A] = {"hi": A()}
) -> Tuple[int, A, Optional[Dict[str, int]]]:
    more_line = 1
    another_out = A()
    complex_out = None
    return more_line, another_out, complex_out


source = inspect.getsource(example_func)


class TestClassName(unittest.TestCase):

    def test_extract_arg_info(self):
        expected = [
            {"name": "arg1", "type_hint": "int", "default": "1"},
            {"name": "arg2", "type_hint": "Dict[str, A]", "default": "{'hi': A()}"},
        ]

        actual = extract_arg_info(source)

        self.assertEqual(actual, expected)

    def test_extract_return_info(self):
        expected = [
            {"name": "more_line", "type_hint": "int"},
            {"name": "another_out", "type_hint": "A"},
            {"name": "complex_out", "type_hint": "Optional[Dict[str, int]]"},
        ]

        actual = extract_return_info(source)

        self.assertEqual(actual, expected)

    def test_extract_return_type(self):
        expected = "Tuple[int, A, Optional[Dict[str, int]]]"

        actual = extract_return_type(source)

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
