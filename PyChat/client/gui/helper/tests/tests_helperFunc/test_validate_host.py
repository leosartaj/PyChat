#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##

import unittest
from PyChat.client.gui.helper.helperFunc import validate_host

class TestValidateHost(unittest.TestCase):
    """
    tests the validate_host function in helperFunc module
    """
    def _checkList(self, func, list_str, val=True):
        """
        Iterates a list 
        and checks if when func is called
        it returns val or not
        """
        for item in list_str:
            self.assertEqual(func(item), val)

    def test_correct_host(self):
        correct = '127.0.0.1'
        self.assertEqual(validate_host(correct), True)

    def test_incorrect_len_host(self):
        inlen = ['127', '127.0', '127.0.', '127.0.0', '127.0.0.1.', '127.0.0.1.1']
        self._checkList(validate_host, inlen, False)

    def test_incorrect_format_host(self):
        informat = ['-127.0.0.1', '127.0.0.256', '127.-1.-1.1']
        self._checkList(validate_host, informat, False)
