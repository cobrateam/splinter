.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Browser
    :keywords: splinter, python, tutorial, browser

+++++++
Browser
+++++++

To use Splinter, you must create a Browser instance:

.. highlight:: python

::

    from splinter import Browser
    browser = Browser()

Alternatively, you can use a context manager using the ``with`` statement:

.. highlight:: python

::

    from splinter import Browser
    with Browser() as b:
        # stuff using the browser

This will automatically close the browser before executing the code outside the ``with`` statement.

``Browser()`` takes the following names, each mapped to a different driver:

* :doc:`chrome </drivers/chrome>`
* :doc:`firefox </drivers/firefox>`
* :doc:`edge </drivers/edge>`
* :doc:`remote </drivers/remote>`
* :doc:`zope.testbrowser </drivers/zope.testbrowser>`
* :doc:`django </drivers/django>`
* :doc:`flask </drivers/flask>`

For example:

.. highlight:: python

::

    browser = Browser('chrome')

=============================
Navigating with Browser.visit
=============================

You can use the ``visit`` method to navigate to other pages:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')

The ``visit`` method takes only a single parameter - the ``url`` to be visited.

You can visit a site protected with basic HTTP authentication by providing the
username and password in the url.

::

    browser.visit('http://username:password@cobrateam.info/protected')

================
Managing Windows
================

You can manage multiple windows (such as popups) through the windows object:

.. highlight:: python

::

    browser.windows              # all open windows
    browser.windows[0]           # the first window
    browser.windows[window_name] # the window_name window
    browser.windows.current      # the current window
    browser.windows.current = browser.windows[3]  # set current window to window 3

    window = browser.windows[0]
    window.is_current            # boolean - whether window is current active window
    window.is_current = True     # set this window to be current window
    window.next                  # the next window
    window.prev                  # the previous window
    window.close()               # close this window
    window.close_others()        # close all windows except this one

This window management interface is not compatible with the undocumented interface
exposed in v0.6.0 and earlier.

=============
Reload a page
=============

You can reload a page using the ``reload`` method:

.. highlight:: python

::

    browser.reload()

============================
Navigate through the history
============================

You can move back and forward through your browsing history using the ``back`` and ``forward`` methods:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')
    browser.visit('https://splinter.readthedocs.io')
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

===========================
Changing Browser User-Agent
===========================

You can pass a User-Agent header on Browser instantiation.

.. highlight:: python

::

    b = Browser(user_agent="Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en)")
