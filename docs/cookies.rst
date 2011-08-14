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

For delete one or more cookies use the delete method:

.. highlight:: python

::

    browser.cookies.delete('mwahahahaha')
    browser.cookies.delete('whatever', 'wherever')

Delete all cookies
------------------

For delete all cookies use the delete method without parameter:

.. highlight:: python

::

    browser.cookies.delete()

For more details, check the API :class:`docs for CookieManager objects <splinter.cookie_manager.CookieManagerAPI>`.
