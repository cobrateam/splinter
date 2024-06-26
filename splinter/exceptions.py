# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class DriverNotFoundError(Exception):
    """
    Exception raised when a driver is not found.

    Example:

        >>> from splinter import Browser
        >>>
        >>>
        >>> try:
        ...     b = Browser('unknown driver')
        ... except DriverNotFoundError:
        ...    pass
    """

    pass


class ElementDoesNotExist(Exception):
    """
    Exception raised when an element is not found in the page.

    The exception is raised only when someone tries to access the element,
    not when the driver is finding it.

    Example:

        >>> elements = browser.find_by_id('unknown-id') # returns an empty list
        >>> try:
        ...     elements[0]
        ... except ElementDoesNotExist:
        ...     pass
    """

    pass
