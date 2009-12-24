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
""" custom IBreadcrumb implementation for IMessageStorage

$Id$
"""
from zope import interface, component
from z3c.breadcrumb.browser import GenericBreadcrumb
from zojax.messaging.interfaces import _, IMessageStorage


class MessagesBreadcrumb(GenericBreadcrumb):
    component.adapts(IMessageStorage, interface.Interface)

    name = _(u'My messages')
