.. Copyright 2013 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with phantomjs webdriver
    :keywords: splinter, python, tutorial, how to install, installation, phantomjs, selenium

+++++++++++++++++++
Phantomjs WebDriver
+++++++++++++++++++

.. module:: splinter.driver.webdriver.phantomjs

Phantomjs WebDriver is provided by Selenium 2.0. To use it, you need to install Selenium 2.0 via pip:

.. highlight:: bash

::

    $ [sudo] pip install selenium

It's important to note that you also need to have `Phantomjs <http://phantomjs.org/>`_ `installed <http://phantomjs.org/download.html>`_ in your machine.
Once you have it installed, there is nothing you have to do, just use it :)

Using Phantomjs WebDriver
-------------------------

To use the Phantomjs driver, all you need to do is pass the string ``phantomjs`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('phantomjs')

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.

API docs
--------

.. autoclass:: WebDriver
   :members:
   :inherited-members:
