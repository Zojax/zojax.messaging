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
from persistent import Persistent
from rwproperty import setproperty, getproperty

from zope import interface
from zope.location import Location

from utils import genUID
from interfaces import IMessage


class Message(Persistent, Location):
    """
    >>> message = Message(u'My message')
    >>> message.title
    u'My message'
    >>> message.__uid__
    '...'

    >>> message.__name__
    '0000'

    >>> message.__id__ = 1
    >>> message.__name__
    '0001'

    >>> message.__uid__ is not None
    True
    """
    interface.implements(IMessage)

    __id__ = 0
    __uid__ = None
    __date__ = None

    def __init__(self, title):
        self.title = title

        self.__uid__ = genUID()

    @property
    def __name__(self):
        return '%0.4d'%self.__id__

    @getproperty
    def __status__(self):
        return self.__parent__.__parent__.readStatus(self)

    @setproperty
    def __status__(self, value):
        if not value:
            self.__parent__.__parent__.clearReadStatus(self)
