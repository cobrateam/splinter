from splinter.driver import DriverAPI, ElementAPI
from zope.testbrowser.browser import Browser
from splinter.finder import QueryElements
from lxml.cssselect import CSSSelector
import lxml.html
import mimetypes


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
        xpath = CSSSelector(selector).path
        return self.find_by_xpath(xpath)

    def find_by_xpath(self, xpath):
        html = lxml.html.fromstring(self.html)
        element = html.xpath(xpath)[0]
        if self._element_is_link(element):
            return self.find_link_by_text(element.text)
        if self._element_is_control(element):
            return self.find_by_name(element.name)
        return QueryElements([ZopeTestBrowserElement(element)])

    def find_by_tag(self, tag):
        return self.find_by_xpath('//%s' % tag)

    def find_by_id(self, id_value):
        return self.find_by_xpath('//*[@id="%s"]' % id_value)

    def find_by_name(self, name):
        control = self._browser.getControl(name=name)
        return QueryElements([ZopeTestBrowserControlElement(control)])

    def find_link_by_text(self, text):
        link = self._browser.getLink(text=text)
        return QueryElements([ZopeTestBrowserLinkElement(link)])

    def find_link_by_href(self, href):
        link = self._browser.getLink(url=href)
        return QueryElements([ZopeTestBrowserLinkElement(link)])

    def fill_in(self, name, value):
        self._browser.getControl(name=name).value = value

    def choose(self, name):
        control = self._browser.getControl(name=name)
        control.value = control.options
    
    check = choose

    def uncheck(self, name):
        control = self._browser.getControl(name=name)
        control.value = []

    def attach_file(self, name, file_path):
        control = self._browser.getControl(name=name)
        content_type, _ = mimetypes.guess_type(file_path)
        control.add_file(open(file_path), content_type, None)

    def _element_is_link(self, element):
        return element.tag == 'a'

    def _element_is_control(self, element):
        return hasattr(element, 'type')


class ZopeTestBrowserElement(ElementAPI):
    
    def __init__(self, element):
        self._element = element

    def __getitem__(self, attr):
        return self._element.attrib[attr]

    @property
    def value(self):
        return self._element.text


class ZopeTestBrowserLinkElement(ElementAPI):
    
    def __init__(self, link):
        self._link = link
    
    def __getitem__(self, attr):
        return self._link.attrs[attr]
    
    @property
    def value(self):
        return self._link.text

    def click(self):
        return self._link.click()


class ZopeTestBrowserControlElement(ElementAPI):
    
    def __init__(self, control):
        self._control = control

    def __getitem__(self, attr):
        return self._control.mech_control.attrs[attr]

    @property
    def value(self):
        return self._control.value
    
    @property
    def checked(self):
        return bool(self._control.value)

    def click(self):
        return self._control.click()
