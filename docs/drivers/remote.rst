.. Copyright 2013 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Remote webdriver
    :keywords: splinter, python, tutorial, how to install, installation, remote, selenium


++++++++++++++++
Remote WebDriver
++++++++++++++++

Remote WebDriver is provided by Selenium2. To use it, you need to install
Selenium2 via pip:

.. highlight:: bash

::

    $ [sudo] pip install selenium

Setting up the Remote WebDriver
-------------------------------

To use the remote web driver, you need to have access to a Selenium remote
webdriver server. Setting up one of these servers is beyond the scope of this
document. However, some companies provide access to a `Selenium Grid`_ as a service.


Useing the Remote WebDriver
---------------------------

To use the Remote WebDriver, you need to pass ``driver_name="remote"``
and ``url=<remote server url>`` when you create the ``Browser`` instance.

You can also pass additional arguments to the additional arguments that
correspond to Selenium `DesiredCapabilities`_ arguments.

Here is an example that uses `Sauce Labs`_ (a company that provides Selenium
remote webdriver servers as a service) to request an Internet Explorer 9
browser instance running on Windows 7.

.. highlight:: python

::

    remote_server_url = ... # Specify the server URL

    with Browser(driver_name="remote",
                 url=remote_server_url,
                 browser='internetexplorer',
                 platform="Windows 7",
                 version="9",
                 name="Test of IE 9 on WINDOWS") as browser:
        print("Link to job: https://saucelabs.com/jobs/{}".format(
              browser.driver.session_id))
        browser.visit("http://splinter.cobrateam.info")
        browser.find_link_by_text('documentation').first.click()


.. _Selenium Grid: https://code.google.com/p/selenium/wiki/Grid2
.. _DesiredCapabilities: https://code.google.com/p/selenium/wiki/DesiredCapabilities
.. _Sauce Labs: https://saucelabs.com