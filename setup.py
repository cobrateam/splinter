# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from setuptools import setup, find_packages
import codecs


README = codecs.open("README.rst", encoding="utf-8").read()

setup(
    name="splinter",
    version="0.14.0",
    url="https://github.com/cobrateam/splinter",
    description="browser abstraction for web acceptance testing",
    long_description=README,
    author="CobraTeam",
    author_email="andrewsmedina@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ]
    + [("Programming Language :: Python :: %s" % x) for x in "2.7 3.6 3.7 3.8 3.9".split()],
    packages=find_packages(exclude=["docs", "tests", "samples"]),
    include_package_data=True,
    install_requires=["selenium>=3.141.0", "six"],
    extras_require={
        "zope.testbrowser": ["zope.testbrowser>=5.2.4", "lxml>=4.2.4", "cssselect"],
        "django": ["Django>=1.7.11", "lxml>=2.3.6", "cssselect", "six"],
        "flask": ["Flask>=1.0.2", "lxml>=2.3.6", "cssselect"],
    },
    tests_require=["coverage", "flask"],
)
