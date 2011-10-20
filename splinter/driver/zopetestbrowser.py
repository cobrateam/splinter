import mimetypes

import lxml.html
from lxml.cssselect import CSSSelector
from zope.testbrowser.browser import Browser

from splinter.element_list import ElementList
from splinter.driver import DriverAPI, ElementAPI
from splinter.utils import warn_deprecated

class ZopeTestBrowser(DriverAPI):

    def __init__(self):
        self._browser = Browser()
        self._last_urls = []

    def visit(self, url):
        self._browser.open(url)

    def back(self):
        self._last_urls.insert(0, self.url)
        self._browser.goBack()

    def forward(self):
        try:
            self.visit(self._last_urls.pop())
        except IndexError:
            pass

    def reload(self):
        self._browser.reload()

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

    def find_option_by_value(self, value):
        html = lxml.html.fromstring(self.html)
        element = html.xpath('//option[@value="%s"]' % value)[0]
        control = self._browser.getControl(element.text)
        return ElementList([ZopeTestBrowserOptionElement(control, self)])

    def find_option_by_text(self, text):
        html = lxml.html.fromstring(self.html)
        element = html.xpath('//option[normalize-space(text())="%s"]' % text)[0]
        control = self._browser.getControl(element.text)
        return ElementList([ZopeTestBrowserOptionElement(control, self)])

    def find_by_css(self, selector):
        xpath = CSSSelector(selector).path
        return self.find_by_xpath(xpath)

    find_by_css_selector = warn_deprecated(find_by_css, 'find_by_css_selector')

    def find_by_xpath(self, xpath):
        html = lxml.html.fromstring(self.html)

        elements = []

        for xpath_element in html.xpath(xpath):
            if self._element_is_link(xpath_element):
                return self.find_link_by_text(xpath_element.text)
            elif self._element_is_control(xpath_element):
                return self.find_by_name(xpath_element.name)
            else:
                elements.append(xpath_element)

        return ElementList([ZopeTestBrowserElement(element, self) for element in elements])

    def find_by_tag(self, tag):
        return self.find_by_xpath('//%s' % tag)

    def find_by_id(self, id_value):
        return self.find_by_xpath('//*[@id="%s"][1]' % id_value)

    def find_by_name(self, name):
        elements = []
        index = 0

        while True:
            try:
                control = self._browser.getControl(name=name, index=index)
                elements.append(control)
                index += 1
            except IndexError:
                break
        return ElementList([ZopeTestBrowserControlElement(element, self) for element in elements])

    def find_link_by_text(self, text):
        return self._find_links_by_xpath("//a[text()='%s']" % text)

    def find_link_by_href(self, href):
        return self._find_links_by_xpath("//a[@href='%s']" % href)

    def fill(self, name, value):
        self.find_by_name(name=name).first._control.value = value

    fill_in = warn_deprecated(fill, 'fill_in')

    def choose(self, name, value):
        control = self._browser.getControl(name=name)
        control.value = [option for option in control.options if option == value]

    def check(self, name):
        control = self._browser.getControl(name=name)
        control.value = control.options

    def uncheck(self, name):
        control = self._browser.getControl(name=name)
        control.value = []

    def attach_file(self, name, file_path):
        control = self._browser.getControl(name=name)
        content_type, _ = mimetypes.guess_type(file_path)
        control.add_file(open(file_path), content_type, None)

    def _find_links_by_xpath(self, xpath):
        html = lxml.html.fromstring(self.html)
        links = html.xpath(xpath)
        return ElementList([ZopeTestBrowserLinkElement(link, self) for link in links])

    def select(self, name, value):
        self.find_by_name(name).first._control.value = [value,]

    def _element_is_link(self, element):
        return element.tag == 'a'

    def _element_is_control(self, element):
        return hasattr(element, 'type')

class ZopeTestBrowserElement(ElementAPI):

    def __init__(self, element, parent):
        self._element = element
        self.parent = parent

    def __getitem__(self, attr):
        return self._element.attrib[attr]

    @property
    def value(self):
        return self._element.text


class ZopeTestBrowserLinkElement(ZopeTestBrowserElement):

    def __init__(self, element, parent):
        super(ZopeTestBrowserLinkElement, self).__init__(element, parent)
        self._browser = parent._browser

    def __getitem__(self, attr):
        return super(ZopeTestBrowserLinkElement, self).__getitem__(attr)

    def __getattr__(self, attr):
        return getattr(self._element, attr)

    def click(self):
        return self._browser.open(self["href"])

class ZopeTestBrowserControlElement(ElementAPI):

    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

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

class ZopeTestBrowserOptionElement(ElementAPI):

    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        return self._control.mech_item.attrs[attr]

    @property
    def text(self):
        return self._control.mech_item.get_labels()[0]._text

    @property
    def value(self):
        return self._control.optionValue

    @property
    def selected(self):
        return self._control.mech_item._selected
