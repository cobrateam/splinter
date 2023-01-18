.. Copyright 2021 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Edge WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, edge, selenium

++++++++++++++
Edge WebDriver
++++++++++++++


Usage
-----

To use the Edge driver, pass the string ``edge`` when you create
the ``Browser`` instance:

.. code-block:: python

    from splinter import Browser
    browser = Browser('edge')

Edge Options
++++++++++++

Selenium Options can be passed to customize Edge's behaviour through the
``EdgeOptions`` object

.. code-block:: python

    from selenium.webdriver.edge.options import Options
    from splinter import Browser

    mobile_emulation = {"deviceName": "Google Nexus 5"}
    edge_options = Options()
    browser = Browser('edge', options=edge_options)

Headless mode
+++++++++++++

To use headless mode, pass the `headless` argument
when creating a new Browser instance.

.. code-block:: python

    from splinter import Browser
    browser = Browser('edge', headless=True)

Incognito mode
++++++++++++++

To use Edge's incognito mode, pass the `incognito` argument
when creating a Browser instance.

.. code-block:: python

    from splinter import Browser
    browser = Browser('edge', incognito=True)

Emulation mode
++++++++++++++

Since Selenium options can be passed to customize Edge's behaviour;
it is then possible to leverage the experimental emulation mode.

.. code-block:: python

    from selenium.webdriver.edge.options import Options
    from splinter import Browser

    mobile_emulation = {"deviceName": "Google Nexus 5"}
    edge_options = Options()
    edge_options.add_experimental_option(
      "mobileEmulation", mobile_emulation,
    )
    browser = Browser('edge', options=edge_options)

Service
+++++++

Selenium uses the Service class to manage edgedriver.
An instance of this class can be given directly to Splinter.

.. code-block:: python

    from splinter import Browser
    from selenium.webdriver.chrome.service import Service

    my_service = Service()
    browser = Browser('chrome', service=my_service)


Custom executable path
~~~~~~~~~~~~~~~~~~~~~~

The Service object can be used to specify the path to edgedriver.
For example:

.. code-block:: python

    from splinter import Browser
    from selenium.webdriver.edge.service import Service

    my_service = Service(executable_path='</path/to/edgedriver>')
    browser = Browser('edge', service=my_service)


Edge Legacy
+++++++++++

By default, Edge WebDriver is configured to use versions of Edge built with
Chromium (Version 79 and up).

To use Edge Legacy, pass the `chromium` argument when creating a new Browser
instance.

This requires the correct version of Edge and Edge Driver to be installed.

.. code-block:: python

    from splinter import Browser
    browser = Browser('edge', chromium=False)

API docs
--------

.. autoclass:: splinter.driver.webdriver.edge.WebDriver
   :members:
   :inherited-members:
