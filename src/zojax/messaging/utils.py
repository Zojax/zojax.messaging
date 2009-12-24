##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import random

# - remove '1', 'l', and 'I' to avoid confusion
# - remove '0', 'O', and 'Q' to avoid confusion
# - remove vowels to avoid spelling words
invalid_chars = ['a','e','i','o','u','y','l','q']

def getValidChars():
    valid_chars = []
    for i in range(0, 26):
        if chr(ord('a')+i) not in invalid_chars:
            valid_chars.append(chr(ord('a')+i))
            valid_chars.append(chr(ord('A')+i))
    for i in range(2, 10):
        valid_chars.append(chr(ord('0')+i))
    return valid_chars

valid_chars = getValidChars()


def genUID(length=10):
    uid = ''
    nchars = len(valid_chars)
    for i in range(0, length):
        uid += valid_chars[random.randint(0,nchars-1)]

    return uid
