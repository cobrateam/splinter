#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import subprocess

from tempfile import TemporaryFile
from lxml.cssselect import CSSSelector
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.firefox import firefox_profile

from splinter.driver import DriverAPI, ElementAPI
from splinter.element_list import ElementList

import time

class BaseWebDriver(DriverAPI):
    old_popen = subprocess.Popen

    def __init__(self, wait_time=2):
        self.wait_time = wait_time

    def _patch_subprocess(self):
        loggers_to_silence = [
            'selenium.webdriver.firefox.utils',
            'selenium.webdriver.firefox.firefoxlauncher',
            'selenium.webdriver.firefox.firefox_profile',
            'selenium.webdriver.remote.utils',
            'selenium.webdriver.remote.remote_connection',
            'addons.xpi',
            'webdriver.ExtensionConnection',
        ]

        class MutedHandler(logging.Handler):
            def emit(self, record):
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

        # also patching firefox profile in order to NOT produce output
        firefox_profile.FirefoxProfile. \
            DEFAULT_PREFERENCES['extensions.logging.enabled'] = "false"

    def _unpatch_subprocess(self):
        # cleaning up the house
        subprocess.Popen = self.old_popen

    @property
    def title(self):
        return self.driver.title

    @property
    def html(self):
        return self.driver.get_page_source()

    @property
    def url(self):
        return self.driver.current_url

    def visit(self, url):
        self.driver.get(url)

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

    def is_element_not_present(self, finder, selector):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            if not finder(selector):
                return True
        return False

    def is_element_present_by_css_selector(self, css_selector, wait_time=None):
        return self.is_element_present(self.find_by_css_selector, css_selector, wait_time)

    def is_element_not_present_by_css_selector(self, css_selector):
        return self.is_element_not_present(self.find_by_css_selector, css_selector)

    def is_element_present_by_xpath(self, xpath, wait_time=None):
        return self.is_element_present(self.find_by_xpath, xpath, wait_time)

    def is_element_not_present_by_xpath(self, xpath):
        return self.is_element_not_present(self.find_by_xpath, xpath)

    def is_element_present_by_tag(self, tag, wait_time=None):
        return self.is_element_present(self.find_by_tag, tag, wait_time)

    def is_element_not_present_by_tag(self, tag):
        return self.is_element_present(self.find_by_tag, tag)

    def is_element_present_by_name(self, name, wait_time=None):
        return self.is_element_present(self.find_by_name, name, wait_time)

    def is_element_not_present_by_name(self, name):
        return self.is_element_not_present(self.find_by_name, name)

    def is_element_present_by_id(self, id, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            try:
                self.driver.find_element_by_id(id)
                return True
            except NoSuchElementException:
                pass
        return False

    def is_element_not_present_by_id(self, id):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                self.driver.find_element_by_id(id)
            except NoSuchElementException:
                return True
        return False

    def switch_to_frame(self, id):
        self.driver.switch_to_frame(id)

    def find_option_by_value(self, value):
        return self.find_by_xpath('//option[@value="%s"]' % value)

    def find_option_by_text(self, text):
        return self.find_by_xpath('//option[normalize-space(text())="%s"]' % text)

    def find_link_by_href(self, href):
        return self.find_by_xpath('//a[@href="%s"]' % href)

    def find_link_by_text(self, text):
        return ElementList([self.element_class(element) for element in self.driver.find_elements_by_link_text(text)])

    def find_by_css_selector(self, css_selector):
        selector = CSSSelector(css_selector)

        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            elements = self.driver.find_elements_by_xpath(selector.path)
            if elements:
                return ElementList([self.element_class(element) for element in elements])
        return ElementList([])

    def find_by_xpath(self, xpath):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            elements = self.driver.find_elements_by_xpath(xpath)
            if elements:
                return ElementList([self.element_class(element) for element in elements])
        return ElementList([])

    def find_by_name(self, name):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            elements = self.driver.find_elements_by_name(name)
            if elements:
                return ElementList([self.element_class(element) for element in elements])
        return ElementList([])

    def find_by_id(self, id):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                element = self.driver.find_element_by_id(id)
                return ElementList([self.element_class(element)])
            except NoSuchElementException:
                pass

        return ElementList([])

    def find_by_tag(self, tag):
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            elements = self.driver.find_elements_by_tag_name(tag)
            if elements:
                return ElementList([self.element_class(element) for element in elements])
        return ElementList([])

    def fill_in(self, name, value):
        field = self.find_by_name(name).first
        field.value = value

    fill = fill_in
    attach_file = fill

    def choose(self, name):
        field = self.find_by_name(name).first
        field.click()

    def check(self, name):
        field = self.find_by_name(name).first
        field.check()

    def uncheck(self, name):
        field = self.find_by_name(name).first
        field.uncheck()

    def select(self, name, value):
        self.find_by_xpath('//select[@name="%s"]/option[@value="%s"]' % (name, value)).first._element.select()

    def quit(self):
        self.driver.quit()


class WebDriverElement(ElementAPI):

    def __init__(self, element):
        self._element = element

    def _get_value(self):
        try:
            return self._element.value
        except WebDriverException:
            return self._element.text

    def _set_value(self, value):
        self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)

    @property
    def text(self):
        return self._element.text

    def click(self):
        self._element.click()

    def check(self):
        if not self.checked:
            self._element.toggle()

    def uncheck(self):
        if self.checked:
            self._element.toggle()

    @property
    def checked(self):
        return self._element.is_selected()

    selected = checked

    @property
    def visible(self):
        return self._element.is_displayed()

    def __getitem__(self, attr):
        return self._element.get_attribute(attr)
