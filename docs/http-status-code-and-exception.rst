.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Dealing with HTTP status code and HTTP exceptions with Splinter
    :keywords: splinter, python, tutorial, documentation, exception, http error, status code

++++++++++++++++++++++++++++++++++++++++++++
Dealing with HTTP status code and exceptions
++++++++++++++++++++++++++++++++++++++++++++

**Note:** After 0.8 version the `webdriver` (firefox, chrome) based drivers does not support http error
handling.

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
    # or
    browser.status_code.code # 200

The difference between those methods is that if you get a redirect (or something that is not an HTTP error),
``status_code.is_success`` will consider your response as successfully. The numeric status code can be accessed via
``status_code.code``.

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
