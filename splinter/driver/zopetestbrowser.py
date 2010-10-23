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

    def find_by_tag(self, tag):
        return self.find_by_xpath('//%s' % tag)

    def find_by_id(self, id_value):
        html = lxml.html.fromstring(self.html)
        return ZopeTestBrowserElement(html.get_element_by_id(id_value))

    def find_by_name(self, name):
        control = self._browser.getControl(name=name)
        return ZopeTestBrowserControlElement(control)

    def find_link_by_text(self, text):
        link = self._browser.getLink(text=text)
        return ZopeTestBrowserLinkElement(link)

    def find_link_by_href(self, href):
        link = self._browser.getLink(url=href)
        return ZopeTestBrowserLinkElement(link)

    def fill_in(self, name, value):
        self._browser.getControl(name=name).value = value


class ZopeTestBrowserElement(ElementAPI):
    
    def __init__(self, element):
        self._element = element

    @property
    def value(self):
        if hasattr(self._element, 'type') and self._element.type == 'text':
            return self._element.value
        return self._element.text


class ZopeTestBrowserLinkElement(ElementAPI):
    
    def __init__(self, link):
        self._link = link
    
    def __getitem__(self, attr):
        return self._link.attrs[attr]

class ZopeTestBrowserControlElement(ElementAPI):
    
    def __init__(self, control):
        self._control = control

    @property
    def value(self):
        return self._control.value

    def click(self):
        return self._control.click()