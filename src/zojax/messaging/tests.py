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
import os
import unittest, doctest
from zope import interface, component
from zope.app.testing import setup
from zope.app.component.hooks import setHooks
from zope.security.interfaces import IPrincipal
from zope.annotation.interfaces import IAnnotations

from storage import MessageStorage
from interfaces import IMessageStorage


class PrincipalAnnotations(dict):
    interface.implements(IAnnotations)
    data = {}

    def __new__(class_, principal):
        try:
            annotations = class_.data[principal.id]
        except KeyError:
            annotations = dict.__new__(class_)
            class_.data[principal.id] = annotations
        return annotations

    def __init__(self, principal):
        pass


key = 'zojax.messaging'

@component.adapter(IPrincipal)
@interface.implementer(IMessageStorage)
def getMessageStorage(principal):
    annotations = IAnnotations(principal)

    storage = annotations.get(key)
    if not IMessageStorage.providedBy(storage):
        storage = MessageStorage(principal.id)
        annotations[key] = storage

    return storage


def setUp(test):
    setHooks()
    setup.setUpTraversal()
    setup.setUpSiteManagerLookup()
    site = setup.placefulSetUp(True)
    site.__name__ = u'portal'
    component.provideAdapter(
        PrincipalAnnotations, (IPrincipal,), IAnnotations)
    component.provideAdapter(getMessageStorage)

    setup.setUpTestAsModule(test, name='zojax.messaging.TESTS')


def tearDown(test):
    setup.placefulTearDown()
    setup.tearDownTestAsModule(test)


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.ru',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        doctest.DocTestSuite(
            'zojax.messaging.message',
            setUp=setUp, tearDown=tearDown,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
        ))
