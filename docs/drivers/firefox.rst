.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Firefox WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, firefox, selenium

+++++++++++++++++
Firefox WebDriver
+++++++++++++++++

External Requirements
=====================

The following applications are required:

  - `Mozilla Firefox <http://firefox.com>`_
  - `Geckodriver <https://github.com/mozilla/geckodriver/releases>`_

Geckodriver must also be available on your operating system's `PATH` environment variable.

Dependencies
++++++++++++

To use Firefox, the python bindings for Selenium 3 or Selenium 4 must be installed.

When splinter is installed via pip, the `selenium3` or `selenium4` extra argument can be provided.
This will automatically install the latest version of Selenium 3 or Selenium 4, respectively.


.. code-block:: bash

    python -m pip install splinter[selenium3]

Installing Geckodriver
======================

Mac OS X
++++++++

The recommended way is by using `Homebrew <http://mxcl.github.com/homebrew/>`_:

.. code-block:: console

    brew install geckodriver

Usage
-----

To use the Firefox driver, pass the string ``firefox`` when you create
the ``Browser`` instance:

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox')

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.

Headless mode
+++++++++++++

Starting with Firefox 55, Firefox can run in a headless mode.

To use headless mode, pass the `headless` argument
when creating a new Browser instance.

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox', headless=True)

Incognito mode
++++++++++++++

To use Firefox's incognito mode, pass the `incognito` argument
when creating a Browser instance.

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox', incognito=True)

Specify Profile
+++++++++++++++

You can specify a `Firefox profile <http://support.mozilla.com/en-US/kb/Profiles>`_ for using on ``Browser`` function
using the ``profile`` keyword (passing the name of the profile as a ``str`` instance):

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox', profile='my_profile')

If you don't specify a profile, a new temporary profile will be created (and deleted when you ``close`` the browser).

Firefox Extensions
++++++++++++++++++

An extension for firefox is a .xpi archive.
To use an extension in Firefox webdriver profile you need to give the path of
the extension, using the extensions keyword (passing the extensions as a ``list`` instance):

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox', extensions=['extension1.xpi', 'extension2.xpi'])

After the browser is closed, extensions will be deleted from the profile, even if the profile is not a temporary one.

Selenium Capabilities
+++++++++++++++++++++

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox', capabilities={'acceptSslCerts': True})

You can pass any selenium `read-write DesiredCapabilities parameters <https://code.google.com/p/selenium/wiki/DesiredCapabilities#Read-write_capabilities>`_ for Firefox.


API docs
--------

.. autoclass:: splinter.driver.webdriver.firefox.WebDriver
   :members:
   :inherited-members:
