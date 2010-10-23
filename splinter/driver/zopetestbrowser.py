from splinter.driver import DriverAPI, ElementAPI
from zope.testbrowser.browser import Browser
import lxml.html


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
  
    def find_by_css_selector(self, selector):
        html = lxml.html.fromstring(self.html)
        return ZopeTestBrowserElement(html.cssselect(selector)[0])

    def find_by_xpath(self, xpath):
        html = lxml.html.fromstring(self.html)
        return ZopeTestBrowserElement(html.xpath(xpath)[0])


class ZopeTestBrowserElement(ElementAPI):
    
    def __init__(self, element):
        self._element = element

    @property
    def value(self):
        return self._element.text