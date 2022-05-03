.. Copyright 2012-2018 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Documentation for splinter, an open source tool for testing web applications
    :keywords: splinter, python, tutorial, documentation, web application, tests, atdd, tdd, acceptance tests

Splinter
==============

Splinter is an open source tool for testing web applications using Python.
It lets you automate browser actions such as visiting URLs and interacting with their elements.

Sample code
-----------

.. highlight:: python

::

    from splinter import Browser

    with Browser() as browser:
        # Visit URL.
        browser.visit("http://www.google.com")

        # Find and fill out the search form.
        browser.find_by_name('q').fill('splinter - python acceptance testing for web applications')

        # Find and click the 'search' button.
        button = browser.find_by_name('btnK').click()

        # Check for result on the page.
        if browser.is_text_present('splinter.readthedocs.io'):
            print("Yes, the official website was found!")
        else:
            print("No, it wasn't found... We need to improve our SEO techniques")

**Note:** if you don't provide any driver to the ``Browser`` function, ``firefox`` will be used.

Features
--------

* Simple API
* Support for multiple drivers
* Support for iframes and alerts
* Can execute javascript
* Works with ajax and async javascript


.. toctree::
   :caption: Getting Started
   :hidden:

   why
   install
   tutorial

.. toctree::
   :caption: Browsing and Interactions
   :hidden:

   browser
   finding
   mouse-interaction
   elements-in-the-page
   matchers
   cookies
   screenshot

.. toctree::
   :caption: JavaScript
   :hidden:

   javascript

.. toctree::
   :caption: Drivers
   :hidden:

   drivers/chrome
   drivers/firefox
   drivers/edge
   drivers/remote
   drivers/zope.testbrowser
   drivers/django
   drivers/flask

.. toctree::
   :caption: More
   :hidden:

   http-status-code-and-exception
   http-proxies
   iframes-and-alerts
   api/index
   selenium-keys

.. toctree::
  :caption: Changelog
  :hidden:
  :maxdepth: 2
  :glob:

  news

.. toctree::
   :caption: Get in touch and contribute
   :hidden:

   community
   contribute
   contribute/writing-new-drivers
   contribute/setting-up-your-development-environment
