# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import re

from lxml.cssselect import CSSSelector
from zope.testbrowser.browser import Browser, ListControl, SubmitControl
from splinter.element_list import ElementList
from splinter.exceptions import ElementDoesNotExist
from splinter.driver import DriverAPI, ElementAPI
from splinter.driver.element_present import ElementPresentMixIn
from splinter.cookie_manager import CookieManagerAPI

import mimetypes
import lxml.html
import time


class CookieManager(CookieManagerAPI):
    def __init__(self, driver):
        self.driver = driver

    def add(self, cookies):
        if isinstance(cookies, list):
            for cookie in cookies:
                for key, value in cookie.items():
                    self.driver.cookies[key] = value
                return
        for key, value in cookies.items():
            self.driver.cookies[key] = value

    def delete(self, *cookies):
        if cookies:
            for cookie in cookies:
                try:
                    del self.driver.cookies[cookie]
                except KeyError:
                    pass
        else:
            self.driver.cookies.clearAll()

    def all(self, verbose=False):
        cookies = {}
        for key, value in self.driver.cookies.items():
            cookies[key] = value
        return cookies

    def __getitem__(self, item):
        return self.driver.cookies[item]

    def __contains__(self, key):
        return key in self.driver.cookies

    def __eq__(self, other_object):
        if isinstance(other_object, dict):
            return dict(self.driver.cookies) == other_object
        return False


class ZopeTestBrowser(ElementPresentMixIn, DriverAPI):

    driver_name = "zope.testbrowser"

    def __init__(self, wait_time=2):
        self.wait_time = wait_time
        self._browser = Browser()

        self._cookie_manager = CookieManager(self._browser)
        self._last_urls = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

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
    def htmltree(self):
        return lxml.html.fromstring(self.html.decode("utf-8"))

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
        html = self.htmltree
        element = html.xpath('//option[@value="%s"]' % value)[0]
        control = self._browser.getControl(element.text)
        return ElementList(
            [ZopeTestBrowserOptionElement(control, self)], find_by="value", query=value
        )

    def find_option_by_text(self, text):
        html = self.htmltree
        element = html.xpath('//option[normalize-space(text())="%s"]' % text)[0]
        control = self._browser.getControl(element.text)
        return ElementList(
            [ZopeTestBrowserOptionElement(control, self)], find_by="text", query=text
        )

    def find_by_css(self, selector):
        xpath = CSSSelector(selector).path
        return self.find_by_xpath(
            xpath, original_find="css", original_selector=selector
        )

    def get_control(self, xpath_element):
        return xpath_element

    def find_by_xpath(self, xpath, original_find=None, original_selector=None):
        html = self.htmltree

        elements = []

        for xpath_element in html.xpath(xpath):
            if self._element_is_link(xpath_element):
                return self._find_links_by_xpath(xpath)
            elif self._element_is_control(xpath_element) and xpath_element.name:
                return self.find_by_name(xpath_element.name)
            else:
                elements.append(self.get_control(xpath_element))

        find_by = original_find or "xpath"
        query = original_selector or xpath

        return ElementList(
            [ZopeTestBrowserElement(element, self) for element in elements],
            find_by=find_by,
            query=query,
        )

    def find_by_tag(self, tag):
        return self.find_by_xpath(
            "//%s" % tag, original_find="tag", original_selector=tag
        )

    def find_by_value(self, value):
        return self.find_by_xpath(
            '//*[@value="%s"]' % value, original_find="value", original_selector=value
        )

    def find_by_text(self, text):
        return self.find_by_xpath(
            '//*[text()="%s"]' % text, original_find="text", original_selector=text
        )

    def find_by_id(self, id_value):
        return self.find_by_xpath(
            '//*[@id="%s"][1]' % id_value,
            original_find="id",
            original_selector=id_value,
        )

    def find_by_name(self, name):
        elements = []
        index = 0

        while True:
            try:
                control = self._browser.getControl(name=name, index=index)
                elements.append(control)
                index += 1
            except LookupError:
                break
            except NotImplementedError:
                break
        return ElementList(
            [ZopeTestBrowserControlElement(element, self) for element in elements],
            find_by="name",
            query=name,
        )

    def find_link_by_text(self, text):
        return self._find_links_by_xpath("//a[text()='%s']" % text)

    def find_link_by_href(self, href):
        return self._find_links_by_xpath("//a[@href='%s']" % href)

    def find_link_by_partial_href(self, partial_href):
        return self._find_links_by_xpath("//a[contains(@href, '%s')]" % partial_href)

    def find_link_by_partial_text(self, partial_text):
        return self._find_links_by_xpath(
            "//a[contains(normalize-space(.), '%s')]" % partial_text
        )

    def fill(self, name, value):
        self.find_by_name(name=name).first._control.value = value

    def fill_form(self, field_values, form_id=None, name=None):
        form = self._browser
        if name or form_id:
            form = self._browser.getForm(name=name, id=form_id)

        for name, value in field_values.items():
            control = form.getControl(name=name)

            if control.type == "checkbox":
                if value:
                    control.value = control.options
                else:
                    control.value = []
            elif control.type == "radio":
                control.value = [
                    option for option in control.options if option == value
                ]
            elif control.type == "select":
                control.value = [value]
            else:
                control.value = value

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
        filename = file_path.split("/")[-1]
        control = self._browser.getControl(name=name)
        content_type, _ = mimetypes.guess_type(file_path)
        control.add_file(open(file_path), content_type, filename)

    def _find_links_by_xpath(self, xpath):
        html = self.htmltree
        links = html.xpath(xpath)
        return ElementList(
            [ZopeTestBrowserLinkElement(link, self) for link in links],
            find_by="xpath",
            query=xpath,
        )

    def select(self, name, value):
        self.find_by_name(name).first._control.value = [value]

    def is_text_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if self._is_text_present(text):
                return True
        return False

    def _is_text_present(self, text):
        try:
            body = self.find_by_tag("body").first
            return text in body.text
        except ElementDoesNotExist:
            # This exception will be thrown if the body tag isn't present
            # This has occasionally been observed. Assume that the
            # page isn't fully loaded yet
            return False

    def is_text_not_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if not self._is_text_present(text):
                return True
        return False

    def _element_is_link(self, element):
        return element.tag == "a"

    def _element_is_control(self, element):
        return hasattr(element, "type")

    @property
    def cookies(self):
        return self._cookie_manager


re_extract_inner_html = re.compile(r"^<[^<>]+>(.*)</[^<>]+>$")


class ZopeTestBrowserElement(ElementAPI):
    def __init__(self, element, parent):
        self._element = element
        self.parent = parent

    def __getitem__(self, attr):
        return self._element.attrib[attr]

    def find_by_css(self, selector):
        elements = self._element.cssselect(selector)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_xpath(self, selector):
        elements = self._element.xpath(selector)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_name(self, name):
        elements = self._element.cssselect('[name="%s"]' % name)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_tag(self, name):
        elements = self._element.cssselect(name)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_value(self, value):
        elements = self._element.cssselect('[value="%s"]' % value)
        return ElementList([self.__class__(element, self) for element in elements])

    def find_by_text(self, text):
        return self.find_by_xpath('.//*[text()="%s"]' % text)

    def find_by_id(self, id):
        elements = self._element.cssselect("#%s" % id)
        return ElementList([self.__class__(element, self) for element in elements])

    @property
    def value(self):
        return self._element.text_content()

    @property
    def text(self):
        return self.value

    @property
    def outer_html(self):
        return lxml.html.tostring(self._element, encoding="unicode").strip()

    @property
    def html(self):
        return re_extract_inner_html.match(self.outer_html).group(1)

    def has_class(self, class_name):
        return len(self._element.find_class(class_name)) > 0


class ZopeTestBrowserLinkElement(ZopeTestBrowserElement):
    def __init__(self, element, parent):
        super(ZopeTestBrowserLinkElement, self).__init__(element, parent)
        self._browser = parent._browser

    def __getitem__(self, attr):
        return super(ZopeTestBrowserLinkElement, self).__getitem__(attr)

    def click(self):
        return self._browser.open(self["href"])


class ZopeTestBrowserControlElement(ZopeTestBrowserElement):
    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        try:
            return getattr(self._control._control, attr)
        except AttributeError:
            return self._control._control.attrs[attr]

    @property
    def value(self):
        value = self._control.value
        if isinstance(self._control, ListControl) and len(value) == 1:
            return value[0]
        return value

    @property
    def checked(self):
        return bool(self._control.value)

    def click(self):
        return self._control.click()

    def fill(self, value):
        self._control.value = value

    def select(self, value):
        self._control.value = [value]


class ZopeTestBrowserOptionElement(ZopeTestBrowserElement):
    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        return getattr(self._control, attr)

    @property
    def text(self):
        return self._control.labels[0]

    @property
    def value(self):
        return self._control.optionValue

    @property
    def selected(self):
        return self._control.selected
