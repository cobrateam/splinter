# -*- coding: utf-8 -*-
import unittest
import warnings

from nose.tools import assert_equals, raises
from splinter.exceptions import DriverNotFoundError


class BrowserTest(unittest.TestCase):

    @raises(DriverNotFoundError)
    def test_should_raise_an_exception_when_browser_driver_is_not_found(self):
        from splinter.browser import Browser
        Browser('unknown-driver')


class BrowserDeprecationTest(unittest.TestCase):

    class Foo(object):
        pass

    def test_should_deprecate_with_the_given_message(self):
        from splinter.browser import deprecate
        with warnings.catch_warnings(record=True) as warnings_list:
            cls = deprecate(self.Foo, message="Foo was deprecated")
            cls()
            warning = warnings_list[0]
            assert type(warning.message) is DeprecationWarning
            assert_equals("Foo was deprecated", warning.message.args[0])

    def test_should_prepend_a_Deprecated_to_class(self):
        from splinter.browser import deprecate
        with warnings.catch_warnings(record=True):
            cls = deprecate(self.Foo, message="Foo was deprecated")
            assert_equals("DeprecatedFoo", cls.__name__)
