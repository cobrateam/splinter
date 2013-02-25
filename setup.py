# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from setuptools import setup, find_packages
import codecs


README = codecs.open('README.rst', encoding='utf-8').read()


setup(
    name='splinter',
    version='0.5.0',
    description='browser abstraction for web acceptance testing',
    long_description=README,
    author='CobraTeam',
    author_email='andrewsmedina@gmail.com',
    packages=find_packages(exclude=['docs', 'tests', 'samples']),
    include_package_data=True,
    install_requires=['selenium>=2.29.0'],
    extras_require={'zope.testbrowser': ['zope.testbrowser>=4.0.2',
                                        'lxml>=2.3.6', 'cssselect']},
    tests_require=['coverage', 'flask'],
)
