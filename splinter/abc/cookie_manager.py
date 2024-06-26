# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from abc import ABC
from abc import abstractmethod
from typing import Dict


class CookieManagerAPI(ABC):
    """Specification for how a Splinter driver handles cookies.

    CookieManager implementations are driver-specific.
    They should not be created by the end-user. To access a CookieManager,
    drivers should implement a `cookies` attribute containing a CookieManager.

    CookieManager has behaviour similar to a ``dict``, thus
    you should get the value of a cookie using the [] operator:

    Example:

        >>> browser.cookies.add({'name': 'Tony'})
        >>> assert browser.cookies['name'] == 'Tony'
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def add(self, cookie: Dict[str, str], **kwargs) -> None:
        """Add a cookie.

        Arguments:
            cookie: A key/value pair containing the cookie's name and value.
            kwargs: Driver-specific extra arguments to build the cookie with.

        Example:

            >>> browser.cookies.add({'cookie_name': 'cookie_value'}, path='/')
            >>> assert browser.cookies['cookie_name'] == 'cookie_value'
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, *cookies: str) -> None:
        """Delete one or more cookies.

        If the cookie does not exist, this function has no effect.

        Arguments:
            cookies (str): Identifiers for each cookie to delete.

        Example:

            >>> browser.cookies.delete('name', 'birthday', 'favorite_color')
            >>> browser.cookies.delete('name')
            >>> assert 'name' not in browser.cookies.all().keys()
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

        Example:

            >>> browser.cookies.add({'name': 'Tony'})
            >>> result = browser.cookies.all()

        Returns:
            All the available cookies.
        """
        raise NotImplementedError

    @abstractmethod
    def __contains__(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __getitem__(self, item: str):
        raise NotImplementedError

    @abstractmethod
    def __eq__(self, other_object) -> bool:
        raise NotImplementedError
