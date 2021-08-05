.. Copyright 2021 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Edge WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, edge, selenium

++++++++++++++
Edge WebDriver
++++++++++++++

Installation
------------

Microsoft Edge has extra requirements:

    - `msedge-selenium-tools <https://github.com/microsoft/edge-selenium-tools>`_

Using pip, they can be installed automatically:

.. code-block:: console

    pip install splinter[edge]

The following applications are also required:

  - `Microsoft Edge <https://www.microsoft.com/edge>`_
  - `Microsoft Edge Driver <https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/>`_

Microsoft Edge Driver must also be available on your operating system's `PATH` environment variable.

Mac OS X
++++++++

Modern versions of Edge (79+) are available for Mac OS X.
However, no versions of Edge Legacy are available.


Linux
+++++

Neither version of Edge is available for Linux, and thus Edge WebDriver
cannot be used on Linux systems.


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

It must be imported from the ``msedge-selenium-tools`` package.

.. code-block:: python

    from msedge.selenium_tools import EdgeOptions
    from splinter import Browser

    mobile_emulation = {"deviceName": "Google Nexus 5"}
    edge_options = EdgeOptions()
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

    from msedge.selenium_tools import EdgeOptions
    from splinter import Browser

    mobile_emulation = {"deviceName": "Google Nexus 5"}
    edge_options = EdgeOptions()
    edge_options.add_experimental_option(
      "mobileEmulation", mobile_emulation,
    )
    browser = Browser('edge', options=edge_options)

Custom executable path
++++++++++++++++++++++

Edge can also be used from a custom path.
Pass the executable path as a dictionary to the `**kwargs` argument.
The dictionary should be set up with `executable_path` as the key and
the value set to the path to the executable file.

.. code-block:: python

    from splinter import Browser
    executable_path = {'executable_path':'</path/to/edge>'}

    browser = Browser('edge', **executable_path)

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