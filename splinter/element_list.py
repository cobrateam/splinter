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
        >>> try:
        ...     element_list[0]
        ... except ElementDoesNotExist:
        ...     pass
    """

    def __init__(
        self,
        elements: list,
        driver=None,
        find_by=None,
        query=None,
    ) -> None:
        self._container = []
        self._container.extend(elements)

        self.driver = driver
        self.find_by = find_by
        self.query = query

    def __getitem__(self, index):
        if not isinstance(index, int) and not isinstance(index, slice):
            return self.first[index]
        try:
            return self._container[index]
        except IndexError as err:
            raise ElementDoesNotExist(
                f'No elements were found with {self.find_by} "{self.query}"',
            ) from err

    @property
    def first(self):
        """An alias to the first element of the list.

        Example:

            >>> element_list = browser.find_by_css('input')
            >>> assert element_list[0] == element_list.first
        """
        return self[0]

    @property
    def last(self):
        """An alias to the last element of the list.

        Example:

            >>> element_list = browser.find_by_css('input')
            >>> assert element_list[-1] == element_list.last
        """
        return self[-1]

    def is_empty(self) -> bool:
        """Check if the ElementList is empty.

        Returns:
            bool: True if the list is empty, else False
        """
        return len(self) == 0

    def __getattr__(self, name: str):
        try:
            return getattr(self.first, name)
        except AttributeError:
            try:
                return getattr(self._container, name)
            except AttributeError as err:
                raise AttributeError(
                    f"'{self.__class__.__name__}' object has no attribute '{name}'",
                ) from err

    def __iter__(self):
        yield from self._container

    def __len__(self) -> int:
        """__len__ checks the internal container."""
        return len(self._container)

    def __repr__(self) -> str:
        """Return the repr of the internal container."""
        return repr(self._container)
