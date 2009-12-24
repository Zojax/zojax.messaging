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
""" Setup for zojax.messaging package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='1.0.5dev'


setup(name = 'zojax.messaging',
      version = version,
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      description = "Messaging service for zojax.",
      long_description = (
          'Detailed Documentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax'],
      install_requires = ['setuptools', 'pytz', 'rwproperty',
                          'ZODB3',
                          'zope.event',
                          'zope.schema',
                          'zope.component',
                          'zope.interface',
                          'zope.publisher',
                          'zope.location',
                          'zope.security',
                          'zope.annotation',
                          'zope.traversing',
                          'zope.i18nmessageid',
                          'zope.lifecycleevent',
                          'zope.cachedescriptors',
                          'zope.app.security',
                          'zope.app.component',

                          'z3c.traverser',
                          'z3c.breadcrumb',

                          'zojax.layout',
                          'zojax.layoutform',
                          'zojax.preferences',
                          'zojax.controlpanel',
                          'zojax.mail',
                          'zojax.mailtemplate',
                          'zojax.formatter',
                          'zojax.statusmessage',
                          ],
      extras_require = dict(test=['zope.app.zcmlfiles',
                                  'zope.app.testing',
                                  'zope.testing',
                                  'zope.testbrowser',
                                  'zope.securitypolicy',
                                  'zojax.personal.messages',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
