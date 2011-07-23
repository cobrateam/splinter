from nose.tools import raises
from splinter.exceptions import DriverNotFoundError

import unittest


class BrowserTest(unittest.TestCase):

    @raises(DriverNotFoundError)
    def test_should_raise_an_exception_when_browser_driver_is_not_found(self):
        from splinter.browser import Browser
        Browser('unknown-driver')
