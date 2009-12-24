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
import pytz
from datetime import datetime, timedelta

from persistent import Persistent
from BTrees.Length import Length
from BTrees.IOBTree import IOBTree
from BTrees.OIBTree import OIBTree
from BTrees.OOBTree import OOBTree
from BTrees.IIBTree import IITreeSet

from zope import event, interface

from zope.location import Location
from zope.component import getUtility
from zope.cachedescriptors.property import Lazy
from zope.app.security.interfaces import IAuthentication

from interfaces import MessageCreatedEvent, MessageRemovedEvent
from interfaces import IMessageStorage, IMessageService, IMessageServiceFactory

timedelta = timedelta(microseconds=1)


class MessageStorage(Persistent, Location):
    interface.implements(IMessageStorage)

    notify = True
    principalId = None

    def __init__(self, principalId):
        self.index = OIBTree()
        self.messages = IOBTree()
        self.services = OOBTree()
        self.readstatus = IITreeSet()
        self.principalId = principalId

        self._next = Length(1)

    @Lazy
    def readstatus(self):
        self.readstatus = IITreeSet()
        return self.readstatus

    @property
    def principal(self):
        try:
            return getUtility(IAuthentication).getPrincipal(self.principalId)
        except:
            return None

    @property
    def unread(self):
        unread = 0
        for serviceId in self.services.keys():
            service = self.getService(serviceId)
            unread = unread + service.unread()
        return unread

    def getMessage(self, messageId):
        return self.messages.get(messageId)

    def getServiceIds(self):
        return list(self.services.keys())

    def getService(self, serviceId):
        service = self.services.get(serviceId)

        if not IMessageService.providedBy(service):
            factory = getUtility(IMessageServiceFactory, serviceId)
            service = factory(self)
            self.services[serviceId] = service

        return service

    def create(self, serviceId, **data):
        """ create and append message to storage """
        id = self._next()
        self._next.change(1)

        service = self.getService(serviceId)

        msg = service.create(**data)
        date = datetime.now(pytz.utc)

        while date in self.index:
            date = date + timedelta

        msg.__id__ = id
        msg.__date__ = date

        self.index[date] = id
        self.messages[id] = msg
        self.readstatus.insert(id)

        service.append(msg)

        event.notify(MessageCreatedEvent(msg, self))
        return id

    def remove(self, messageId):
        message = self.messages.get(messageId)

        if message is None:
            return
        else:
            self.clearReadStatus(message)

            del self.index[message.__date__]
            del self.messages[message.__id__]

            for serviceId in self.services.keys():
                service = self.getService(serviceId)
                service.remove(message)

            event.notify(MessageRemovedEvent(message, self))

    def readStatus(self, message):
        return message.__id__ in self.readstatus

    def clearReadStatus(self, message):
        if message.__id__ not in self.readstatus:
            return

        idx = message.__date__
        for serviceId in self.services.keys():
            service = self.getService(serviceId)
            if idx in service.index and service.unread() > 0:
                service.unread.change(-1)

        self.readstatus.remove(message.__id__)
