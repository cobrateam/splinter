# -*- coding: utf-8 -*-

# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os.path
import re
import time
import sys

import six

import lxml.etree
import lxml.html
from lxml.cssselect import CSSSelector
from splinter.driver import DriverAPI, ElementAPI
from splinter.driver.find_links import FindLinks
from splinter.driver.element_present import ElementPresentMixIn
from splinter.driver.xpath_utils import _concat_xpath_from_str
from splinter.element_list import ElementList
from splinter.exceptions import ElementDoesNotExist


class LxmlDriver(ElementPresentMixIn, DriverAPI):
    _response = ""
    _url = ""

    def __init__(self, user_agent=None, wait_time=2):
        self.wait_time = wait_time
        self._history = []
        self._last_urls = []
        self._forms = {}

        self.links = FindLinks(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _do_method(self, action, url, data=None):
        raise NotImplementedError(
            "%s doesn't support doing http methods." % self.driver_name
        )

    def visit(self, url):
        self._do_method("get", url)

    def serialize(self, form):
        data = {}

        for key in form.inputs.keys():
            input = form.inputs[key]
            if getattr(input, "type", "") == "submit":
                try:
                    form.remove(input)
                # Issue 595: throws ValueError: Element not child of this node
                except ValueError:
                    pass

        for k, v in form.fields.items():
            if v is None:
                continue

            if isinstance(v, lxml.html.MultipleSelectOptions):
                data[k] = list(v)
            else:
                data[k] = v

        for key in form.inputs.keys():
            input = form.inputs[key]
            if getattr(input, "type", "") == "file" and key in data:
                data[key] = open(data[key], "rb")

        return data

    def submit(self, form):
        method = form.attrib.get("method", "get").lower()
        action = form.attrib.get("action", "")
        if action.strip() != ".":
            url = os.path.join(self._url, action)
        else:
            url = self._url
        self._url = url
        data = self.serialize(form)

        self._do_method(method, url, data=data)
        return self._response

    def submit_data(self, form):
        raise NotImplementedError(
            "%s doesn't support submitting then getting the data." % self.driver_name
        )

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
        return html.xpath("//title")[0].text_content().strip()

    @property
    def html(self):
        raise NotImplementedError(
            "%s doesn't support getting the html of the response." % self.driver_name
        )

    @property
    def url(self):
        return self._url

    def find_option_by_value(self, value):
        html = self.htmltree
        element = html.xpath('//option[@value="%s"]' % value)[0]
        control = LxmlControlElement(element.getparent(), self)
        return ElementList(
            [LxmlOptionElement(element, control)], find_by="value", query=value
        )

    def find_option_by_text(self, text):
        html = self.htmltree
        element = html.xpath('//option[normalize-space(text())="%s"]' % text)[0]
        control = LxmlControlElement(element.getparent(), self)
        return ElementList(
            [LxmlOptionElement(element, control)], find_by="text", query=text
        )

    def find_by_css(self, selector):
        xpath = CSSSelector(selector).path
        return self.find_by_xpath(
            xpath, original_find="css", original_query=selector
        )

    def find_by_xpath(self, xpath, original_find=None, original_query=None):
        html = self.htmltree

        elements = []

        for xpath_element in html.xpath(xpath):
            if self._element_is_link(xpath_element):
                return self._find_links_by_xpath(xpath)
            elif self._element_is_control(xpath_element):
                elements.append((LxmlControlElement, xpath_element))
            else:
                elements.append((LxmlElement, xpath_element))

        find_by = original_find or "xpath"
        query = original_query or xpath

        return ElementList(
            [element_class(element, self) for element_class, element in elements],
            find_by=find_by,
            query=query,
        )

    def find_by_tag(self, tag):
        return self.find_by_xpath(
            "//%s" % tag, original_find="tag", original_query=tag
        )

    def find_by_value(self, value):
        elem = self.find_by_xpath(
            '//*[@value="%s"]' % value, original_find="value", original_query=value
        )
        if elem:
            return elem
        return self.find_by_xpath('//*[.="%s"]' % value)

    def find_by_text(self, text):
        xpath_str = _concat_xpath_from_str(text)
        return self.find_by_xpath(
            xpath_str,
            original_find="text",
            original_query=text,
        )

    def find_by_id(self, id_value):
        return self.find_by_xpath(
            '//*[@id="%s"][1]' % id_value,
            original_find="id",
            original_query=id_value,
        )

    def find_by_name(self, name):
        html = self.htmltree

        xpath = '//*[@name="%s"]' % name
        elements = []

        for xpath_element in html.xpath(xpath):
            elements.append(xpath_element)

        find_by = "name"
        query = xpath

        return ElementList(
            [LxmlControlElement(element, self) for element in elements],
            find_by=find_by,
            query=query,
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
        self.find_by_name(name=name).first.fill(value)

    def fill_form(self, field_values, form_id=None, name=None, ignore_missing=False):
        form = None

        if name is not None:
            form = self.find_by_name(name)
        if form_id is not None:
            form = self.find_by_id(form_id)

        for name, value in field_values.items():
            try:
                if form:
                    element = form.find_by_name(name)
                    control = element.first._element
                else:
                    element = self.find_by_name(name)
                    control = element.first._control
                control_type = control.get("type")
                if control_type == "checkbox":
                    if value:
                        control.value = value  # control.options
                    else:
                        control.value = []
                elif control_type == "radio":
                    control.value = (
                        value
                    )  # [option for option in control.options if option == value]
                elif control_type == "select":
                    if isinstance(value, list):
                        control.value = value
                    else:
                        control.value = [value]
                else:
                    # text, textarea, password, tel
                    control.value = value
            except ElementDoesNotExist as e:
                if not ignore_missing:
                    raise ElementDoesNotExist(e)

    def choose(self, name, value):
        self.find_by_name(name).first._control.value = value

    def check(self, name):
        control = self.find_by_name(name).first._control
        control.value = ["checked"]

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
            [LxmlLinkElement(link, self) for link in links],
            find_by="xpath",
            query=xpath,
        )

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
        return element.tag in ["button", "input", "textarea"]

    @property
    def cookies(self):
        return self._cookie_manager


class LxmlElement(ElementAPI):
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
        # Add a period to the xpath to search only inside the parent.
        xpath_str = '.{}'.format(_concat_xpath_from_str(text))
        return self.find_by_xpath(xpath_str)

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
        return re.match(r"^<[^<>]+>(.*)</[^<>]+>$", self.outer_html, re.MULTILINE | re.DOTALL).group(1)

    def has_class(self, class_name):
        return len(self._element.find_class(class_name)) > 0


class LxmlLinkElement(LxmlElement):
    def __init__(self, element, parent):
        super(LxmlLinkElement, self).__init__(element, parent)
        self._browser = parent

    def __getitem__(self, attr):
        return super(LxmlLinkElement, self).__getitem__(attr)

    def click(self):
        return self._browser.visit(self["href"])


class LxmlControlElement(LxmlElement):
    def __init__(self, control, parent):
        self._control = control
        self.parent = parent

    def __getitem__(self, attr):
        return self._control.attrib[attr]

    @property
    def value(self):
        try:
            return self._control.value
        except AttributeError:
            return self._control.text

    @property
    def checked(self):
        return bool(self._control.value)

    def click(self):
        parent_form = self._get_parent_form()

        if self._control.get("type") == "submit":
            name = self._control.get("name")

            if name:
                value = self._control.get("value", "")
                parent_form.append(
                    lxml.html.Element("input", name=name, value=value, type="hidden")
                )

        return self.parent.submit_data(parent_form)

    def fill(self, value):
        parent_form = self._get_parent_form()

        if not sys.version_info[0] > 2:
            if not isinstance(value, six.text_type):
                value = value.decode("utf-8")

        parent_form.fields[self["name"]] = value

    def select(self, value):
        self._control.value = value

    def _get_parent_form(self):
        parent_form = next(self._control.iterancestors("form"))
        return self.parent._forms.setdefault(parent_form._name(), parent_form)


class LxmlOptionElement(LxmlElement):
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
        return self._control.attrib["value"]

    @property
    def selected(self):
        return self.parent.value == self.value
