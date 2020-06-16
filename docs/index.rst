.. Copyright 2012-2018 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Documentation for splinter, an open source tool for testing web applications
    :keywords: splinter, python, tutorial, documentation, web application, tests, atdd, tdd, acceptance tests

Splinter
==============

Splinter is an open source tool for testing web applications using Python.
It lets you automate browser actions, such as visiting URLs and interacting with their items.

Sample code
-----------

.. highlight:: python

::

    from splinter import Browser

    with Browser() as browser:
        # Visit URL
        url = "http://www.google.com"
        browser.visit(url)
        browser.fill('q', 'splinter - python acceptance testing for web applications')
        # Find and click the 'search' button
        button = browser.find_by_name('btnG')
        # Interact with elements
        button.click()
        if browser.is_text_present('splinter.readthedocs.io'):
            print("Yes, the official website was found!")
        else:
            print("No, it wasn't found... We need to improve our SEO techniques")

**Note:** if you don't provide any driver to the ``Browser`` function, ``firefox`` will be used.

Features
--------

* simple api
* multiple webdrivers (chrome, firefox, zopetestbrowser, remote
  webdriver, Django, Flask)
* css and xpath selectors
* support for iframes and alerts
* can execute javascript
* works with ajax and async javascript

Getting started
---------------
* :doc:`Why use Splinter </why>`
* :doc:`Installation </install>`
* :doc:`Quick tutorial </tutorial>`

Basic browsing and interactions
-------------------------------

* :doc:`Browser and navigation </browser>`
* :doc:`Finding elements </finding>`
* :doc:`Mouse interactions </mouse-interaction>`
* :doc:`Interacting with elements and forms </elements-in-the-page>`
* :doc:`Verify the presence of texts and elements in a page, with matchers </matchers>`
* :doc:`Cookies manipulation </cookies>`
* :doc:`Take screenshot </screenshot>`

JavaScript support
------------------

* :doc:`Executing JavaScript </javascript>`

Walking on...
-------------

* :doc:`Dealing with HTTP status code and exceptions </http-status-code-and-exception>`
* :doc:`Using HTTP proxies </http-proxies>`
* :doc:`Interacting with iframes, alerts and prompts </iframes-and-alerts>`
* :doc:`Full API documentation </api/index>`

Drivers
-------

Browser based drivers
+++++++++++++++++++++

The following drivers open a browser to run your actions:

* :doc:`Chrome WebDriver </drivers/chrome>`
* :doc:`Firefox WebDriver </drivers/firefox>`

Headless drivers
++++++++++++++++

The following drivers don't open a browser to run your actions (but each has its own dependencies, check the
specific docs for each driver):

* :doc:`Chrome WebDriver (headless option) </drivers/chrome>`
* :doc:`Firefox WebDriver  (headless option) </drivers/firefox>`
* :doc:`zope.testbrowser </drivers/zope.testbrowser>`
* :doc:`django client </drivers/django>`
* :doc:`flask client </drivers/flask>`

Remote driver
++++++++++++++

The remote driver uses Selenium Remote to control a web browser on a remote
machine.

* :doc:`Remote WebDriver </drivers/remote>`


Get in touch and contribute
===========================

* :doc:`Community </community>`
* :doc:`Contribute </contribute>`
* :doc:`Writing new drivers </contribute/writing-new-drivers>`
* :doc:`Setting up your splinter development environment </contribute/setting-up-your-development-environment>`

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
