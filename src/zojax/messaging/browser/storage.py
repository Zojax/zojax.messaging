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
from zope.component import getUtilitiesFor
from zojax.statusmessage.interfaces import IStatusMessage

from zojax.messaging.interfaces import _


class StorageView(object):

    def getServices(self):
        context = self.context

        services = []
        for serviceId in context.getServiceIds():
            service = context.getService(serviceId)
            if service.index:
                services.append(
                    (service.priority, service.title, service))

        services.sort()
        return [service for p,t,service in services]

    def update(self):
        request = self.request
        context = self.context

        if 'form.remove' in request:
            ids = request.get('msgid', ())

            if not ids:
                IStatusMessage(request).add(_(u'Please select messages.'))
                return

            for msgid in ids:
                try:
                    msgid = int(msgid)
                except:
                    continue

                context.remove(msgid)

            IStatusMessage(request).add(_(u'Selected messages have been removed.'))
