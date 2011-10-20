.. meta::
    :description: Cookie manipulation
    :keywords: splinter, python, tutorial, documentation, cookies

++++++++++++++++++++
Cookies manipulation
++++++++++++++++++++

It's possible manipulate cookies using `cookies` attribute from a `Browser` instance. The `cookies` attribute is a instance of a `CookieManager` class that manipulate cookies, like, add and delete cookies.

Create cookie
-------------

For add a cookie use the add method:

.. highlight:: python

::

    browser.cookies.add({'whatever': 'and ever'})

Delete a cookie
---------------

You can delete one or more cookies with the ``delete`` method:

.. highlight:: python

::

    browser.cookies.delete('mwahahahaha') #deletes the cookie 'mwahahahaha'
    browser.cookies.delete('whatever', 'wherever') #deletes two cookies

Delete all cookies
------------------

You also can delete all cookies: just call the ``delete`` method without any
parameters:

.. highlight:: python

::

    browser.cookies.delete() #deletes all cookies

For more details, check the API reference for the
:class:`CookieManager <splinter.cookie_manager.CookieManagerAPI>` class.
