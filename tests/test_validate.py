import unittest

from subprocess import CompletedProcess
from conapp.validate import validate_subprocess


class ValidateSubprocessTestCase(unittest.TestCase):
    def test_validates_true(self):
        proc = CompletedProcess(['d'], returncode=0)
        result = validate_subprocess(proc)
        self.assertEqual(result, True)

    def test_raise_sys_exit(self):
        return_code = 15
        proc = CompletedProcess(['bla'], returncode=return_code)

        with self.assertRaises(SystemExit) as exception:
            validate_subprocess(proc)

        self.assertEqual(exception.exception.code, return_code)


if __name__ == '__main__':
    unittest.main()
