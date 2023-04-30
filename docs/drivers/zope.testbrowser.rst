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


Usage
-----

To use the ``zope.testbrowser`` driver, all you need to do is pass the string ``zope.testbrowser`` when you create
the ``Browser`` instance:

.. code-block:: python

    from splinter import Browser
    browser = Browser('zope.testbrowser')

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.

API docs
--------

.. autoclass:: splinter.driver.zopetestbrowser.ZopeTestBrowser
   :members:
   :inherited-members:
   :exclude-members: execute_script, evaluate_script
