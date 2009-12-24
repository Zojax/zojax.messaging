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
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from zope.component.interfaces import IObjectEvent, ObjectEvent
from zojax.preferences.interfaces import IPreferenceCategory

_ = MessageFactory('zojax.messaging')


class IMessage(interface.Interface):

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Message title.'),
        required = True)

    __id__ = interface.Attribute('ID')

    __uid__ = interface.Attribute('Unique ID')

    __date__ = interface.Attribute('Date')

    __parent__ = interface.Attribute('Parent')

    __status__ = interface.Attribute('Status')

    service = interface.Attribute('IMessageService object')


class IMessageStorage(interface.Interface):
    """ message storage """

    index = interface.Attribute('Index')

    unread = interface.Attribute('Unread count')

    messages = interface.Attribute('Messages')

    principal = interface.Attribute('Principal')

    def getMessage(messageId):
        """ message id """

    def getService(serviceId):
        """ return service messages """

    def getServiceIds():
        """ return service ids """

    def create(service, **data):
        """ create and append message to storage """

    def remove(messageId):
        """ remove message """

    def readStatus(message):
        """ return message read status """

    def clearReadStatus(message):
        """ set message status as read """


class IMessageService(interface.Interface):
    """ message service for principal """

    title = schema.TextLine(
        title = u'Title',
        required = True)

    description = schema.Text(
        title = u'Description',
        required = False)

    priority = schema.Int(
        title = u'Priority',
        default = 9999,
        required = True)

    index = interface.Attribute('Date index')

    unread = interface.Attribute('Unread count')

    def __len__():
        """ """

    def __iter__():
        """ """

    def get(msgId, default=None):
        """ """

    def create(**data):
        """ create message """

    def append(message):
        """ append message """

    def remove(message):
        """ remove message """


class IMessageServiceFactory(interface.Interface):
    """ message service factory """

    def __call__(*args, **kw):
        """ create message service """


class IPortalMessagingPreference(interface.Interface):
    """ Preferences related to portal messaging """

    notify = schema.Bool(
        title = _(u'Notification'),
        description = _(u'Send me an email notification if message is received.'),
        default = True,
        required = True)


class IMessageCreatedEvent(IObjectEvent):
    """ The message has been created. """

    storage = interface.Attribute('IMessageStorage object')


class IMessageRemovedEvent(IObjectEvent):
    """ The message has been removed. """

    storage = interface.Attribute('IMessageStorage object')


class MessageCreatedEvent(ObjectEvent):
    interface.implements(IMessageCreatedEvent)

    def __init__(self, object, storage):
        self.object = object
        self.storage = storage


class MessageRemovedEvent(ObjectEvent):
    interface.implements(IMessageRemovedEvent)

    def __init__(self, object, storage):
        self.object = object
        self.storage = storage


class IServiceView(interface.Interface):
    """ service view type """


class IMessageMailView(interface.Interface):
    """ mail view for message """
