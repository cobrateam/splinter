# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os

from setuptools import setup, find_packages


def read(filename: str) -> str:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r') as f:
        return f.read()


def get_version_data() -> dict:
    data = {}

    path = os.path.join(os.path.dirname(__file__), 'splinter', 'version.py')

    with open(path) as fp:
        exec(fp.read(), data)

    return data


version_data = get_version_data()


setup(
    name="splinter",
    version=version_data['__version__'],
    url="https://github.com/cobrateam/splinter",
    description="browser abstraction for web acceptance testing",
    long_description=read('README.rst'),
    author="CobraTeam",
    author_email="andrewsmedina@gmail.com",
    license="BSD",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
    ]
    + [("Programming Language :: Python :: %s" % x) for x in "3.7 3.8 3.9 3.10 3.11".split()],
    project_urls={
        "Documentation": "https://splinter.readthedocs.io/",
        "Changelog": "https://github.com/cobrateam/splinter/tree/master/docs/news",
        "Source": "https://github.com/cobrateam/splinter/",
        "Tracker": "https://github.com/cobrateam/splinter/issues",
    },
    packages=find_packages(exclude=["docs", "tests", "samples"]),
    include_package_data=True,
    install_requires=[
        "urllib3 >=1.26.14,<2.0"
    ],
    extras_require={
        "zope.testbrowser": ["zope.testbrowser>=5.5.1", "lxml>=4.2.4", "cssselect"],
        "django": ["Django>=2.0.6", "lxml>=4.2.4", "cssselect"],
        "flask": ["Flask>=2.0.2", "lxml>=4.2.4", "cssselect"],
        "selenium": ["selenium>=4.1.0,<4.8.0"],
    },
    tests_require=["coverage", "flask"],
)
