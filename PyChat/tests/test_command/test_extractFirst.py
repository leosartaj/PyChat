import unittest
from PyChat import command as cmd

class Test_extractFirst_addFirst(unittest.TestCase):
    """
    tests the extractFirst, addFirst function in command module
    """
    def setUp(self):
        self.sep = '~~'

    def test_extractFirst_with_sep(self):
        line = 'do' + self.sep + 'dummy'
        first, rem = cmd.extractFirst(line, self.sep)
        self.assertEqual(first, 'do')
        self.assertEqual(rem, 'dummy')

    def test_extractFirst_without_sep(self):
        line = 'do' + 'dummy'
        first, rem = cmd.extractFirst(line, self.sep)
        self.assertEqual(first, None)
        self.assertEqual(rem, line)

    def test_addFirst(self):
        line = 'do' + self.sep + 'dummy'
        add = 'first'
        result = cmd.addFirst(line, add, self.sep)
        self.assertTrue(result.startswith(add + self.sep))
