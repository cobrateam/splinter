# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

try:
    from httplib import HTTPException
except ImportError:
    from http.client import HTTPException

from urllib3.exceptions import MaxRetryError

from selenium.common.exceptions import WebDriverException

from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.remote import WebDriver as RemoteWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
from splinter.exceptions import DriverNotFoundError


_DRIVERS = {
    "firefox": FirefoxWebDriver,
    "remote": RemoteWebDriver,
    "chrome": ChromeWebDriver,
}


try:
    from splinter.driver.zopetestbrowser import ZopeTestBrowser

    _DRIVERS["zope.testbrowser"] = ZopeTestBrowser
except ImportError:
    pass

try:
    import django  # noqa
    from splinter.driver.djangoclient import DjangoClient

    _DRIVERS["django"] = DjangoClient
except ImportError:
    pass

try:
    import flask  # noqa
    from splinter.driver.flaskclient import FlaskClient

    _DRIVERS["flask"] = FlaskClient
except ImportError:
    pass


def get_driver(driver, retry_count=3, *args, **kwargs):
    """Try to instantiate the driver.

    Common selenium errors are caught and a retry attempt occurs.
    This can mitigate issues running on Remote WebDriver.

    """
    err = None

    for _ in range(retry_count):
        try:
            return driver(*args, **kwargs)
        except (IOError, HTTPException, WebDriverException, MaxRetryError) as e:
            err = e

    raise err


def Browser(driver_name="firefox", retry_count=3, *args, **kwargs):  # NOQA: N802
    """
    Returns a driver instance for the given name.

    When working with ``firefox``, it's possible to provide a profile name
    and a list of extensions.

    If you don't provide any driver_name, then ``firefox`` will be used.

    If there is no driver registered with the provided ``driver_name``, this
    function will raise a :class:`splinter.exceptions.DriverNotFoundError`
    exception.
    """

    try:
        driver = _DRIVERS[driver_name]
    except KeyError:
        raise DriverNotFoundError("No driver for %s" % driver_name)

    return get_driver(driver, retry_count=retry_count, *args, **kwargs)
