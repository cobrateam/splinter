# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import tempfile
import time
import re
import sys
import os
from contextlib import contextmanager

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from splinter.driver import DriverAPI, ElementAPI
from splinter.element_list import ElementList
from splinter.utils import warn_deprecated
from splinter.request_handler.status_code import StatusCode


if sys.version_info[0] > 2:
    _meth_func = '__func__'
    _func_name = '__name__'
else:
    _meth_func = 'im_func'
    _func_name = 'func_name'


class switch_window:

    def __init__(self, browser, window_handle):
        self.browser = browser
        self.window_handle = window_handle

    def __enter__(self):
        self.current_window_handle = self.browser.driver.current_window_handle
        self.browser.driver.switch_to_window(self.window_handle)

    def __exit__(self, type, value, traceback):
        if self.current_window_handle in self.browser.driver.window_handles:
            self.browser.driver.switch_to_window(self.current_window_handle)


class Window(object):
    """ A class representing a browser window """
    def __init__(self, browser, name):
        self._browser = browser
        self.name = name

    @property
    def title(self):
        """ The title of this window """
        with switch_window(self._browser, self.name):
            return self._browser.title

    @property
    def url(self):
        """ The url of this window """
        with switch_window(self._browser, self.name):
            return self._browser.url

    @property
    def index(self):
        """ The index of this window in browser.windows """
        return self._browser.driver.window_handles.index(self.name)

    @property
    def prev(self):
        """ Return the previous window """
        prev_index = self.index - 1
        prev_handle = self._browser.driver.window_handles[prev_index]
        return Window(self._browser, prev_handle)

    @property
    def next(self):
        """ Return the next window """
        next_index = (self.index + 1) % len(self._browser.driver.window_handles)
        next_handle = self._browser.driver.window_handles[next_index]
        return Window(self._browser, next_handle)

    def is_current():
        doc = "Whether this window is currently the browser's active window."

        def fget(self):
            return self._browser.driver.current_window_handle == self.name

        def fset(self, value):
            if value is True:
                self._browser.driver.switch_to_window(self.name)
            else:
                raise TypeError("can only set to True")
        return locals()
    is_current = property(**is_current())

    def close(self):
        """ Close this window. If this window is active, switch to previous window """
        target = self.prev if (self.is_current and self.prev != self) else None

        with switch_window(self._browser, self.name):
            self._browser.driver.close()

        if target is not None:
            target.is_current = True

    def close_others(self):
        self.is_current = True
        for window in self._browser.windows:
            if window != self:
                window.close()

    def __eq__(self, other):
        return self._browser == other._browser and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "<Window %s: %s>" % (self.name, self.url)


class Windows(object):

    """ A class representing all open browser windows """

    def __init__(self, browser):
        self._browser = browser

    def __len__(self):
        return len(self._browser.driver.window_handles)

    def __getitem__(self, key):
        window_handles = self._browser.driver.window_handles
        try:
            return Window(self._browser, window_handles[key])
        except TypeError:
            if key not in window_handles:
                raise KeyError(key)
            return Window(self._browser, key)

    def current():
        doc = "The currently active window"

        def fget(self):
            current_handle = self._browser.driver.current_window_handle
            return Window(self._browser, current_handle) if current_handle else None

        def fset(self, value):
            self._browser.driver.switch_to_window(value.name)
        return locals()
    current = property(**current())

    def __repr__(self):
        return str([Window(self._browser, handle) for handle in self._browser.driver.window_handles])


class BaseWebDriver(DriverAPI):

    def __init__(self, wait_time=2):
        self.wait_time = wait_time
        self.status_code = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.quit()

    @property
    def title(self):
        return self.driver.title

    @property
    def html(self):
        return self.driver.page_source

    @property
    def url(self):
        return self.driver.current_url

    def visit(self, url):
        self.status_code = None
        self.driver.get(url)
        self.status_code = StatusCode(200, 'OK')

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def reload(self):
        self.driver.refresh()

    def execute_script(self, script):
        self.driver.execute_script(script)

    def evaluate_script(self, script):
        return self.driver.execute_script("return %s" % script)

    def is_element_visible(self, finder, selector, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if finder(selector) and finder(selector).visible:
                return True
        return False

    def is_element_not_visible(self, finder, selector, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            element = finder(selector)
            if not element or (element and not element.visible):
                return True
        return False

    def is_element_visible_by_css(self, css_selector, wait_time=None):
        return self.is_element_visible(self.find_by_css, css_selector, wait_time)

    def is_element_not_visible_by_css(self, css_selector, wait_time=None):
        return self.is_element_not_visible(self.find_by_css, css_selector, wait_time)

    def is_element_visible_by_xpath(self, xpath, wait_time=None):
        return self.is_element_visible(self.find_by_xpath, xpath, wait_time)

    def is_element_not_visible_by_xpath(self, xpath, wait_time=None):
        return self.is_element_not_visible(self.find_by_xpath, xpath, wait_time)

    def is_element_present(self, finder, selector, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if finder(selector):
                return True
        return False

    def is_element_not_present(self, finder, selector, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if not finder(selector):
                return True
        return False

    def is_element_present_by_css(self, css_selector, wait_time=None):
        return self.is_element_present(self.find_by_css, css_selector, wait_time)

    def is_element_not_present_by_css(self, css_selector, wait_time=None):
        return self.is_element_not_present(self.find_by_css, css_selector, wait_time)

    def is_element_present_by_xpath(self, xpath, wait_time=None):
        return self.is_element_present(self.find_by_xpath, xpath, wait_time)

    def is_element_not_present_by_xpath(self, xpath, wait_time=None):
        return self.is_element_not_present(self.find_by_xpath, xpath, wait_time)

    def is_element_present_by_tag(self, tag, wait_time=None):
        return self.is_element_present(self.find_by_tag, tag, wait_time)

    def is_element_not_present_by_tag(self, tag, wait_time=None):
        return self.is_element_not_present(self.find_by_tag, tag, wait_time)

    def is_element_present_by_name(self, name, wait_time=None):
        return self.is_element_present(self.find_by_name, name, wait_time)

    def is_element_not_present_by_name(self, name, wait_time=None):
        return self.is_element_not_present(self.find_by_name, name, wait_time)

    def is_element_present_by_value(self, value, wait_time=None):
        return self.is_element_present(self.find_by_value, value, wait_time)

    def is_element_not_present_by_value(self, value, wait_time=None):
        return self.is_element_not_present(self.find_by_value, value, wait_time)

    def is_element_present_by_text(self, text, wait_time=None):
        return self.is_element_present(self.find_by_text, text, wait_time)

    def is_element_not_present_by_text(self, text, wait_time=None):
        return self.is_element_not_present(self.find_by_text, text, wait_time)

    def is_element_present_by_id(self, id, wait_time=None):
        return self.is_element_present(self.find_by_id, id, wait_time)

    def is_element_not_present_by_id(self, id, wait_time=None):
        return self.is_element_not_present(self.find_by_id, id, wait_time)

    def get_alert(self):
        return AlertElement(self.driver.switch_to_alert())

    def is_text_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            try:
                self.driver.find_element_by_tag_name('body').text.index(text)
                return True
            except ValueError:
                pass
            except NoSuchElementException:
                # This exception will be thrown if the body tag isn't present
                # This has occasionally been observed. Assume that the
                # page isn't fully loaded yet
                pass
        return False

    def is_text_not_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            try:
                self.driver.find_element_by_tag_name('body').text.index(text)
            except ValueError:
                return True
            except NoSuchElementException:
                # This exception will be thrown if the body tag isn't present
                # This has occasionally been observed. Assume that the
                # page isn't fully loaded yet
                pass
        return False

    @contextmanager
    def get_iframe(self, id):
        self.driver.switch_to.frame(id)
        try:
            yield self
        finally:
            self.driver.switch_to.frame(None)

    def find_option_by_value(self, value):
        return self.find_by_xpath(
            '//option[@value="%s"]' % value, original_find="option by value", original_query=value)

    def find_option_by_text(self, text):
        return self.find_by_xpath(
            '//option[normalize-space(text())="%s"]' % text, original_find="option by text",
            original_query=text)

    def find_link_by_href(self, href):
        return self.find_by_xpath('//a[@href="%s"]' % href, original_find="link by href", original_query=href)

    def find_link_by_partial_href(self, partial_href):
        return self.find_by_xpath(
            '//a[contains(@href, "%s")]' % partial_href, original_find="link by partial href",
            original_query=partial_href)

    def find_link_by_partial_text(self, partial_text):
        return self.find_by_xpath(
            '//a[contains(normalize-space(.), "%s")]' % partial_text,
            original_find="link by partial text", original_query=partial_text)

    def find_link_by_text(self, text):
        return self.find_by_xpath(
            '//a[text()="%s"]' % text, original_find="link by text", original_query=text)

    def find_by(self, finder, selector, original_find=None, original_query=None):
        elements = None
        end_time = time.time() + self.wait_time

        func_name = getattr(getattr(finder, _meth_func), _func_name)
        find_by = original_find or func_name[func_name.rfind('_by_') + 4:]
        query = original_query or selector

        while time.time() < end_time:
            try:
                elements = finder(selector)
                if not isinstance(elements, list):
                    elements = [elements]
            except NoSuchElementException:
                pass

            if elements:
                return ElementList(
                    [self.element_class(element, self) for element in elements],
                    find_by=find_by, query=query)
        return ElementList([], find_by=find_by, query=query)

    def find_by_css(self, css_selector):
        return self.find_by(
            self.driver.find_elements_by_css_selector, css_selector, original_find='css',
            original_query=css_selector)

    def find_by_xpath(self, xpath, original_find=None, original_query=None):
        original_find = original_find or "xpath"
        original_query = original_query or xpath
        return self.find_by(
            self.driver.find_elements_by_xpath, xpath, original_find=original_find,
            original_query=original_query)

    def find_by_name(self, name):
        return self.find_by(self.driver.find_elements_by_name, name)

    def find_by_tag(self, tag):
        return self.find_by(self.driver.find_elements_by_tag_name, tag)

    def find_by_value(self, value):
        return self.find_by_xpath('//*[@value="%s"]' % value, original_find='value', original_query=value)

    def find_by_text(self, text):
        return self.find_by_xpath('//*[text()="%s"]' % text,
                                  original_find='text', original_query=text)

    def find_by_id(self, id):
        return self.find_by(self.driver.find_element_by_id, id)

    def fill(self, name, value):
        field = self.find_by_name(name).first
        field.value = value

    attach_file = fill

    def fill_form(self, field_values):
        for name, value in field_values.items():
            elements = self.find_by_name(name)
            element = elements.first
            if element['type'] in ['text', 'password', 'tel'] or element.tag_name == 'textarea':
                element.value = value
            elif element['type'] == 'checkbox':
                if value:
                    element.check()
                else:
                    element.uncheck()
            elif element['type'] == 'radio':
                for field in elements:
                    if field.value == value:
                        field.click()
            elif element._element.tag_name == 'select':
                element.find_by_value(value).first._element.click()
            else:
                element.value = value

    def type(self, name, value, slowly=False):
        element = self.find_by_name(name).first._element
        if slowly:
            return TypeIterator(element, value)
        element.send_keys(value)
        return value

    def choose(self, name, value):
        fields = self.find_by_name(name)
        for field in fields:
            if field.value == value:
                field.click()

    def check(self, name):
        self.find_by_name(name).first.check()

    def uncheck(self, name):
        self.find_by_name(name).first.uncheck()

    def screenshot(self, name=None, suffix='.png'):

        name = name or ''

        (fd, filename) = tempfile.mkstemp(prefix=name, suffix=suffix)
        # don't hold the file
        os.close(fd)

        self.driver.get_screenshot_as_file(filename)
        return filename

    def select(self, name, value):
        self.find_by_xpath('//select[@name="%s"]//option[@value="%s"]' % (name, value)).first._element.click()

    def select_by_text(self, name, text):
        self.find_by_xpath('//select[@name="%s"]/option[text()="%s"]' % (name, text)).first._element.click()

    def quit(self):
        self.driver.quit()

    @property
    def cookies(self):
        return self._cookie_manager

    @property
    def windows(self):
        return Windows(self)


class TypeIterator(object):

    def __init__(self, element, keys):
        self._element = element
        self._keys = keys

    def __iter__(self):
        for key in self._keys:
            self._element.send_keys(key)
            yield key


class WebDriverElement(ElementAPI):

    def __init__(self, element, parent):
        self._element = element
        self.parent = parent
        self.action_chains = ActionChains(parent.driver)

    def _get_value(self):
        return self['value'] or self._element.text

    def _set_value(self, value):
        if self._element.get_attribute('type') != 'file':
            self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)

    @property
    def text(self):
        return self._element.text

    @property
    def tag_name(self):
        return self._element.tag_name

    def clear(self):
        if self._element.get_attribute('type') in ['textarea', 'text', 'password', 'tel']:
            self._element.clear()

    def fill(self, value):
        self.value = value

    def select(self, value):
        self.find_by_xpath(
            '//select[@name="%s"]/option[@value="%s"]' % (self["name"], value))._element.click()

    def select_by_text(self, text):
        self.find_by_xpath('//select[@name="%s"]/option[text()="%s"]' % (self["name"], text))._element.click()

    def type(self, value, slowly=False):
        if slowly:
            return TypeIterator(self._element, value)

        self._element.send_keys(value)
        return value

    def click(self):
        self._element.click()

    def check(self):
        if not self.checked:
            self._element.click()

    def uncheck(self):
        if self.checked:
            self._element.click()

    @property
    def checked(self):
        return self._element.is_selected()

    selected = checked

    @property
    def visible(self):
        return self._element.is_displayed()

    @property
    def html(self):
        return self['innerHTML']

    @property
    def outer_html(self):
        return self['outerHTML']

    def find_by_css(self, selector, original_find=None, original_query=None):
        find_by = original_find or 'css'
        query = original_query or selector

        elements = self._element.find_elements_by_css_selector(selector)
        return ElementList(
            [self.__class__(element, self.parent) for element in elements], find_by=find_by, query=query)

    def find_by_xpath(self, selector, original_find=None, original_query=None):
        elements = ElementList(self._element.find_elements_by_xpath(selector))
        return ElementList(
            [self.__class__(element, self.parent) for element in elements], find_by='xpath', query=selector)

    def find_by_name(self, name):
        elements = ElementList(self._element.find_elements_by_name(name))
        return ElementList(
            [self.__class__(element, self.parent) for element in elements], find_by='name', query=name)

    def find_by_tag(self, tag):
        elements = ElementList(self._element.find_elements_by_tag_name(tag))
        return ElementList(
            [self.__class__(element, self.parent) for element in elements], find_by='tag', query=tag)

    def find_by_value(self, value):
        selector = '[value="%s"]' % value
        return self.find_by_css(selector, original_find='value', original_query=value)

    def find_by_text(self, text):
        selector = '//*[text()="%s"]' % text
        return self.find_by_xpath(selector, original_find='text', original_query=text)

    def find_by_id(self, id):
        elements = ElementList(self._element.find_elements_by_id(id))
        return ElementList(
            [self.__class__(element, self.parent) for element in elements], find_by='id', query=id)

    def has_class(self, class_name):
        return bool(re.search(r'(?:^|\s)' + re.escape(class_name) + r'(?:$|\s)', self['class']))

    def mouse_over(self):
        """
        Performs a mouse over the element.

        Currently works only on Chrome driver.
        """
        self.action_chains.move_to_element(self._element)
        self.action_chains.perform()

    def mouse_out(self):
        """
        Performs a mouse out the element.

        Currently works only on Chrome driver.
        """
        self.action_chains.move_by_offset(5000, 5000)
        self.action_chains.perform()

    mouseover = warn_deprecated(mouse_over, 'mouseover')

    def double_click(self):
        """
        Performs a double click in the element.

        Currently works only on Chrome driver.
        """
        self.action_chains.double_click(self._element)
        self.action_chains.perform()

    def right_click(self):
        """
        Performs a right click in the element.

        Currently works only on Chrome driver.
        """
        self.action_chains.context_click(self._element)
        self.action_chains.perform()

    def drag_and_drop(self, droppable):
        """
        Performs drag a element to another elmenet.

        Currently works only on Chrome driver.
        """
        self.action_chains.drag_and_drop(self._element, droppable._element)
        self.action_chains.perform()

    def __getitem__(self, attr):
        return self._element.get_attribute(attr)


class AlertElement(object):

    def __init__(self, alert):
        self._alert = alert
        self.text = alert.text

    def accept(self):
        self._alert.accept()

    def dismiss(self):
        self._alert.dismiss()

    def fill_with(self, text):
        self._alert.send_keys(text)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
