# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import logging
from http.client import HTTPException
from typing import Dict, Tuple, Type, Union, Optional, Any
from urllib3.exceptions import MaxRetryError
from splinter.driver import DriverAPI
from splinter.exceptions import DriverNotFoundError

logger = logging.getLogger(__name__)

# Define base exceptions tuple
driver_exceptions: Tuple[Type[Exception], ...] = (IOError, HTTPException, MaxRetryError)

# Safely add WebDriverException if available
try:
    from selenium.common.exceptions import WebDriverException
    driver_exceptions = driver_exceptions + (WebDriverException,)
except ImportError as e:
    logger.debug("Selenium WebDriverException not available: %s", str(e))

# Type alias for driver types
DriverType = Union[None, Type[DriverAPI]]

class DriverRegistry:
    """Registry for managing browser drivers."""
    
    _drivers: Dict[str, DriverType] = {
        "chrome": None,
        "edge": None,
        "firefox": None,
        "remote": None,
        "django": None,
        "flask": None,
        "zope.testbrowser": None,
    }

    @classmethod
    def register_driver(cls, name: str, driver: DriverType) -> None:
        """Register a new driver."""
        cls._drivers[name] = driver

    @classmethod
    def get_driver(cls, name: str) -> DriverType:
        """Get a registered driver."""
        return cls._drivers.get(name)

# Register WebDriver implementations
def _register_webdrivers() -> None:
    try:
        from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
        from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
        from splinter.driver.webdriver.remote import WebDriver as RemoteWebDriver
        
        DriverRegistry.register_driver("chrome", ChromeWebDriver)
        DriverRegistry.register_driver("firefox", FirefoxWebDriver)
        DriverRegistry.register_driver("remote", RemoteWebDriver)
    except ImportError as e:
        logger.debug("WebDriver import failed: %s", str(e))

    try:
        from splinter.driver.webdriver.edge import WebDriver as EdgeWebDriver
        DriverRegistry.register_driver("edge", EdgeWebDriver)
    except ImportError as e:
        logger.debug("Edge WebDriver import failed: %s", str(e))

# Register other drivers
def _register_other_drivers() -> None:
    try:
        from splinter.driver.zopetestbrowser import ZopeTestBrowser
        DriverRegistry.register_driver("zope.testbrowser", ZopeTestBrowser)
    except ImportError as e:
        logger.debug("Zope TestBrowser import failed: %s", str(e))

    try:
        import django  # noqa
        from splinter.driver.djangoclient import DjangoClient
        DriverRegistry.register_driver("django", DjangoClient)
    except ImportError as e:
        logger.debug("Django client import failed: %s", str(e))

    try:
        import flask  # noqa
        from splinter.driver.flaskclient import FlaskClient
        DriverRegistry.register_driver("flask", FlaskClient)
    except ImportError as e:
        logger.debug("Flask client import failed: %s", str(e))

# Initialize drivers
_register_webdrivers()
_register_other_drivers()

def get_driver(
    driver: Type[DriverAPI],
    retry_count: int,
    config: Optional[Dict[str, Any]] = None,
    *args: Any,
    **kwargs: Any
) -> DriverAPI:
    """
    Try to instantiate the driver with retry mechanism.
    
    Args:
        driver: Driver class to instantiate
        retry_count: Number of retry attempts
        config: Optional configuration dictionary
        *args: Positional arguments for driver initialization
        **kwargs: Keyword arguments for driver initialization
    
    Returns:
        Instantiated driver
    
    Raises:
        Exception: Last caught exception if all retries fail
    """
    if retry_count < 1:
        raise ValueError("retry_count must be positive")
        
    last_error = None
    for attempt in range(retry_count):
        try:
            return driver(config=config, *args, **kwargs)
        except driver_exceptions as e:
            last_error = e
            logger.warning(
                "Driver instantiation failed (attempt %d/%d): %s",
                attempt + 1,
                retry_count,
                str(e)
            )
            
    if last_error:
        raise last_error
    raise RuntimeError("Unknown error during driver instantiation")

def Browser(
    driver_name: str = "firefox",
    retry_count: int = 3,
    config: Optional[Dict[str, Any]] = None,
    *args: Any,
    **kwargs: Any
) -> DriverAPI:
    """
    Get a new driver instance.
    
    Args:
        driver_name: Name of the driver to use
        retry_count: Number of times to try instantiating the driver
        config: Optional configuration dictionary
        *args: Additional positional arguments for the driver
        **kwargs: Additional keyword arguments for the driver
    
    Returns:
        Driver instance
    
    Raises:
        DriverNotFoundError: If the requested driver is not available
        ValueError: If retry_count is less than 1
    """
    if retry_count < 1:
        raise ValueError("retry_count must be positive")

    driver = DriverRegistry.get_driver(driver_name.lower())
    
    if driver is None:
        raise DriverNotFoundError(
            f"Driver '{driver_name}' is not available. "
            "Please ensure the required dependencies are installed."
        )
        
    return get_driver(driver, retry_count, config, *args, **kwargs)