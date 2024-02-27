# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from abc import ABC, abstractmethod


class CookieManagerAPI(ABC):
    """Specification for how a Splinter driver deals with cookies.

    Add cookies using the :meth:`add <CookieManagerAPI.add>` method,
    and remove cookies using
    the :meth:`delete <CookieManagerAPI.delete>` and
    :meth:`delete <CookieManagerAPI.delete_all>`methods.

    A CookieManager acts like a ``dict``, so you can access the value of a
    cookie through the [] operator, passing the cookie identifier:

    Examples:

        >>> cookie_manager.add({'name': 'Tony'})
        >>> assert cookie_manager['name'] == 'Tony'
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def add(self, cookie, **kwargs) -> None:
        """Add a cookie.

        Extra arguments will be used to build the cookie.

        Arguments:
            cookie (dict): Each key is an identifier for the cookie value.

        Examples:

            >>> cookie_manager.add({'name': 'Tony'})
            >>> browser.cookies.add({'cookie_name': 'cookie_value'}, path='/cookiePath')
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, *cookies: str) -> None:
        """Delete one or more cookies.

        You can pass all the cookies identifier that you want to delete.

        Arguments:
            cookies (list): Identifiers for each cookie to delete.

        Examples:

            >>> cookie_manager.delete(
                'name', 'birthday', 'favorite_color') # deletes these three cookies
            >>> cookie_manager.delete('name') # deletes one cookie
        """
        raise NotImplementedError

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all cookies."""
        raise NotImplementedError

    @abstractmethod
    def all(self, verbose: bool = False):  # NOQA: A003
        """Get all of the cookies.

            **Note:** If you're using any webdriver and want more info about
            the cookie, set the `verbose` parameter to `True` (in other
            drivers, it won't make any difference). In this case, this method
            will return a list of dicts, each with one cookie's info.

        Examples:

            >>> cookie_manager.add({'name': 'Tony'})
            >>> cookie_manager.all()
            [{'name': 'Tony'}]

        Returns:
            All the available cookies.
        """
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, key) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, item):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other_object) -> bool:
        raise NotImplementedError
