from selenium.webdriver import Remote

"""The following functions prepare Webdriver for use.

Config, Options, Service, and other arguments are configured and sent to
the driver.

The driver is returned.
"""


def _setup_chrome(driver_class, config=None, options=None, service=None, **kwargs):
    """
    Returns: selenium.webdriver.Chrome || selenium.webdriver.Remote
    """
    if config.user_agent is not None:
        options.add_argument(f"--user-agent={config.user_agent}")

    if config.incognito:
        options.add_argument("--incognito")

    if config.fullscreen:
        options.add_argument("--kiosk")

    if config.headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    if config.extensions:
        for extension in config.extensions:
            options.add_extension(extension)

    if driver_class == Remote:
        rv = driver_class(options=options, **kwargs)
    else:
        rv = driver_class(options=options, service=service, **kwargs)

    return rv


def _setup_edge(driver_class, config=None, options=None, service=None, **kwargs):
    """
    Returns: selenium.webdriver.Edge || selenium.webdriver.Remote
    """
    if config.user_agent is not None:
        options.add_argument(f"--user-agent={config.user_agent}")

    if config.incognito:
        options.add_argument("--incognito")

    if config.fullscreen:
        options.add_argument("--kiosk")

    if config.headless:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    if config.extensions:
        for extension in config.extensions:
            options.add_extension(extension)

    if driver_class == Remote:
        rv = driver_class(options=options, **kwargs)
    else:
        rv = driver_class(options=options, service=service, **kwargs)

    return rv


def _setup_firefox(driver_class, config=None, options=None, service=None, **kwargs):
    """
    Returns: selenium.webdriver.Firefox || selenium.webdriver.Remote
    """
    if config.user_agent is not None:
        options.set_preference("general.useragent.override", config.user_agent)

    if config.headless:
        options.add_argument("--headless")

    if config.incognito:
        options.add_argument("-private")

    if driver_class == Remote:
        rv = driver_class(options=options, **kwargs)
    else:
        rv = driver_class(options=options, service=service, **kwargs)

    if config.extensions:
        for extension in config.extensions:
            rv.install_addon(extension)

    if config.fullscreen:
        rv.fullscreen_window()

    return rv


def _setup_safari(driver_class, config=None, options=None, service=None, **kwargs):
    """
    Returns: selenium.webdriver.Safari || selenium.webdriver.Remote
    """
    if driver_class == Remote:
        rv = driver_class(options=options, **kwargs)
    else:
        rv = driver_class(options=options, service=service, **kwargs)

    return rv
