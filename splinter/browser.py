# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import sys

from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.remote import WebDriver as RemoteWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
from splinter.driver.webdriver.phantomjs import WebDriver as PhantomJSWebDriver
from splinter.exceptions import DriverNotFoundError


_DRIVERS = {
    'firefox': FirefoxWebDriver,
    'remote': RemoteWebDriver,
    'chrome': ChromeWebDriver,
    'phantomjs': PhantomJSWebDriver,
}

if sys.version_info[0] <= 2:
    try:
        from splinter.driver.zopetestbrowser import ZopeTestBrowser
        _DRIVERS['zope.testbrowser'] = ZopeTestBrowser
    except ImportError:
        pass

try:
    import django  # noqa
    from splinter.driver.djangoclient import DjangoClient
    _DRIVERS['django'] = DjangoClient
except ImportError:
    pass

try:
    import flask  # noqa
    from splinter.driver.flaskclient import FlaskClient
    _DRIVERS['flask'] = FlaskClient
except ImportError:
    pass


def Browser(driver_name='firefox', *args, **kwargs):
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
    return driver(*args, **kwargs)
