.. Copyright 2013 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: How to use splinter with Remote WebDriver
    :keywords: splinter, python, tutorial, how to install, installation, remote, selenium


++++++++++++++++
Remote WebDriver
++++++++++++++++

Remote WebDriver is provided by Selenium. To use it, you need to install
Selenium via pip:

.. highlight:: bash

::

    $ [sudo] pip install selenium

Setting up the Remote WebDriver
-------------------------------

To use Remote WebDriver, you need to have access to a Selenium remote
WebDriver server. Setting up one of these servers is beyond the scope of this
document. However, some companies provide access to a `Selenium Grid`_ as a service.


Using the Remote WebDriver
--------------------------

To use the Remote WebDriver, use ``driver_name="remote"`` when you create the ``Browser`` instance.

The ``browser_name`` argument should then be used to specify the web browser.
The other arguments match Selenium's `Remote WebDriver`_ arguments.

`Desired Capabilities`_ will be set automatically based on Selenium's defaults.
These can be expanded and/or replaced by providing your own.

The following example uses `Sauce Labs`_ (a company that provides Selenium
Remote WebDriver servers as a service) to request an Internet Explorer 9
browser instance running on Windows 7.

.. highlight:: python

::

    # Specify the server URL
    remote_server_url = 'http://YOUR_SAUCE_USERNAME:YOUR_SAUCE_ACCESS_KEY@ondemand.saucelabs.com:80/wd/hub'

    with Browser(
        driver_name="remote",
        browser='internetexplorer',
        command_executor=remote_server_url,
        desired_capabilities = {
          'platform': 'Windows 7',
          'version': '9',
          'name': 'Test of IE 9 on WINDOWS',
        },
        keep_alive=True,
    ) as browser:
        print("Link to job: https://saucelabs.com/jobs/{}".format(
              browser.driver.session_id))
        browser.visit("https://splinter.readthedocs.io")
        browser.find_by_text('documentation').first.click()


.. _Desired Capabilities: https://selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.desired_capabilities.html
.. _Selenium Grid: https://selenium.dev/documentation/en/grid/
.. _Sauce Labs: https://saucelabs.com
.. _Remote WebDriver: https://selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html
