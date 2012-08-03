.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Finding elements
    :keywords: splinter, python, tutorial, screenshot

++++++++++++++++++
Taking screenshots
++++++++++++++++++

Splinter doesn't support taking screenshots by itself, to take screenshots you must to call the driver's `take_screenshot` method:

.. highlight:: python

::

    browser = Browser()
    browser.driver.save_screenshot('your_screenshot.png')
