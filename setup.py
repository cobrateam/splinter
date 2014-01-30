# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from setuptools import setup, find_packages
import codecs


README = codecs.open('README.rst', encoding='utf-8').read()

setup(
    name='splinter',
    version='0.5.5',
    description='browser abstraction for web acceptance testing',
    long_description=README,
    author='CobraTeam',
    author_email='andrewsmedina@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ] + [('Programming Language :: Python :: %s' % x) for x in '2.6 2.7 3.0 3.1 3.2 3.3'.split()],
    packages=find_packages(exclude=['docs', 'tests', 'samples']),
    include_package_data=True,
    install_requires=['selenium>=2.39.0'],
    extras_require={'zope.testbrowser': ['zope.testbrowser>=4.0.4',
                                         'lxml>=2.3.6', 'cssselect']},
    tests_require=['coverage', 'flask'],
)
