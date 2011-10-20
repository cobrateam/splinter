.. meta::
    :description: Browser
    :keywords: splinter, python, tutorial, browser, firefox, chrome, zope, testebrowser 

+++++++
Browser
+++++++

To use splinter you need create a Browser instance:

.. highlight:: python

::

    from splinter.browser import Browser
    browser = Browser()


splinter support three drivers: chrome, firefox and zopetestbrowser

.. highlight:: python

::

    browser = Browser('chrome')
    browser = Browser('firefox')
    browser = Browser('zope.testbrowser')

=============================
Navigating with Browser.visit
=============================

You can use the ``visit`` method to navigate to other pages:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')

The ``visit`` method takes only a single parameter - the ``url`` to be visited.

=============
Reload a page
=============

You can reload a page using ``reload`` method:

.. highlight:: python

::

    browser.reload()

============================
Navigate through the history
============================

You can back and forward on your browsing history using ``back`` and ``forward`` methods:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')
    browser.visit('http://splinter.cobrateam.info')
    browser.back()
    browser.forward()

=============
Browser.title
=============

You can get the title of the visited page using the ``title`` attribute:

.. highlight:: python

::

    browser.title

========================================
Verifying page content with Browser.html
========================================

You can use the ``html`` attribute to get the html content of the visited page:

.. highlight:: python

::

    browser.html

===================================
Verifying page url with Browser.url
===================================

The visited page's url can be accessed by the ``url`` attribute:

.. highlight:: python

::

    browser.url

