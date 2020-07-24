.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Selenium Keys
    :keywords: splinter, python, tutorial, documentation, selenium integration, selenium keys, keyboard events

+++++++++++++
Selenium Keys
+++++++++++++

With Splinter's type() method, you can use Selenium's Keys implementation.

.. highlight:: python

::

    from selenium.webdriver.common.keys import Keys
    from splinter import Browser


    browser = Browser()
    browser.type(Keys.RETURN)

The full list of all supported keys can be found at the official Selenium documentation:
`selenium.webdriver.common.keys <https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html>`_