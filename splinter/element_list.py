# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from splinter.exceptions import ElementDoesNotExist


class ElementList(list):
    """
    List of elements. Each member of the list is (usually) an instance
    of :class:`ElementAPI <splinter.driver.ElementAPI>`.

    Beyond the traditional list methods, the ``ElementList`` provides some
    other methods, listed below.

    There is a peculiar behavior on ElementList: you never get an
    ``IndexError``. Instead, you can an :class:`ElementDoesNotExist
    <splinter.exceptions.ElementDoesNotExist>` exception when trying to
    access an inexistent item in the list:

        >>> element_list = ElementList([])
        >>> element_list[0] # raises ElementDoesNotExist
    """

    def __init__(self, list, driver=None, find_by=None, query=None):
        """
        Creates the list.
        """
        self.extend(list)
        self.driver = driver
        self.find_by = find_by
        self.query = query

    def __getitem__(self, index):
        if not isinstance(index, int):
            return self.first[index]
        try:
            return super(ElementList, self).__getitem__(index)
        except IndexError:
            raise ElementDoesNotExist(
                u'no elements could be found with {0} "{1}"'.format(
                    self.find_by, self.query
                )
            )

    @property
    def first(self):
        """
        An alias to the first element of the list:

            >>> assert element_list[0] == element_list.first
        """
        return self[0]

    @property
    def last(self):
        """
        An alias to the last element of the list:

            >>> assert element_list[-1] == element_list.last
        """
        return self[-1]

    def is_empty(self):
        """
        Returns ``True`` if the list is empty.
        """
        return len(self) == 0

    def __getattr__(self, name):
        try:
            return getattr(self.first, name)
        except (ElementDoesNotExist, AttributeError):
            raise AttributeError(
                u"'{0}' object has no attribute '{1}'".format(
                    self.__class__.__name__, name
                )
            )
