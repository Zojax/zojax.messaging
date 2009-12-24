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
from zojax.layout.pagelet import BrowserPagelet
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.messaging.interfaces import _


class MessageView(BrowserPagelet):

    def update(self):
        request = self.request
        context = self.context
        storage = context.__parent__

        if 'form.remove' in request:
            storage.removeMessage(context.__id__)
            self.redirect('../')

            IStatusMessage(request).add(_(u'Message has been removed.'))
            return

        storage.clearReadStatus(context.__id__)

        super(MessageView, self).update()
