from splinter.driver import DriverAPI, ElementAPI
from zope.testbrowser.browser import Browser


class ZopeTestBrowser(DriverAPI):
    
    def __init__(self):
        self._browser = Browser()

    def visit(self, url):
        self._browser.open(url)
        
    def quit(self):
        pass
        
    @property
    def title(self):
        return self._browser.title
        
    @property
    def html(self):
        return self._browser.contents

    @property
    def url(self):
        return self._browser.url