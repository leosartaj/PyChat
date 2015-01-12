import unittest
from PyChat import command as cmd

class Testcmd(unittest.TestCase):
    """
    tests the cmd and its derived functions in command module
    """
    def setUp(self):
        self.sep = cmd.SEPARATOR
        self.client_prefix = cmd.CLIENT_PREFIX
        self.server_prefix = cmd.SERVER_PREFIX

    def test_cmd(self):
        comd, val = 'do', 'dummy'
        sep, prefix = self.sep, self.client_prefix
        shouldbe = prefix + sep + comd + sep + val
        result = cmd.cmd(comd, val, self.client_prefix, self.sep)
        self.assertEqual(result, shouldbe)

    def test_servercmd(self):
        comd, val = 'do', 'dummy'
        sep, prefix = self.sep, self.client_prefix
        shouldbe = prefix + sep + comd + sep + val
        result = cmd.servercmd(comd, val)
        self.assertEqual(result, shouldbe)

    def test_clientcmd(self):
        comd, val = 'do', 'dummy'
        sep, prefix = self.sep, self.server_prefix
        shouldbe = prefix + sep + comd + sep + val
        result = cmd.clientcmd(comd, val)
        self.assertEqual(result, shouldbe)
