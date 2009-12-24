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
from zope import interface
from zope.viewlet.viewlet import ViewletBase

from zojax.messaging.interfaces import _
from zojax.messaging.interfaces import IMessageStorage


class Messaging(ViewletBase):

    weight = 20

    def isAvailable(self):
        return not self.manager.isAnonymous and self.storage is not None

    def update(self):
        self.storage = IMessageStorage(self.manager.principal, None)

    def render(self):
        manager = self.manager

        s = _(u'Messages')

        unread = self.storage.unread
        if unread:
            s = s + '(%s)'%unread

        return '<a href="%s/messaging/">%s</a>'%(manager.portal_url, s)
