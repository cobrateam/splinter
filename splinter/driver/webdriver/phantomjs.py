from selenium.webdriver import PhantomJS, DesiredCapabilities
from splinter.driver.webdriver import (BaseWebDriver,
                                       WebDriverElement as BaseWebDriverElement)
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriverElement(BaseWebDriverElement):
    def mouse_out(self):
        raise NotImplementedError('Not supported by phantomjs webdriver.')

    def mouse_over(self):
        raise NotImplementedError('Not supported by phantomjs webdriver.')

    def right_click(self):
        raise NotImplementedError('Not supported by webdriver.')

    def double_click(self):
        raise NotImplementedError('Not supported by webdriver.')


class WebDriver(BaseWebDriver):
    driver_name = "PhantomJS"
    element_class = WebDriverElement

    def __init__(self, user_agent=None, load_images=True,
                 desired_capabilities=None, wait_time=2,
                 custom_headers={}, **kwargs):
        capabilities = DesiredCapabilities.PHANTOMJS.copy()
        if user_agent is not None:
            capabilities['phantomjs.page.settings.userAgent'] = user_agent
        capabilities['phantomjs.page.settings.loadImages'] = load_images
        if isinstance(custom_headers, dict):
            for name, value in custom_headers.items():
                capabilities['phantomjs.page.customHeaders.%s' % name] = value
        if desired_capabilities:
            capabilities.update(desired_capabilities)

        self.driver = PhantomJS(desired_capabilities=capabilities, **kwargs)

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)

    def get_alert(self):
        raise NotImplementedError('Currently not implemented by ghostdriver.')
