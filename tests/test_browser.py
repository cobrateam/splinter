# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from splinter.exceptions import DriverNotFoundError

from selenium.common.exceptions import WebDriverException

import pytest

import splinter


def test_browser_can_still_be_imported_from_splinters_browser_module():
    from splinter.browser import Browser  # NOQA


def test_should_raise_an_exception_when_browser_driver_is_not_found():
    with pytest.raises(DriverNotFoundError):
        from splinter import Browser

        Browser("unknown-driver")


@pytest.mark.parametrize('browser_name', ['chrome', 'firefox'])
def test_local_driver_not_present(browser_name):
    """When chromedriver/geckodriver are not present on the system."""
    from splinter import Browser

    with pytest.raises(WebDriverException) as e:
        Browser(browser_name, executable_path='failpath')

    assert "Message: 'failpath' executable needs to be in PATH." in str(e.value)


def test_driver_retry_count():
    from splinter import Browser

    global test_retry_count

    class TestDriverPlugin:
        """Add a test driver that can return how many times it retried."""
        @splinter.hookimpl
        def splinter_prepare_drivers(self, drivers):

            def test_driver(*args, **kwargs):
                global test_retry_count
                test_retry_count += 1
                raise IOError("test_retry_count: {}".format(str(test_retry_count)))

            drivers['test_driver'] = test_driver

    splinter.plugins.register(TestDriverPlugin())

    test_retry_count = 0
    with pytest.raises(IOError) as e:
        Browser("test_driver")
    assert "test_retry_count: 3" == str(e.value)

    test_retry_count = 0
    with pytest.raises(IOError) as e:
        Browser("test_driver", retry_count=10)
    assert "test_retry_count: 10" == str(e.value)
