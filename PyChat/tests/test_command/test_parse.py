import unittest
from PyChat import command as cmd

class Testparse(unittest.TestCase):
    """
    tests the parse function in command module
    """
    def setUp(self):
        self.prefix = 'c$'
        self.sep = '~~'

    def test_parse_correct_command(self):
        line = self.prefix + self.sep + 'do' + self.sep + 'dummy'
        comd, val = cmd.parse(line, self.prefix, self.sep)
        self.assertEqual(comd, 'do')
        self.assertEqual(val, 'dummy')

    def test_parse_command_without_prefix(self):
        line = 'do' + self.sep + 'dummy'
        comd, val = cmd.parse(line, self.prefix, self.sep)
        self.assertEqual(comd, None)
        self.assertEqual(val, line)

    def test_parse_command_without_sep(self):
        line = self.prefix + 'do' + 'dummy'
        comd, val = cmd.parse(line, self.prefix, self.sep)
        self.assertEqual(comd, None)
        self.assertEqual(val, line)
