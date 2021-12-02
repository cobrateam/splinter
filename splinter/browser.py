# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


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
    from splinter.driver.webdriver.edge import WebDriver as EdgeWebDriver

    _DRIVERS["edge"] = EdgeWebDriver
except ImportError:
    pass


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
    """Get a new driver instance.

    Extra arguments will be sent to the driver instance.

    If there is no driver registered with the provided ``driver_name``, this
    function will raise a :class:`splinter.exceptions.DriverNotFoundError`
    exception.

    Arguments:
        driver_name (str): Name of the driver to use.
        retry_count (int): Number of times to try and instantiate the driver.

    Returns:
        Driver instance
    """

    try:
        driver = _DRIVERS[driver_name]
    except KeyError:
        raise DriverNotFoundError("No driver for %s" % driver_name)

    return get_driver(driver, retry_count=retry_count, *args, **kwargs)
