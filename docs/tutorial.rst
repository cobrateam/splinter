.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Splinter tutorial, learn how to test your web applications
    :keywords: splinter, python, tutorial, documentation, web application

++++++++
Tutorial
++++++++

Before starting, make sure Splinter is :doc:`installed <install/install>`

This tutorial provides a simple example, teaching step by step how to:

* search for ``splinter - python acceptance testing for web applications'`` in google.com, and
* find if splinter official website is listed among the search results

Create a Browser instance
=========================

Import the ``Browser`` class and instantiate it:

.. code-block:: python

    from splinter import Browser


    browser = Browser()


**Note:** if you don't provide any argument to the ``Browser`` function, ``firefox`` will be used (`Browser function documentation <https://splinter.readthedocs.io/en/latest/api/driver-and-element-api.html>`_).


Visit a website
===============

Navigate to any website using the ``browser.visit()`` method.

Let's go to Google:

.. code-block:: python
    :emphasize-lines: 6

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')


Find an element
===============

After a page is loaded, you can perform actions, such as clicking, filling text input, checking radio and checkboxes.

To do that, first you must find the correct element:

.. code-block:: python
    :emphasize-lines: 7

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')
    input_element = browser.find_by_name('q')


Input text
==========

Let's fill Google's search element with ``splinter - python acceptance testing for web applications``:

.. code-block:: python
    :emphasize-lines: 8

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')
    input_element = browser.find_by_name('q')
    input_element.fill('splinter - python acceptance testing for web applications')


Click a button
==============

Tell Splinter which button should be pressed. A button - or any other element - can be identified using its css, xpath, id, tag or name.

In order to find Google's search button, do:

.. code-block:: python
    :emphasize-lines: 10

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')
    input_element = browser.find_by_name('q')
    input_element.fill('splinter - python acceptance testing for web applications')
    # There are two elements with name btnK - only the second is visible
    button_element = browser.find_by_name('btnK')[1]


**Note** The name ``btnK`` was found by inspecting Google's search page source code.

With the button identified, we can then click it:

.. code-block:: python
    :emphasize-lines: 11

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')
    input_element = browser.find_by_name('q')
    input_element.fill('splinter - python acceptance testing for web applications')
    # There are two elements with name btnK - only the second is visible
    button_element = browser.find_by_name('btnK')[1]
    button_element.click()


**Note:** Both steps presented above could be joined in a single line, such as:

.. code-block:: python
    :emphasize-lines: 7,8

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')
    browser.find_by_name('q').fill('splinter - python acceptance testing for web applications')
    browser.find_by_name('btnK')[1].click()


Check for results
=================

After pressing the button, you can check if Splinter official website is among the search responses. This can be done like this:

.. code-block:: python
    :emphasize-lines: 13,14,15,16

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')
    input_element = browser.find_by_name('q')
    input_element.fill('splinter - python acceptance testing for web applications')
    # There are two elements with name btnK - only the second is visible
    button_element = browser.find_by_name('btnK')[1]
    button_element.click()

    if browser.is_text_present('splinter.readthedocs.io'):
        print("Yes, found it! :)")
    else:
        print("No, didn't find it :(")


In this case, we are just printing something. You might use assertions, if you're writing tests.

Close the browser
=================

When you've finished testing, close your browser using ``browser.quit``:

.. code-block:: python
    :emphasize-lines: 18

    from splinter import Browser


    browser = Browser()

    browser.visit('http://google.com')
    input_element = browser.find_by_name('q')
    input_element.fill('splinter - python acceptance testing for web applications')
    # There are two elements with name btnK - only the second is visible
    button_element = browser.find_by_name('btnK')[1]
    button_element.click()

    if browser.is_text_present('splinter.readthedocs.io'):
        print("Yes, the official website was found!")
    else:
        print("No, it wasn't found... We need to improve our SEO techniques")

    browser.quit()
