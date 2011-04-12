AttributeError from a method call should not be hidden by exception
handling intended to ignore the case where the method is not present.

    >>> import sys
    >>> import unittest

    >>> import nose.case
    >>> import nose.proxy
    >>> import nose.result
    >>> import nose.util
    >>> import nose.plugins.doctests

    >>> class Result(nose.result.TextTestResult):
    ...
    ...     def afterTest(self, test):
    ...         raise AttributeError("bug in Result")
    ...
    ...     def beforeTest(self, test):
    ...         raise AttributeError("bug in Result")

    >>> class TestCase(unittest.TestCase):
    ...
    ...     def address(self):
    ...         raise AttributeError("bug in TestCase")
    ...
    ...     def runTest(self):
    ...         pass


    >>> test = nose.case.Test(TestCase())
    >>> result = Result(sys.stdout, True, 1)
    >>> proxy = nose.proxy.ResultProxy(result, test)
    >>> proxy.beforeTest(test)
    Traceback (most recent call last):
    AttributeError: bug in Result
    >>> proxy.afterTest(test)
    Traceback (most recent call last):
    AttributeError: bug in Result

    >>> test.address()
    Traceback (most recent call last):
    AttributeError: bug in TestCase

    >>> nose.util.test_address(test)
    Traceback (most recent call last):
    AttributeError: bug in TestCase
