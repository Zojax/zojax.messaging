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
from BTrees.Length import Length
from BTrees.OIBTree import OIBTree

from zope import interface
from zope.location import Location
from zope.component import getUtility

from interfaces import IMessageService, IMessageServiceFactory


class MessageService(Persistent, Location):
    interface.implements(IMessageService)

    def __init__(self, storage):
        self.__parent__ = storage

        self.index = OIBTree()
        self.unread = Length(0)

    def __len__(self):
        return len(self.index)

    def __iter__(self):
        return iter(self.index.values())

    def __contains__(self, key):
        msg = self.__parent__.getMessage(key)
        if msg is not None:
            return True
        else:
            return False

    def get(self, msgId, default=None):
        msg = self.__parent__.getMessage(msgId)
        if msg is not None:
            if msg.__date__ in self.index:
                return msg

        return default

    def append(self, message):
        message.__parent__ = self

        if self.__parent__.readStatus(message):
            self.unread.change(1)

        self.index[message.__date__] = message.__id__

    def remove(self, message):
        id = message.__date__

        if id in self.index:
            del self.index[id]

            if self.__parent__.readStatus(message) and self.unread() > 0:
                self.unread.change(-1)

    def create(self, **data):
        raise NotImplemented('create')
