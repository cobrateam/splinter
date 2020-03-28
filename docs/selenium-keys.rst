.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Selenium Keys
    :keywords: splinter, python, tutorial, documentation, selenium integration, selenium keys, keyboard events

++++++++++++++++++
Selenium Keys
++++++++++++++++++

With Splinter You can use selenium keys implementation.

Here is a simple example:

.. highlight:: python

::

    from selenium.webdriver.common.keys import Keys
    ElementAPI.type(Keys.RETURN)

Full list of all support keys can be found on official selenium documentation
`selenium.webdriver.common.keys <https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html>`_