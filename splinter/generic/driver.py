import lxml.html
from lxml.cssselect import CSSSelector
from splinter.driver import DriverAPI
from splinter.element_list import ElementList
from splinter.generic.element import GenericElement, GenericLinkElement, GenericOptionElement


class GenericDriver(DriverAPI):
    def find_option_by_value(self, value):
        html = lxml.html.fromstring(self.html)
        element = html.xpath('//option[@value="%s"]' % value)[0]
        return ElementList([GenericOptionElement(element, self)])

    def find_option_by_text(self, text):
        html = lxml.html.fromstring(self.html)
        element = html.xpath('//option[normalize-space(text())="%s"]' % text)[0]
        return ElementList([GenericOptionElement(element, self)])

    def find_by_css(self, selector):
        xpath = CSSSelector(selector).path
        return self.find_by_xpath(xpath, original_find="css", original_selector=selector)

    find_by_css_selector = find_by_css

    def find_by_xpath(self, xpath, original_find=None, original_selector=None):
        html = lxml.html.fromstring(self.html)

        elements = []

        for xpath_element in html.xpath(xpath):
            if self._element_is_link(xpath_element):
                return self.find_link_by_text(xpath_element.text)
            elif self._element_is_control(xpath_element):
                return self.find_by_name(xpath_element.name)
            else:
                elements.append(xpath_element)

        find_by = original_find or "xpath"
        query = original_selector or xpath

        return ElementList([GenericElement(element, self) for element in elements])

    def find_by_tag(self, tag):
        return self.find_by_xpath('//%s' % tag, original_find="tag", original_selector=tag)

    def find_by_value(self, value):
        return self.find_by_xpath('//*[@value="%s"]' % value, original_find="value", original_selector=value)

    def find_by_id(self, id_value):
        return self.find_by_xpath('//*[@id="%s"][1]' % id_value, original_find="id", original_selector=id_value)

    def find_by_name(self, name):
        html = lxml.html.fromstring(self.html)

        elements = []
        for element in html.xpath('//*[@name="%s"]' % name):
            elements.append(element)
        return ElementList([GenericElement(element, self) for element in elements])

    def find_link_by_text(self, text):
        return self._find_links_by_xpath("//a[text()='%s']" % text)

    def find_link_by_href(self, href):
        return self._find_links_by_xpath("//a[@href='%s']" % href)

    def find_link_by_partial_href(self, partial_href):
        return self._find_links_by_xpath("//a[contains(@href, '%s')]" % partial_href)

    def find_link_by_partial_text(self, partial_text):
        return self._find_links_by_xpath("//a[contains(text(), '%s')]" % partial_text)

    def _find_links_by_xpath(self, xpath):
        html = lxml.html.fromstring(self.html)
        links = html.xpath(xpath)
        return ElementList([GenericLinkElement(link, self) for link in links])

    def _element_is_link(self, element):
        return element.tag == 'a'

    def _element_is_control(self, element):
        return hasattr(element, 'type')
