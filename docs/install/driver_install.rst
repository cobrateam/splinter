.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Chrome WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, chrome, selenium

+++++++++++++++
Install Drivers
+++++++++++++++
.. _install-drivers:

The various Drivers which are supported by splinter must be installed separately.

Install Using Extra Arguments
=============================

When splinter is installed via pip, extra arguments can be provided.
These will automatically install the latest version of the desired driver.

The following are the valid extra arguments

- selenium
- django
- flask
- zope.testbrowser

Example
-------

To install splinter with selenium included automatically:

.. code-block:: bash

    pip install splinter[selenium]


Selenium
========

To use ``chrome``, ``fireFox``, ``edge``, or ``remote``, the
`python bindings for Selenium <https://pypi.org/project/selenium/>`_ must be installed.

Django
======

To use the ``django``, the following must be installed:

- `django <http://pypi.python.org/pypi/django>`_
- `lxml <https://pypi.python.org/pypi/lxml>`_
- `cssselect <http://pypi.python.org/pypi/cssselect>`_

Flask
=====

To use the ``flask`` driver, the following must be installed:

- `Flask <https://pypi.python.org/pypi/Flask>`_
- `lxml <https://pypi.python.org/pypi/lxml>`_
- `cssselect <http://pypi.python.org/pypi/cssselect>`_

zope.testbrowser
================

To use the ``zope.testbrowser``, the following must be installed:

- `zope.testbrowser <http://pypi.python.org/pypi/zope.testbrowser>`_
- `lxml <https://pypi.python.org/pypi/lxml>`_
- `cssselect <http://pypi.python.org/pypi/cssselect>`_
