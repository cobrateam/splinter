#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import subprocess
from contextlib import contextmanager

from tempfile import TemporaryFile
from lxml.cssselect import CSSSelector
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.firefox import firefox_profile

from splinter.driver import DriverAPI, ElementAPI
from splinter.element_list import ElementList
from splinter.utils import warn_deprecated


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

    is_element_present_by_css_selector = warn_deprecated(is_element_present_by_css, 'is_element_present_by_css_selector')

    def is_element_not_present_by_css(self, css_selector, wait_time=None):
        return self.is_element_not_present(self.find_by_css, css_selector, wait_time)

    is_element_not_present_by_css_selector = warn_deprecated(is_element_not_present_by_css, 'is_element_not_present_by_css_selector')

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
        return self.find_by_xpath('//option[@value="%s"]' % value)

    def find_option_by_text(self, text):
        return self.find_by_xpath('//option[normalize-space(text())="%s"]' % text)

    def find_link_by_href(self, href):
        return self.find_by_xpath('//a[@href="%s"]' % href)

    def find_link_by_text(self, text):
        return ElementList([self.element_class(element, self) for element in self.driver.find_elements_by_link_text(text)])

    def find_by(self, finder, selector):
        elements = None
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                elements = finder(selector)
                if not isinstance(elements, list):
                    elements = [elements]
            except NoSuchElementException:
                pass

            if elements:
                return ElementList([self.element_class(element, self) for element in elements])
        return ElementList([])

    def find_by_css(self, css_selector):
        selector = CSSSelector(css_selector)
        return self.find_by(self.driver.find_elements_by_xpath, selector.path)

    find_by_css_selector = warn_deprecated(find_by_css, 'find_by_css_selector')

    def find_by_xpath(self, xpath):
        return self.find_by(self.driver.find_elements_by_xpath, xpath)

    def find_by_name(self, name):
        return self.find_by(self.driver.find_elements_by_name, name)

    def find_by_tag(self, tag):
        return self.find_by(self.driver.find_elements_by_tag_name, tag)

    def find_by_id(self, id):
        return self.find_by(self.driver.find_element_by_id, id)

    def fill(self, name, value):
        field = self.find_by_name(name).first
        field.value = value

    fill_in = warn_deprecated(fill, 'fill_in')
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

    def __init__(self, element, parent):
        self._element = element
        self.parent = parent

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
