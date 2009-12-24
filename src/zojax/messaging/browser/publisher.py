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
from zope import interface, component
from zope.location import LocationProxy
from zope.security.interfaces import Unauthorized
from zope.app.component.interfaces import ISite
from zope.publisher.interfaces import NotFound
from zope.publisher.interfaces.browser import IBrowserView
from z3c.traverser.interfaces import ITraverserPlugin

from zojax.messaging.interfaces import IMessageStorage


@interface.implementer(IBrowserView)
@component.adapter(ISite, interface.Interface)
def getMessageStorage(site, request):
    storage = IMessageStorage(request.principal, None)

    if storage is not None:
        return storage

    raise Unauthorized()


class TraverserPlugin(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        try:
            id = int(name)
        except:
            raise NotFound(self.context, name, request)

        try:
            message = self.context.getMessage(id)
        except:
            raise NotFound(self.context, name, request)

        return LocationProxy(message, self.context, message.__name__)
