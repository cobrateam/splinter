# -*- coding: utf-8 -*-
from splinter.meta import InheritedDocs

class CookieManagerAPI(object):
    """
    An API that specifies how a splinter driver deals with cookies.

    You can add cookies using the :meth:`add <CookieManagerAPI.add>` method,
    and remove one or all cookies using the :meth:`delete <CookieManagerAPI.delete>`
    method.

    A CookieManager acts like a ``dict``, so you can access the value of a cookie through the []
    operator, passing the cookie identifier:

        >>> cookie_manager.add({ 'name' : 'Tony' })
        >>> assert cookie_manager['name'] == 'Tony'
    """
    __metaclass__ = InheritedDocs

    def add(self, cookies):
        """
        Adds a cookie.

        The ``cookie`` parameter is a ``dict`` where each key is an identifier for the cookie
        value (like any ``dict``).

        Example of use:

            >>> cookie.add({ 'name' : 'Tony' })
        """
        raise NotImplementedError

    def delete(self, *cookies):
        """
        Deletes one or more cookies. You can pass all the cookies identifier that you want to delete.

        If none identifier is provided, all cookies are deleted.

        Examples:

            >>> cookie.delete() # deletes all cookies
            >>> cookie.delete('name', 'birthday', 'favorite_color') # deletes these three cookies
            >>> cookie.delete('name') # deletes one cookie
        """
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError

    def __eq__(self, other_object):
        raise NotImplementedError
