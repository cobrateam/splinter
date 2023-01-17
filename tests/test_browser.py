# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


import builtins
from importlib import reload

from splinter.exceptions import DriverNotFoundError

import pytest


def patch_driver(pattern):
    old_import = builtins.__import__

    def custom_import(name, *args, **kwargs):
        if pattern in name:
            return None
        return old_import(name, *args, **kwargs)

    builtins.__import__ = custom_import

    return old_import


def unpatch_driver(module, old_import):
    builtins.__import__ = old_import
    reload(module)


def test_browser_can_still_be_imported_from_splinters_browser_module():
    from splinter.browser import Browser  # NOQA


def test_browser_should_work_even_without_zope_testbrowser():
    old_import = patch_driver("zope")
    from splinter import browser

    reload(browser)
    assert None is browser._DRIVERS['zope.testbrowser']

    unpatch_driver(browser, old_import)


def test_browser_message_on_missing_driver():
    old_import = patch_driver("zope")
    from splinter import browser

    reload(browser)

    with pytest.raises(DriverNotFoundError) as e:
        from splinter import Browser

        Browser("zope.testbrowser")

    assert 'Driver for zope.testbrowser was not found.' == str(e.value)

    unpatch_driver(browser, old_import)


def test_browser_should_raise_an_exception_when_driver_is_not_found():
    with pytest.raises(DriverNotFoundError):
        from splinter import Browser

        Browser("unknown-driver")


def test_browser_driver_retry_count():
    """Checks that the retry count is being used"""
    from splinter.browser import _DRIVERS
    from splinter import Browser
    global test_retry_count

    def test_driver(*args, **kwargs):
        global test_retry_count
        test_retry_count += 1
        raise IOError("test_retry_count: " + str(test_retry_count))
    _DRIVERS["test_driver"] = test_driver

    test_retry_count = 0
    with pytest.raises(IOError) as e:
        Browser("test_driver")
    assert "test_retry_count: 3" == str(e.value)

    test_retry_count = 0
    with pytest.raises(IOError) as e:
        Browser("test_driver", retry_count=10)
    assert "test_retry_count: 10" == str(e.value)

    del test_retry_count
    del _DRIVERS["test_driver"]


def test_browser_log_missing_drivers(caplog):
    """Missing drivers are logged at the debug level."""
    import logging
    caplog.set_level(logging.DEBUG)
    old_import = patch_driver("flask")
    from splinter import browser

    reload(browser)
    unpatch_driver(browser, old_import)

    assert 7 == len(caplog.records)
    for i in range(0, 6):
        record = caplog.records[i]
        assert record.levelname == 'DEBUG'
        assert 'Import Warning' in record.message
