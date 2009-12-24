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
""" mail template

$Id$
"""
from email.Utils import formataddr

from zope import interface, component
from zope.component import queryUtility, getMultiAdapter

from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.security.management import queryInteraction
from zope.lifecycleevent.interfaces import IObjectCreatedEvent

from zojax.mail.interfaces import IMailAddress
from zojax.mailtemplate.interfaces import IMailTemplate

from zojax.formatter.utils import getFormatter

from zojax.messaging.interfaces import IMessage
from zojax.messaging.interfaces import IMessageService
from zojax.messaging.interfaces import IMessageCreatedEvent
from zojax.messaging.interfaces import IPortalMessagingPreference


class MessageTemplate(object):

    contentType = 'text/html'

    def update(self):
        super(MessageTemplate, self).update()

        context = self.context
        request = self.request

        formatter = getFormatter(request, 'fancyDatetime', 'medium')

        self.date = formatter.format(context.__date__)
        self.service = context.__parent__

        storage = self.service.__parent__
        self.url = '%s/%s/'%(absoluteURL(storage, request), context.__name__)

    @property
    def subject(self):
        msg = u'You have been received new message.'

        title = getattr(getSite(), 'title', u'')
        if title:
            return u'%s: %s'%(title, msg)
        else:
            return msg

    @property
    def messageId(self):
        return '<%s@zojax>'%self.context.__uid__


@component.adapter(IMessage, IMessageCreatedEvent)
def messageCreated(message, event):
    principal = event.storage.principal

    prefs = IPortalMessagingPreference(principal)
    if not prefs.notify:
        return

    email = IMailAddress(principal, None)
    if email:
        request = queryInteraction().participations[0]
        template = getMultiAdapter(
            (message, request), IMailTemplate, 'template-created')
        template.addHeader(u'To', formataddr((principal.title, email.address)))
        template.send((email.address,))
