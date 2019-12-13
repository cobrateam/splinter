.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Cookie manipulation
    :keywords: splinter, python, tutorial, documentation, cookies

++++++++++++++++++++
Cookies Manipulation
++++++++++++++++++++

It is possible to manipulate cookies using the `cookies` attribute from a
`Browser` instance. The `cookies` attribute is a instance of a `CookieManager`
class that manipulates cookies (ie: adding and deleting them).

Create Cookie
-------------

To add a cookie use the browser.cookies.add method:

.. highlight:: python

::

    browser.cookies.add('cookie name', 'cookie value')

Extra Arguments
~~~~~~~~~~~~~~~

Each driver accepts various parameters when creating cookies.
These can be used with browser.cookies.add as extra arguments.
For example, WebDriver can use `path`, `domain`, `secure`, and `expiry`:

::
    browser.cookies.add('cookie_name', 'cookie_value', path='/cookiePath')

Retrieve All Cookies
--------------------

To retrieve all cookies use the `all` method:

.. highlight:: python

::

    browser.cookies.all()

Delete a cookie
---------------

You can delete one or more cookies with the ``delete`` method:

.. highlight:: python

::

    browser.cookies.delete('mwahahahaha')  # deletes the cookie 'mwahahahaha'
    browser.cookies.delete('whatever', 'wherever')  # deletes two cookies

Delete all cookies
------------------

You can also delete all cookies: just call the ``delete`` method without any
parameters:

.. highlight:: python

::

    browser.cookies.delete()  # deletes all cookies

For more details check the API reference of the
:class:`CookieManager <splinter.cookie_manager.CookieManagerAPI>` class.
