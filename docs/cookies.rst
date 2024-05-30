.. Copyright 2012 splinter authors. All rights reserved.
   Use of this source code is governed by a BSD-style
   license that can be found in the LICENSE file.

.. meta::
    :description: Cookies
    :keywords: splinter, python, tutorial, documentation, cookies

+++++++
Cookies
+++++++

It is possible to manipulate cookies using the `cookies` attribute from a
`Browser` instance.


Add a cookie
------------

.. code-block:: python

    browser.cookies.add({'chocolate_chip': '200'})

Extra Arguments
~~~~~~~~~~~~~~~

Each driver accepts various parameters when creating cookies.
These can be used with browser.cookies.add as extra arguments.
For example, WebDriver can use `path`, `domain`, `secure`, and `expiry`:

.. code-block:: python

    browser.cookies.add({'chocolate_chip': '200'}, path='/cookiePath')

Retrieve all cookies
--------------------

.. code-block:: python

    cookies = browser.cookies.all()

Delete a cookie
---------------

Given a cookie named `chocolate_chip`, we can delete it by passing the name
to the `delete` method:

.. code-block:: python

    browser.cookies.delete('chocolate_chip')

Multiple cookie names can be passed to `delete`:

.. code-block:: python

    browser.cookies.delete('chocolate_chip', 'blueberry')

Delete all cookies
------------------

.. code-block:: python

    browser.cookies.delete_all()

Further Reading
---------------

For more details see the API reference for the
:class:`CookieManager <splinter.abc.cookie_manager.CookieManagerAPI>` class.
