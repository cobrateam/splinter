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
`Browser` instance. The `cookies` attribute is a instance of a `CookieManager`
class that manipulates cookies, like adding and deleting them.

Create cookie
-------------

To add a cookie use the add method:

.. highlight:: python

::

    browser.cookies.add({'whatever': 'and ever'})

Retrieve all cookies
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
