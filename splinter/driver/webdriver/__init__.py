#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import subprocess
import time
from contextlib import contextmanager

from lxml.cssselect import CSSSelector
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from splinter.driver import DriverAPI, ElementAPI
from splinter.element_list import ElementList
from splinter.utils import warn_deprecated
from tempfile import TemporaryFile


class BaseWebDriver(DriverAPI):
    old_popen = subprocess.Popen

    def __init__(self, wait_time=2):
        self.wait_time = wait_time

    def _patch_subprocess(self):
        loggers_to_silence = [
            'selenium.webdriver.firefox.extension_connection',
            'selenium.webdriver.remote.remote_connection',
            'selenium.webdriver.remote.utils',
        ]

        class MutedHandler(logging.Handler):
            pass

        for name in loggers_to_silence:
            logger = logging.getLogger(name)
            logger.addHandler(MutedHandler())
            logger.setLevel(99999)

        # selenium is such a verbose guy let's make it open the
        # browser without showing all the meaningless output
        def MyPopen(*args, **kw):
            kw['stdout'] = TemporaryFile()
            kw['stderr'] = TemporaryFile()
            kw['close_fds'] = True
            return self.old_popen(*args, **kw)

        subprocess.Popen = MyPopen

    def _unpatch_subprocess(self):
        # cleaning up the house
        subprocess.Popen = self.old_popen

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
        self.connect(url)
        self.ensure_success_response()
        self.driver.get(url)

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
        return False

    def is_text_not_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            try:
                self.driver.find_element_by_tag_name('body').text.index(text)
            except ValueError:
                return True
        return False

    @contextmanager
    def get_iframe(self, id):
        self.driver.switch_to_frame(id)
        try:
            yield self
        finally:
            self.driver.switch_to_frame(None)

    def find_option_by_value(self, value):
        return self.find_by_xpath('//option[@value="%s"]' % value, original_find="option by value", original_query=value)

    def find_option_by_text(self, text):
        return self.find_by_xpath('//option[normalize-space(text())="%s"]' % text, original_find="option by text", original_query=text)

    def find_link_by_href(self, href):
        return self.find_by_xpath('//a[@href="%s"]' % href, original_find="link by href", original_query=href)

    def find_link_by_partial_href(self, partial_href):
        return self.find_by_xpath('//a[contains(@href, "%s")]' % partial_href, original_find="link by partial href", original_query=partial_href)

    def find_link_by_partial_text(self, partial_text):
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_partial_link_text(partial_text)], find_by="partial text", query=partial_text)

    def find_link_by_text(self, text):
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_link_text(text)], find_by="link by text", query=text)

    def find_by(self, finder, selector, original_find=None, original_query=None):
        elements = None
        end_time = time.time() + self.wait_time

        func_name = finder.im_func.func_name
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
                return ElementList([self.element_class(element, self) for element in elements], find_by=find_by, query=query)
        return ElementList([], find_by=find_by, query=query)

    def find_by_css(self, css_selector):
        selector = CSSSelector(css_selector)
        return self.find_by(self.driver.find_elements_by_xpath, selector.path, original_find='css', original_query=css_selector)

    def find_by_xpath(self, xpath, original_find=None, original_query=None):
        original_find = original_find or "xpath"
        original_query = original_query or xpath
        return self.find_by(self.driver.find_elements_by_xpath, xpath, original_find=original_find, original_query=original_query)

    def find_by_name(self, name):
        return self.find_by(self.driver.find_elements_by_name, name)

    def find_by_tag(self, tag):
        return self.find_by(self.driver.find_elements_by_tag_name, tag)

    def find_by_value(self, value):
        return self.find_by_xpath('//*[@value="%s"]' % value, original_find='value', original_query=value)

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
            if element['type'] == 'text':
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

    def type(self, name, value, slowly=False):
        element = self.driver.find_element_by_css_selector('input[name="%s"]' % name)
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
        field = self.find_by_name(name).first
        field.check()

    def uncheck(self, name):
        field = self.find_by_name(name).first
        field.uncheck()

    def select(self, name, value):
        element = self.find_by_xpath('//select[@name="%s"]/option[@value="%s"]' % (name, value)).first._element
        element.click()

    def quit(self):
        self.driver.quit()

    @property
    def cookies(self):
        return self._cookie_manager


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
        value = self["value"]
        if value:
            return value
        else:
            return self._element.text

    def _set_value(self, value):
        if  self._element.get_attribute('type') != 'file':
            self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)

    @property
    def text(self):
        return self._element.text

    def fill(self, value):
        self.value = value

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

    def find_by_css(self, selector, original_find=None, original_query=None):
        find_by = original_find or 'css'
        query = original_query or selector

        elements = self._element.find_elements_by_css_selector(selector)
        return ElementList([self.__class__(element, self.parent) for element in elements], find_by=find_by, query=query)

    def find_by_xpath(self, selector):
        elements = ElementList(self._element.find_elements_by_xpath(selector))
        return ElementList([self.__class__(element, self.parent) for element in elements], find_by='xpath', query=selector)

    def find_by_name(self, name):
        elements = ElementList(self._element.find_elements_by_name(name))
        return ElementList([self.__class__(element, self.parent) for element in elements], find_by='name', query=name)

    def find_by_tag(self, tag):
        elements = ElementList(self._element.find_elements_by_tag_name(tag))
        return ElementList([self.__class__(element, self.parent) for element in elements], find_by='tag', query=tag)

    def find_by_value(self, value):
        selector = '[value="%s"]' % value
        return self.find_by_css(selector, original_find='value', original_query=value)

    def find_by_id(self, id):
        elements = ElementList(self._element.find_elements_by_id(id))
        return ElementList([self.__class__(element, self.parent) for element in elements], find_by='id', query=id)

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
    mouseout = warn_deprecated(mouse_out, 'mouseout')

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
