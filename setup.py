# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from setuptools import setup, find_packages
import codecs


README = codecs.open('README.rst', encoding='utf-8').read()

setup(
    name='splinter',
    version='0.7.5',
    url='https://github.com/cobrateam/splinter',
    description='browser abstraction for web acceptance testing',
    long_description=README,
    author='CobraTeam',
    author_email='andrewsmedina@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ] + [('Programming Language :: Python :: %s' % x) for x in '2.6 2.7 3.3 3.4'.split()],
    packages=find_packages(exclude=['docs', 'tests', 'samples']),
    include_package_data=True,
    install_requires=['selenium>=2.53.6'],
    extras_require={'zope.testbrowser': ['zope.testbrowser>=4.0.4',
                                         'lxml>=2.3.6', 'cssselect'],
                    'django': ['Django>=1.7.11,<1.10.2', 'lxml>=2.3.6', 'cssselect', 'six'],
                    'flask': ['Flask>=0.10', 'lxml>=2.3.6', 'cssselect']},
    tests_require=['coverage', 'flask'],
)
