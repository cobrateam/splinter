.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Firefox webdriver
    :keywords: splinter, python, tutorial, how to install, installation, firefox, selenium

+++++++++++++++++
Firefox WebDriver
+++++++++++++++++

.. module:: splinter.driver.webdriver.firefox

Firefox WebDriver is provided by Selenium 2.0. To use it, you need to install Selenium 2.0 via pip:

.. highlight:: bash

::

    $ [sudo] pip install selenium


It's important to note that you also need to have `Firefox <http://firefox.com>`_ and `geckodriver <https://github.com/mozilla/geckodriver/releases>`_ installed in your machine and available on `PATH` environment variable.
Once you have it installed, there is nothing you have to do, just use it :)

Using Firefox WebDriver
-----------------------

To use the Firefox driver, all you need to do is pass the string ``firefox`` when you create
the ``Browser`` instance:

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('firefox')

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.


Using headless option for Firefox
-----------------------------------

Starting with Firefox 55, we can run Firefox as a headless browser in Linux.

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('firefox', headless=True)


Using incognito option for Firefox
------------------------------------

We can run Firefox as a private browser.

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('firefox', incognito=True)


How to use a specific profile for Firefox
-----------------------------------------

You can specify a `Firefox profile <http://support.mozilla.com/en-US/kb/Profiles>`_ for using on ``Browser`` function
using the ``profile`` keyword (passing the name of the profile as a ``str`` instance):

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('firefox', profile='my_profile')

If you don't specify a profile, a new temporary profile will be created (and deleted when you ``close`` the browser).

How to use specific extensions for Firefox
------------------------------------------

An extension for firefox is a .xpi archive. To use an extension in Firefox webdriver profile you need to give the path of the extension, using the extensions keyword (passing the extensions as a ``list`` instance):

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('firefox', extensions=['extension1.xpi', 'extension2.xpi'])

If you give an extension, after you close the browser, the extension will be deleted from the profile, even if is not a temporary one.

How to use selenium capabilities for Firefox
--------------------------------------------

.. highlight:: python

::

    from splinter import Browser
    browser = Browser('firefox', capabilities={'acceptSslCerts': True})

You can pass any selenium `read-write DesiredCapabilities parameters <https://code.google.com/p/selenium/wiki/DesiredCapabilities#Read-write_capabilities>`_ for Firefox.


API docs
--------

.. autoclass:: WebDriver
   :members:
   :inherited-members:
