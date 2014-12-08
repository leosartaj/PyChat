#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

import unittest
import os
from PyChat.client.gui.helper.helperFunc import find_file

class TestfindFile(unittest.TestCase):
    """
    tests the find_file function in helperFunc module
    """
    def setUp(self):
        self.test_file = 'test_file'
        with open(self.test_file, 'w'): # create test file
            pass

    def test_check_file(self):
        path = find_file('.', self.test_file)
        self.assertEqual(os.path.isfile(path), True)

    def tearDown(self):
        os.remove(self.test_file)

