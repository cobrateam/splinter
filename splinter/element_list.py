# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from splinter.exceptions import ElementDoesNotExist


class ElementList:
    """Collection of elements.

    Each member of the collection is by default an instance
    of :class:`ElementAPI <splinter.driver.ElementAPI>`.

    Beyond the traditional list methods, ``ElementList`` provides some
    other methods, listed below.

    There is a peculiar behavior on ElementList: you never get an
    ``IndexError``. Instead, you get an :class:`ElementDoesNotExist
    <splinter.exceptions.ElementDoesNotExist>` exception when trying to
    access a non-existent item:

        >>> element_list = ElementList([])
        >>> element_list[0] # raises ElementDoesNotExist
    """

    def __init__(self, list, driver=None, find_by=None, query=None) -> None:  # NOQA: A002
        self._container = []
        self._container.extend(list)

        self.driver = driver
        self.find_by = find_by
        self.query = query

    def __getitem__(self, index):
        if not isinstance(index, int) and not isinstance(index, slice):
            return self.first[index]
        try:
            return self._container[index]
        except IndexError:
            raise ElementDoesNotExist(
                u'no elements could be found with {0} "{1}"'.format(
                    self.find_by, self.query
                )
            )

    @property
    def first(self):
        """An alias to the first element of the list.

        Example:

            >>> assert element_list[0] == element_list.first
        """
        return self[0]

    @property
    def last(self):
        """An alias to the last element of the list.

        Example:

            >>> assert element_list[-1] == element_list.last
        """
        return self[-1]

    def is_empty(self) -> bool:
        """Check if the ElementList is empty.

        Returns:
            bool: True if the list is empty, else False
        """
        return len(self) == 0

    def __getattr__(self, name):
        try:
            return getattr(self.first, name)
        except AttributeError:
            try:
                return getattr(self._container, name)
            except AttributeError:
                raise AttributeError(
                    u"'{0}' object has no attribute '{1}'".format(
                        self.__class__.__name__, name
                    )
                )

    def __iter__(self):
        for item in self._container:
            yield item

    def __len__(self) -> int:
        """__len__ checks the internal container."""
        return len(self._container)

    def __repr__(self) -> str:
        """Return the repr of the internal container."""
        return repr(self._container)
