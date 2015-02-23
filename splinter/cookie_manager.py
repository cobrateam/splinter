# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from splinter.meta import InheritedDocs


class CookieManagerAPI(InheritedDocs('_CookieManagerAPI', (object,), {})):
    """
    An API that specifies how a splinter driver deals with cookies.

    You can add cookies using the :meth:`add <CookieManagerAPI.add>` method,
    and remove one or all cookies using
    the :meth:`delete <CookieManagerAPI.delete>` method.

    A CookieManager acts like a ``dict``, so you can access the value of a
    cookie through the [] operator, passing the cookie identifier:

        >>> cookie_manager.add({'name': 'Tony'})
        >>> assert cookie_manager['name'] == 'Tony'
    """

    def add(self, cookies):
        """
        Adds a cookie.

        The ``cookie`` parameter is a ``dict`` where each key is an identifier
        for the cookie value (like any ``dict``).

        Example of use:

            >>> cookie_manager.add({'name': 'Tony'})
        """
        raise NotImplementedError

    def delete(self, *cookies):
        """
        Deletes one or more cookies. You can pass all the cookies identifier
        that you want to delete.

        If none identifier is provided, all cookies are deleted.

        Examples:

            >>> cookie_manager.delete() # deletes all cookies
            >>> cookie_manager.delete('name', 'birthday',
                                      'favorite_color') # deletes these three cookies
            >>> cookie_manager.delete('name') # deletes one cookie
        """
        raise NotImplementedError

    def all(self, verbose=False):
        """
        Returns all of the cookies.

            **Note:** If you're using any webdriver and want more info about
            the cookie, set the `verbose` parameter to `True` (in other
            drivers, it won't make any difference). In this case, this method
            will return a list of dicts, each with one cookie's info.

        Examples:

            >>> cookie_manager.add({'name': 'Tony'})
            >>> cookie_manager.all()
            [{'name': 'Tony'}]
        """
        raise NotImplementedError

    def __getitem__(self, item):
        raise NotImplementedError

    def __eq__(self, other_object):
        raise NotImplementedError
