from splinter.driver import WebDriver

class Browser(object):

    def __init__(self):
        self._driver = WebDriver()

    def __getattr__(self, attr):
        return getattr(self._driver, attr)
