# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


import logging

from http.client import HTTPException
from typing import Dict, Tuple, Type, Union

from urllib3.exceptions import MaxRetryError

from splinter.driver import DriverAPI
from splinter.exceptions import DriverNotFoundError

logger = logging.getLogger(__name__)

driver_exceptions: Tuple[Type[Exception], ...] = (IOError, HTTPException, MaxRetryError)

try:
    from selenium.common.exceptions import WebDriverException
    driver_exceptions += (WebDriverException,)
except ImportError as e:
    logger.debug(f"Import Warning: {e}")


_DRIVERS: Dict[str, Union[None, Type[DriverAPI]]] = {
    'chrome': None,
    'edge': None,
    'firefox': None,
    'remote': None,
    'django': None,
    'flask': None,
    'zope.testbrowser': None,
}

try:
    from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
    from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
    from splinter.driver.webdriver.remote import WebDriver as RemoteWebDriver

    _DRIVERS['chrome'] = ChromeWebDriver
    _DRIVERS['firefox'] = FirefoxWebDriver
    _DRIVERS['remote'] = RemoteWebDriver
except ImportError as e:
    logger.debug(f'Import Warning: {e}')

try:
    from splinter.driver.webdriver.edge import WebDriver as EdgeWebDriver

    _DRIVERS["edge"] = EdgeWebDriver
except ImportError as e:
    logger.debug(f'Import Warning: {e}')


try:
    from splinter.driver.zopetestbrowser import ZopeTestBrowser

    _DRIVERS["zope.testbrowser"] = ZopeTestBrowser
except ImportError as e:
    logger.debug(f'Import Warning: {e}')

try:
    import django  # noqa
    from splinter.driver.djangoclient import DjangoClient

    _DRIVERS["django"] = DjangoClient
except ImportError as e:
    logger.debug(f'Import Warning: {e}')

try:
    import flask  # noqa
    from splinter.driver.flaskclient import FlaskClient

    _DRIVERS["flask"] = FlaskClient
except ImportError as e:
    logger.debug(f'Import Warning: {e}')


def get_driver(driver, retry_count=3, *args, **kwargs):
    """Try to instantiate the driver.

    Common selenium errors are caught and a retry attempt occurs.
    This can mitigate issues running on Remote WebDriver.

    """
    err = None

    for _ in range(retry_count):
        try:
            return driver(*args, **kwargs)
        except driver_exceptions as e:
            err = e

    raise err


def Browser(driver_name: str = "firefox", retry_count: int = 3, *args, **kwargs):  # NOQA: N802
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
        raise DriverNotFoundError(f'{driver_name} is not a recognized driver.')

    if driver is None:
        raise DriverNotFoundError(f'Driver for {driver_name} was not found.')

    return get_driver(driver, retry_count=retry_count, *args, **kwargs)
