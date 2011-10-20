# -*- coding: utf-8 -*-

class DriverNotFoundError(Exception):
    """
    Exception raised when a driver is not found.

    Example:

        >>> from splinter.browser import Browser
        >>> b = Browser('unknown driver') # raises DriverNotFoundError
    """
    pass


class ElementDoesNotExist(Exception):
    """
    Exception raised when an element is not found in the page.

    The exception is raised only when someone tries to access the element, not when
    the driver is finding it.

    Example:

        >>> elements = browser.find_by_id('unknown-id') # returns an empty list
        >>> elements[0] # raises ElementDoesNotExist
    """
    pass
