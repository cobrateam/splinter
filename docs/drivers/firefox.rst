.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Firefox WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, firefox, selenium

+++++++++++++++++
Firefox WebDriver
+++++++++++++++++


Usage
-----

To use the Firefox driver, pass the string ``firefox`` when you create
the ``Browser`` instance:

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox')

**Note:** if you don't provide any driver to ``Browser`` function, ``firefox`` will be used.


Service
+++++++

Selenium uses the Service class to manage geckodriver.
An instance of this class can be given directly to Splinter.

.. code-block:: python

    from splinter import Browser
    from selenium.webdriver.firefox.service import Service

    my_service = Service()
    browser = Browser('firefox', service=my_service)


Custom executable path
~~~~~~~~~~~~~~~~~~~~~~

The Service object can be used to specify the path to geckodriver.
For example:

.. code-block:: python

    from splinter import Browser
    from selenium.webdriver.firefox.service import Service

    my_service = Service(executable_path='</path/to/geckodriver>')
    browser = Browser('firefox', service=my_service)


Custom binary path
~~~~~~~~~~~~~~~~~~~~~~

The Service object can be used to specify the binary path.
For example:

.. code-block:: python

    from selenium import webdriver

    firefox_options = webdriver.firefox.options.Options()
    firefox_options.binary_location = "/path/to/firefox_nightly"
    browser = Browser('firefox', options=firefox_options)




Specify Profile
+++++++++++++++

You can specify a `Firefox profile <http://support.mozilla.com/en-US/kb/Profiles>`_ for using on ``Browser`` function
using the ``profile`` keyword (passing the name of the profile as a ``str`` instance):

.. code-block:: python

    from splinter import Browser
    browser = Browser('firefox', profile='my_profile')

If you don't specify a profile, a new temporary profile will be created (and deleted when you ``close`` the browser).


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
