.. meta::
    :description: Documentation for splinter, an open source tool for testing web applications
    :keywords: splinter, python, tutorial, documentation, web application, tests, atdd, tdd, acceptance tests


+++++++++++++++++++++++++++++++++++++++++++++
automate web application actions using python
+++++++++++++++++++++++++++++++++++++++++++++

:doc:`what's new in splinter 0.0.3? </news>`

First steps
===========

Getting started
---------------

* :doc:`Installation </install>`
* :doc:`Setup Google Chrome driver </setup-chrome>`
* :doc:`Quick tutorial </tutorial>`

Walking on...
-------------

* :doc:`Browser </browser>`
* :doc:`Finding elements </finding>`
* :doc:`Interacting with elements </elements-in-the-page>`
* :doc:`Execute JavaScript </javascript>`
* :doc:`AJAX and asynchronous JavaScript </ajax-and-asyn-javascript>`
* :doc:`Interacting with iframes, alerts and prompts </iframes-and-alerts>`

splinter open source project
============================

* :doc:`Community </community>`
* :doc:`Contribute </contribute>`


documentation
=============

Dealing with HTTP status code
-----------------------------

It's also possible to check which HTTP status code a browser.visit gets. You can use ``status_code.is_success`` to do the work
for you or you can compare the status code directly:

.. highlight:: python

::

    browser.visit('http://cobrateam.info')
    browser.status_code.is_success() # True
    # or
    browser.status_code == 200 # True

The difference between those methods is that if you get a redirect (or something that is not an HTTP error),
``status_code.is_success`` will consider your response as successfully.

Handling HTTP exceptions
------------------------

Whenever you use the ``visit`` method, Splinter will check if the response is success or not, and if not, it will raise an
HttpResponseError exception. But don't worry, you can easily catch it:

.. highlight:: python

::

    try:
        browser.visit('http://cobrateam.info/i-want-cookies')
    except HttpResponseError, e:
        print "Oops, I failed with the status code %s and reason %s" % (e.status_code, e.reason)

..

    **Note:** ``status_code`` and this HTTP exception handling is available only for selenium webdriver
