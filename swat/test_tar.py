import unittest
from swat.tar import get_tar_cmd, TAR_CREATE_FLAGS


class TestGetTarCmd(unittest.TestCase):
    def test_string_flags(self):
        expected = "tar -c -v -z"
        self.assertEqual(expected, get_tar_cmd(flags=TAR_CREATE_FLAGS))

    def test_tuple_flags(self):
        expected = 'tar -f test'

        self.assertEqual(expected, get_tar_cmd(flags=[('f', 'test')]))

    def test_both_flags(self):
        expected = "tar -c -v -f test"

        self.assertEqual(expected, get_tar_cmd(flags=['c', 'v' , ('f', 'test')]))

if __name__ == '__main__':
    unittest.main()
