.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with zope.testbrowser
    :keywords: splinter, python, tutorial, how to install, installation, zope, testbrowser, zope.testbrowser

++++++++++++++++
zope.testbrowser
++++++++++++++++

.. module:: splinter.driver.zopetestbrowser

To use the ``zope.testbrowser`` driver, you need to install `zope.testbrowser <http://pypi.python.org/pypi/zope.testbrowser>`_, `lxml <https://pypi.python.org/pypi/lxml>`_ and `cssselect <http://pypi.python.org/pypi/cssselect>`_. You can install all of them in one step by running:

.. highlight:: bash

::

    $ pip install splinter[zope.testbrowser]

Using zope.testbrowser
----------------------

To use the ``zope.testbrowser`` driver, all you need to do is pass the string ``zope.testbrowser`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('zope.testbrowser')

By default ``zope.testbrowser`` respects any robots.txt preventing access to a lot of sites. If you want to circumvent
this you can call

.. highlight:: python

::

    browser = Browser('zope.testbrowser', ignore_robots=True)

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.

API docs
--------

.. autoclass:: ZopeTestBrowser
   :members:
   :inherited-members:
