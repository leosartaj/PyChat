#!/usr/bin/env python2

##
# PyChat
# https://github.com/leosartaj/PyChat.git
#
# Copyright (c) 2014 Sartaj Singh
# Licensed under the MIT license.
##


"""
Upper key and lower key functionality
when pressed gives last written text
"""

class stack:
    """
    Makes a stack
    that can be cycled
    up and down
    """
    def __init__(self, textList=[]):
        self.textList = textList
        self.reset_point()

    def reset_point(self):
        """
        Sets the pointer to the end of the list
        """
        self.point = len(self.textList)

    def push(self, text):
        """
        Push new text in stack
        """
        textList = self.textList
        textList.append(text)
        self.reset_point()
        return textList # only for testing purposes

    def pop(self):
        """
        Returns the previous text in textList
        """
        if self.point > 0:
            text = self.textList[self.point - 1]
            self.point -= 1
            return text
        return None

    def up(self):
        """
        Cycles up the stack
        returns the text if possible
        returns None if already at top
        """
        if self.point + 1 < len(self.textList):
            self.point += 1
            text = self.textList[self.point]
            return text
        return None
