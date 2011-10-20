import spynner
from splinter.driver.generic.driver import GenericDriver

class Spynner(GenericDriver):

    def __init__(self):
        self._browser = spynner.Browser()

    def visit(self, url):
        self._browser.load(url)

    def quit(self):
        self._browser.close()

    @property
    def html(self):
        return self._browser.html

    @property
    def url(self):
        return self._browser.url
