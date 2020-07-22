.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Take screenshot
    :keywords: splinter, python, tutorial, screenshot

+++++++++++++++
Take screenshot
+++++++++++++++

Splinter can take a screenshot of the current view:

.. highlight:: python

::

    browser = Browser()
    screenshot_path = browser.screenshot('absolute_path/your_screenshot.png')

You should use the absolute path to save a screenshot. If you don't use
an absolute path, the screenshot will be saved in a temporary file.

Take a full view screenshot:

.. highlight:: python

::

    browser = Browser()
    screenshot_path = browser.screenshot('absolute_path/your_screenshot.png', full=True)

+++++++++++++++++++++++
Take element screenshot
+++++++++++++++++++++++
To use this function, install the Pillow dependency:

::

    pip install Pillow

If the element is in the current view:

.. highlight:: python

::

    browser = Browser()
    browser.visit('http://example.com')
    screenshot_path = browser.find_by_xpath('xpath_rule').first.screenshot('absolute_path/your_screenshot.png')

If the element is not in the current view:

.. highlight:: python

::

    browser = Browser()
    browser.visit('http://example.com')
    screenshot_path = browser.find_by_xpath('xpath_rule').first.screenshot('absolute_path/your_screenshot.png', full=True)


++++++++++++++++++
Take html snapshot
++++++++++++++++++
Splinter can also take a snapshot of the current HTML:

.. highlight:: python

::

    browser = Browser()
    screenshot_path = browser.html_snapshot('absolute_path/your_screenshot.html')
