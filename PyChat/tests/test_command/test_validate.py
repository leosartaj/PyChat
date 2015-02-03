#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

import unittest
from PyChat import command as cmd

class Testvalidate(unittest.TestCase):
    """
    tests the validate function in command module
    """
    def setUp(self):
        self.prefix = 'c$'

    def test_correct_string(self):
        dummy = self.prefix + '~dummy'
        self.assertTrue(cmd.validate(dummy, self.prefix))

    def test_incorrect_string(self):
        dummy = 's$~dummy'
        self.assertFalse(cmd.validate(dummy, self.prefix))
