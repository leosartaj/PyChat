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
from PyChat.client.gui.helper.stack import stack

class TestStack(unittest.TestCase):
    """
    tests the stack class in stack module
    """
    def setUp(self):
        self.empty_stack = stack()
        self.length = 10
        nums = [i for i in range(self.length)]
        self.stack = stack(nums)

    def test_point_empty_stack(self):
        point = self.empty_stack.point
        self.assertEqual(point, 0)

    def test_point_stack(self):
        point = self.stack.point
        self.assertEqual(point, self.length)

    def test_push_empty_stack(self):
        textList = self.empty_stack.push(self.length)
        self.assertEqual(textList, [self.length])

    def test_push_stack(self):
        textList = self.stack.push(self.length)
        for index, item in enumerate(textList):
            self.assertEqual(index, item)

    def test_up_empty_stack(self):
        self.assertEqual(self.empty_stack.up(), None)

    def test_up_stack(self):
        self.stack.point = -1 # put pointer at start
        for i in range(self.length):
            self.assertEqual(self.stack.up(), i)

    def test_pop_empty_stack(self):
        self.assertEqual(self.empty_stack.pop(), None)

    def test_pop_stack(self):
        for i in range(self.length - 1, -1, -1):
            self.assertEqual(self.stack.pop(), i)
