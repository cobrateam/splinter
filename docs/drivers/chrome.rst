.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Chrome WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, chrome, selenium

++++++++++++++++
Chrome WebDriver
++++++++++++++++


Usage
-----

To use the Chrome driver, pass the string ``chrome`` when you create
the ``Browser`` instance:

.. code-block:: python

    from splinter import Browser
    browser = Browser('chrome')

**Note:** if you don't provide any driver to the ``Browser`` function, ``firefox`` will be used.

**Note:** if you have trouble with ``$HOME/.bash_profile``, you can try ``$HOME/.bashrc``.


Emulation mode
++++++++++++++

Chrome options can be passed to customize Chrome's behaviour; it is then possible to leverage the
experimental emulation mode.

Further Information: `chrome driver documentation <https://sites.google.com/a/chromium.org/chromedriver/mobile-emulation>`_

.. code-block:: python

    from selenium import webdriver
    from splinter import Browser

    mobile_emulation = {"deviceName": "Google Nexus 5"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
      "mobileEmulation", mobile_emulation,
    )
    browser = Browser('chrome', options=chrome_options)

Service
+++++++

Selenium uses the Service class to manage chromedriver.
An instance of this class can be given directly to Splinter.

.. code-block:: python

    from splinter import Browser
    from selenium.webdriver.chrome.service import Service

    my_service = Service()
    browser = Browser('chrome', service=my_service)


Custom executable path
~~~~~~~~~~~~~~~~~~~~~~

The Service object can be used to specify the path to chromedriver.
For example:

.. code-block:: python

    from splinter import Browser
    from selenium.webdriver.chrome.service import Service

    my_service = Service(executable_path='</path/to/chromedriver>')
    browser = Browser('chrome', service=my_service)


API docs
--------

.. autoclass:: splinter.driver.webdriver.chrome.WebDriver
   :members:
   :inherited-members:
