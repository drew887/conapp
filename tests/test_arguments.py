import unittest

from argparse import Namespace
from conapp.arguments import validate_args, get_args


# NOTE: only part of arguments module is actually testable

class ValidateArgsTestCase(unittest.TestCase):
    def test_failure(self):
        self.assertEqual(
            validate_args(Namespace(command=None)),
            False
        )


class GetArgsTestCase(unittest.TestCase):
    def test_default_argument_list(self):
        expected = Namespace(command=None)
        result = get_args([])

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
