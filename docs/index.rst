.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Documentation for splinter, an open source tool for testing web applications
    :keywords: splinter, python, tutorial, documentation, web application, tests, atdd, tdd, acceptance tests


+++++++++++++++++++++++++++++++++++++++++++++
automate web application actions using python
+++++++++++++++++++++++++++++++++++++++++++++

:doc:`what's new in splinter? </news>`

Using splinter
==============

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

JavaScript support
------------------

* :doc:`Executing JavaScript </javascript>`

Walking on...
-------------

* :doc:`Dealing with HTTP status code and exceptions </http-status-code-and-exception>`
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

The following drivers don't open a browser to run your actions (but has its own dependencies, check the
specific docs for each driver):

* :doc:`Phantomjs WebDriver </drivers/phantomjs>`
* :doc:`zope.testbrowser </drivers/zope.testbrowser>`
*
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
