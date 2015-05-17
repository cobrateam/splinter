# -*- coding: utf-8 -*-

# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import with_statement
import os.path
import re
import time
import sys

import lxml.html
from lxml.cssselect import CSSSelector
from splinter.cookie_manager import CookieManagerAPI
from splinter.driver import DriverAPI, ElementAPI
from splinter.element_list import ElementList
from splinter.exceptions import ElementDoesNotExist
from splinter.request_handler.status_code import StatusCode


class CookieManager(CookieManagerAPI):

    def __init__(self, browser_cookies):
        self._cookies = browser_cookies

    def add(self, cookies):
        if isinstance(cookies, list):
            for cookie in cookies:
                for key, value in cookie.items():
                    self._cookies.set_cookie('localhost', key, value)
                return
        for key, value in cookies.items():
            self._cookies.set_cookie('localhost', key, value)

    def delete(self, *cookies):
        if cookies:
            for cookie in cookies:
                try:
                    self._cookies.delete_cookie('localhost', cookie)
                except KeyError:
                    pass
        else:
            self._cookies.cookie_jar.clear()

    def all(self, verbose=False):
        cookies = {}
        for cookie in self._cookies.cookie_jar:
            cookies[cookie.name] = cookie.value
        return cookies

    def __getitem__(self, item):
        cookies = dict([(c.name, c) for c in self._cookies.cookie_jar])
        return cookies[item].value

    def __eq__(self, other_object):
        if isinstance(other_object, dict):
            cookies_dict = dict([(c.name, c.value)
                                 for c in self._cookies.cookie_jar])
            return cookies_dict == other_object


class FlaskClient(DriverAPI):

    driver_name = "flask"

    def __init__(self, app, user_agent=None, wait_time=2):
        self.wait_time = wait_time
        app.config['TESTING'] = True
        self._browser = app.test_client()
        self._history = []
        self._cookie_manager = CookieManager(self._browser)
        self._last_urls = []
        self._forms = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _post_load(self):
        self._forms = {}
        try:
            del self._html
        except AttributeError:
            pass
        self.status_code = StatusCode(self._response.status_code, '')

    def visit(self, url):
        self._url = url
        self._response = self._browser.get(url, follow_redirects=True)
        self._last_urls.append(url)
        self._post_load()

    def submit(self, form):
        method = form.attrib['method']
        func_method = getattr(self._browser, method.lower())
        action = form.attrib['action']
        if action.strip() != '.':
            url = os.path.join(self._url, form.attrib['action'])
        else:
            url = self._url
        self._url = url
        data = dict(((k, v) for k, v in form.fields.items() if v is not None))
        for key in form.inputs.keys():
            input = form.inputs[key]
            if getattr(input, 'type', '') == 'file' and key in data:
                data[key] = open(data[key], 'rb')
        self._response = func_method(url, data=data, follow_redirects=True)
        self._post_load()
        return self._response

    def back(self):
        self._last_urls.insert(0, self.url)
        self.visit(self._last_urls[1])

    def forward(self):
        try:
            self.visit(self._last_urls.pop())
        except IndexError:
            pass

    def reload(self):
        self.visit(self._url)

    def quit(self):
        pass

    @property
    def htmltree(self):
        try:
            return self._html
        except AttributeError:
            self._html = lxml.html.fromstring(self.html)
            return self._html

    @property
    def title(self):
        html = self.htmltree
        return html.xpath('//title')[0].text_content().strip()

    @property
    def html(self):
        return self._response.get_data(as_text=True)

    @property
    def url(self):
        return self._url

    def find_option_by_value(self, value):
        html = self.htmltree
        element = html.xpath('//option[@value="%s"]' % value)[0]
        control = FlaskClientControlElement(element.getparent(), self)
        return ElementList([FlaskClientOptionElement(element, control)], find_by="value", query=value)

    def find_option_by_text(self, text):
        html = self.htmltree
        element = html.xpath('//option[normalize-space(text())="%s"]' % text)[0]
        control = FlaskClientControlElement(element.getparent(), self)
        return ElementList([FlaskClientOptionElement(element, control)], find_by="text", query=text)

    def find_by_css(self, selector):
        xpath = CSSSelector(selector).path
        return self.find_by_xpath(xpath, original_find="css", original_selector=selector)

    def find_by_xpath(self, xpath, original_find=None, original_selector=None):
        html = self.htmltree

        elements = []

        for xpath_element in html.xpath(xpath):
            if self._element_is_link(xpath_element):
                return self._find_links_by_xpath(xpath)
            elif self._element_is_control(xpath_element):
                elements.append((FlaskClientControlElement, xpath_element))
            else:
                elements.append((FlaskClientElement, xpath_element))

        find_by = original_find or "xpath"
        query = original_selector or xpath

        return ElementList(
            [element_class(element, self) for element_class, element in elements],
            find_by=find_by, query=query)

    def find_by_tag(self, tag):
        return self.find_by_xpath('//%s' % tag, original_find="tag", original_selector=tag)

    def find_by_value(self, value):
        return self.find_by_xpath('//*[@value="%s"]' % value, original_find="value", original_selector=value)

    def find_by_text(self, text):
        return self.find_by_xpath('//*[text()="%s"]' % text,
                                  original_find="text", original_selector=text)

    def find_by_id(self, id_value):
        return self.find_by_xpath(
            '//*[@id="%s"][1]' % id_value, original_find="id", original_selector=id_value)

    def find_by_name(self, name):
        html = self.htmltree

        xpath = '//*[@name="%s"]' % name
        elements = []

        for xpath_element in html.xpath(xpath):
            elements.append(xpath_element)

        find_by = "name"
        query = xpath

        return ElementList(
            [FlaskClientControlElement(element, self) for element in elements],
            find_by=find_by, query=query)

    def find_link_by_text(self, text):
        return self._find_links_by_xpath("//a[text()='%s']" % text)

    def find_link_by_href(self, href):
        return self._find_links_by_xpath("//a[@href='%s']" % href)

    def find_link_by_partial_href(self, partial_href):
        return self._find_links_by_xpath("//a[contains(@href, '%s')]" % partial_href)

    def find_link_by_partial_text(self, partial_text):
        return self._find_links_by_xpath("//a[contains(normalize-space(.), '%s')]" % partial_text)

    def fill(self, name, value):
        self.find_by_name(name=name).first.fill(value)

    def fill_form(self, field_values):
        for name, value in field_values.items():
            element = self.find_by_name(name)
            control = element.first._control
            control_type = control.get('type')
            if control_type == 'checkbox':
                if value:
                    control.value = value  # control.options
                else:
                    control.value = []
            elif control_type == 'radio':
                control.value = value  # [option for option in control.options if option == value]
            elif control_type == 'select':
                control.value = [value]
            else:
                # text, textarea, password, tel
                control.value = value

    def choose(self, name, value):
        self.find_by_name(name).first._control.value = value

    def check(self, name):
        control = self.find_by_name(name).first._control
        control.value = ['checked']

    def uncheck(self, name):
        control = self.find_by_name(name).first._control
        control.value = []

    def attach_file(self, name, file_path):
        control = self.find_by_name(name).first._control
        control.value = file_path

    def _find_links_by_xpath(self, xpath):
        html = self.htmltree
        links = html.xpath(xpath)
        return ElementList(
            [FlaskClientLinkElement(link, self) for link in links], find_by="xpath", query=xpath)

    def select(self, name, value):
        self.find_by_name(name).first._control.value = value

    def is_text_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if self._is_text_present(text):
                return True
        return False

    def _is_text_present(self, text):
        try:
            body = self.find_by_tag('body').first
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
        return element.tag == 'a'

    def _element_is_control(self, element):
        return hasattr(element, 'type')

    @property
    def cookies(self):
        return self._cookie_manager


re_extract_inner_html = re.compile(r'^<[^<>]+>(.*)</[^<>]+>$')


class FlaskClientElement(ElementAPI):

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
        return self.find_by_xpath('//*[text()="%s"]' % text)

    def find_by_id(self, id):
        elements = self._element.cssselect('#%s' % id)
        return ElementList([self.__class__(element, self) for element in elements])

    @property
    def value(self):
        return self._element.text_content()

    @property
    def text(self):
        return self.value

    @property
    def outer_html(self):
        return lxml.html.tostring(self._element, encoding='unicode').strip()

    @property
    def html(self):
        return re_extract_inner_html.match(self.outer_html).group(1)

    def has_class(self, class_name):
        return len(self._element.find_class(class_name)) > 0


class FlaskClientLinkElement(FlaskClientElement):

    def __init__(self, element, parent):
        super(FlaskClientLinkElement, self).__init__(element, parent)
        self._browser = parent

    def __getitem__(self, attr):
        return super(FlaskClientLinkElement, self).__getitem__(attr)

    def click(self):
        return self._browser.visit(self["href"])


class FlaskClientControlElement(FlaskClientElement):

    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        return self._control.attrib[attr]

    @property
    def value(self):
        return self._control.value

    @property
    def checked(self):
        return bool(self._control.value)

    def click(self):
        parent_form = self._get_parent_form()
        return self.parent.submit(parent_form).data

    def fill(self, value):
        parent_form = self._get_parent_form()
        if sys.version_info[0] > 2:
            parent_form.fields[self['name']] = value
        else:
            parent_form.fields[self['name']] = value.decode('utf-8')

    def select(self, value):
        self._control.value = value

    def _get_parent_form(self):
        parent_form = next(self._control.iterancestors('form'))
        return self.parent._forms.setdefault(parent_form._name(), parent_form)


class FlaskClientOptionElement(FlaskClientElement):

    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        return self._control.attrib[attr]

    @property
    def text(self):
        return self._control.text

    @property
    def value(self):
        return self._control.attrib['value']

    @property
    def selected(self):
        return self.parent.value == self.value
