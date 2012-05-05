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
