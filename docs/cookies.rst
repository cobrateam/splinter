.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Cookie manipulation
    :keywords: splinter, python, tutorial, documentation, cookies

++++++++++++++++++++
Cookies manipulation
++++++++++++++++++++

It is possible to manipulate cookies using the `cookies` attribute from a
`Browser` instance. The `cookies` attribute is an instance of the `CookieManager`
class that manipulates cookies (ie: adding and deleting).

Add a cookie
------------

.. code-block:: python

    browser.cookies.add({'cookie_name': 'cookie_value'})

Retrieve all cookies
--------------------

.. code-block:: python

    cookies = browser.cookies.all()

Delete a cookie
---------------

.. code-block:: python

    browser.cookies.delete('cookie_name')  # delete the cookie 'cookie_name'
    browser.cookies.delete('cookies_name_1', 'cookies_name_2')  # delete two cookies

Delete all cookies
------------------

.. code-block:: python

    browser.cookies.delete_all()


For more details check the API reference of the
:class:`CookieManager <splinter.cookie_manager.CookieManagerAPI>` class.

Extra Arguments
~~~~~~~~~~~~~~~

Each driver accepts various parameters when creating cookies.
These can be used with browser.cookies.add as extra arguments.
For example, WebDriver can use `path`, `domain`, `secure`, and `expiry`:

::
    browser.cookies.add({'cookie_name': 'cookie_value'}, path='/cookiePath')
