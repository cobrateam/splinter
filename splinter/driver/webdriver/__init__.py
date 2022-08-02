# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import io
import os
import re
import tempfile
import time
import warnings
from contextlib import contextmanager
from typing import Optional

from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    WebDriverException,
    StaleElementReferenceException,
    TimeoutException,
    MoveTargetOutOfBoundsException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # NOQA: N812
from selenium.webdriver.support.ui import WebDriverWait

from splinter.driver import DriverAPI, ElementAPI
from splinter.driver.find_links import FindLinks
from splinter.driver.xpath_utils import _concat_xpath_from_str
from splinter.element_list import ElementList
from splinter.driver.webdriver.cookie_manager import CookieManager
from splinter.exceptions import ElementDoesNotExist
from splinter.retry import _retry


# Patch contextmanager onto Selenium's Alert
def alert_enter(self):
    return self


def alert_exit(self, type, value, traceback):  # NOQA: A002
    pass


Alert.__enter__ = alert_enter
Alert.__exit__ = alert_exit
Alert.fill_with = Alert.send_keys


class switch_window:  # NOQA: N801
    def __init__(self, browser, window_handle):
        self.browser = browser
        self.window_handle = window_handle

    def __enter__(self):
        self.current_window_handle = self.browser.driver.current_window_handle
        self.browser.driver.switch_to.window(self.window_handle)

    def __exit__(self, type, value, traceback):  # NOQA: A002
        if self.current_window_handle in self.browser.driver.window_handles:
            self.browser.driver.switch_to.window(self.current_window_handle)


class Window:
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

    @property  # NOQA: A003
    def next(self):  # NOQA: A003
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
                self._browser.driver.switch_to.window(self.name)
            else:
                raise TypeError("can only set to True")

        return locals()

    is_current = property(**is_current())

    def new_tab(self, url):
        """ Open new tab in current window """
        if self._browser.driver.name == 'firefox':
            self._browser.driver.get('about:config')
            self._browser.driver.execute_script('document.getElementById("warningButton").click();')
            self._browser.driver.execute_script(
                """
                Components.classes['@mozilla.org/preferences-service;1']
                    .getService(Components.interfaces.nsIPrefBranch)
                    .setIntPref('browser.link.open_newwindow', 3);
                """)

        self._browser.driver.execute_script("window.open('%s', '_blank');" % url)

        if self._browser.driver.name == 'firefox':
            self._browser.driver.execute_script(
                """
                Components.classes['@mozilla.org/preferences-service;1']
                    .getService(Components.interfaces.nsIPrefBranch)
                    .setIntPref('browser.link.open_newwindow', 2);
                """)
            self._browser.driver.back()

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


class Windows:

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
            self._browser.driver.switch_to.window(value.name)

        return locals()

    current = property(**current())

    def __repr__(self):
        return str(
            [
                Window(self._browser, handle)
                for handle in self._browser.driver.window_handles
            ]
        )


def _find(self, finder, finder_kwargs=None):
    """Search for elements. Returns a list of results.

    Arguments:
        finder: The function to use for the element search.
        finder_kwargs: Keyword Arguments for the finder function.

    Returns:
        list

    """
    finder_kwargs = finder_kwargs or {}

    elements = None
    elem_list = []

    try:
        elements = finder(**finder_kwargs)
        if not isinstance(elements, list):
            elements = [elements]

    except (
        NoSuchElementException,
        StaleElementReferenceException,
    ):
        # This exception is sometimes thrown if the page changes
        # quickly
        pass

    if elements:
        elem_list = [self.element_class(element, self, finder_kwargs) for element in elements]

    return elem_list


def find_by(
    self,
    finder,
    finder_kwargs=None,
    original_find: str = None,
    original_query: str = None,
    wait_time: int = None,
):
    """Wrapper for finding elements.

    Must be attached to a class.

    Returns:
        ElementList

    """
    elem_list = []

    find_by = original_find or finder_kwargs['by']
    query = original_query or finder_kwargs.get('value')

    # Zero second wait time means only check once
    if wait_time == 0:
        elem_list = _find(self, finder, finder_kwargs)
    else:
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            elem_list = _find(self, finder, finder_kwargs)

            if elem_list:
                break

    return ElementList(elem_list, find_by=find_by, query=query)


class BaseWebDriver(DriverAPI):
    driver = None
    find_by = find_by

    def __init__(self, driver=None, wait_time=2):
        self.wait_time = wait_time

        self.links = FindLinks(self)

        self.driver = driver
        self._find_elements = self.driver.find_elements

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

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

    @property
    def status_code(self):
        raise NotImplementedError

    def visit(self, url):
        self.driver.get(url)

    def back(self):
        self.driver.back()

    def forward(self):
        self.driver.forward()

    def reload(self):
        self.driver.refresh()

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def evaluate_script(self, script, *args):
        return self.driver.execute_script("return %s" % script, *args)

    def is_element_visible_by_css(self, css_selector, wait_time=None):
        warnings.warn(
            f'browser.is_element_visible_by_css({css_selector}, {wait_time}) is deprecated.'
            f' Use browser.find_by_css({css_selector}).is_visible({wait_time}) instead.',
            FutureWarning,
        )
        return self.find_by_css(css_selector, wait_time).is_visible(wait_time)

    def is_element_not_visible_by_css(self, css_selector, wait_time=None):
        warnings.warn(
            f'browser.is_element_not_visible_by_css({css_selector}, {wait_time}) is deprecated.'
            f' Use browser.find_by_css({css_selector}).is_not_visible({wait_time}) instead.',
            FutureWarning,
        )
        return self.find_by_css(css_selector, wait_time).is_not_visible(wait_time)

    def is_element_visible_by_xpath(self, xpath, wait_time=None):
        warnings.warn(
            f'browser.is_element_visible_by_xpath({xpath}, {wait_time}) is deprecated.'
            f' Use browser.find_by_xpath({xpath}).is_visible({wait_time}) instead.',
            FutureWarning,
        )
        return self.find_by_xpath(xpath, wait_time).is_visible(wait_time)

    def is_element_not_visible_by_xpath(self, xpath, wait_time=None):
        warnings.warn(
            f'browser.is_element_not_visible_by_xpath({xpath}, {wait_time}) is deprecated.'
            f' Use browser.find_by_xpath({xpath}).is_not_visible({wait_time}) instead.',
            FutureWarning,
        )
        return self.find_by_xpath(xpath, wait_time).is_not_visible(wait_time)

    def is_element_present(self, finder, selector, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if finder(selector, wait_time=wait_time):
                return True
        return False

    def is_element_not_present(self, finder, selector, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if not finder(selector, wait_time=0):
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

    def is_element_present_by_id(self, id, wait_time=None):  # NOQA: A002
        return self.is_element_present(self.find_by_id, id, wait_time)

    def is_element_not_present_by_id(self, id, wait_time=None):  # NOQA: A002
        return self.is_element_not_present(self.find_by_id, id, wait_time)

    def get_alert(self, wait_time=None):
        wait_time = wait_time or self.wait_time

        try:
            alert = WebDriverWait(self.driver, wait_time).until(EC.alert_is_present())
            return alert
        except TimeoutException:
            return None

    def _is_text_present(self, text):
        try:
            self.find_by_tag("body").text.index(text)
            return True
        except (NoSuchElementException, StaleElementReferenceException, ValueError):
            # NoSuchElementException will be thrown if the body tag isn't present
            # Can occur if the page isn't fully loaded yet.
            # StaleElementReferenceException will be thrown if the page changes quickly
            pass
        return False

    def is_text_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if self._is_text_present(text):
                return True
        return False

    def is_text_not_present(self, text, wait_time=None):
        wait_time = wait_time or self.wait_time
        end_time = time.time() + wait_time

        while time.time() < end_time:
            if not self._is_text_present(text):
                return True
        return False

    @contextmanager
    def get_iframe(self, frame_reference):

        # If a WebDriverElement is provided, send the underlying element
        if isinstance(frame_reference, WebDriverElement):
            frame_reference = frame_reference._element

        self.driver.switch_to.frame(frame_reference)

        try:
            yield self
        finally:
            self.driver.switch_to.frame(None)

    def find_option_by_value(self, value):
        return self.find_by_xpath(
            '//option[@value="%s"]' % value,
            original_find="option by value",
            original_query=value,
        )

    def find_option_by_text(self, text):
        return self.find_by_xpath(
            '//option[normalize-space(text())="%s"]' % text,
            original_find="option by text",
            original_query=text,
        )

    def find_by_css(self, css_selector, wait_time=None):
        return self.find_by(
            self.driver.find_elements,
            finder_kwargs={'by': By.CSS_SELECTOR, 'value': css_selector},
            original_find="css",
            original_query=css_selector,
            wait_time=wait_time,
        )

    def find_by_xpath(self, xpath, original_find="xpath", original_query=None, wait_time=None):
        original_query = original_query or xpath
        return self.find_by(
            self.driver.find_elements,
            finder_kwargs={'by': By.XPATH, 'value': xpath},
            original_find=original_find,
            original_query=original_query,
            wait_time=wait_time,
        )

    def find_by_name(self, name, wait_time=None):
        return self.find_by(
            self.driver.find_elements,
            finder_kwargs={'by': By.NAME, 'value': name},
            original_find='name',
            wait_time=wait_time,
        )

    def find_by_tag(self, tag, wait_time=None):
        return self.find_by(
            self.driver.find_elements,
            finder_kwargs={'by': By.TAG_NAME, 'value': tag},
            original_find='tag_name',
            wait_time=wait_time,
        )

    def find_by_value(self, value, wait_time=None):
        elem = self.find_by_xpath(
            '//*[@value="{}"]'.format(value),
            original_find="value",
            original_query=value,
            wait_time=wait_time,
        )
        if elem:
            return elem
        return self.find_by_xpath('//*[.="%s"]' % value)

    def find_by_text(self, text=None, wait_time=None):
        xpath_str = _concat_xpath_from_str(text)
        return self.find_by_xpath(
            xpath_str,
            original_find="text",
            original_query=text,
            wait_time=wait_time,
        )

    def find_by_id(self, id, wait_time=None):  # NOQA: A002
        return self.find_by(
            self.driver.find_element,
            finder_kwargs={'by': By.ID, 'value': id},
            original_find='id',
            wait_time=wait_time,
        )

    def fill(self, name, value):
        field = self.find_by_name(name).first
        field.value = value

    attach_file = fill

    def fill_form(self, field_values, form_id=None, name=None, ignore_missing=False):
        form = None

        if name is not None:
            form = self.find_by_name(name)
        if form_id is not None:
            form = self.find_by_id(form_id)

        for name, value in field_values.items():
            try:
                if form:
                    elements = form.find_by_name(name)
                else:
                    elements = self.find_by_name(name)
                element = elements.first
                if (
                    element["type"] in ["text", "password", "tel"]
                    or element.tag_name == "textarea"
                ):
                    element.value = value
                elif element["type"] == "checkbox":
                    if value:
                        element.check()
                    else:
                        element.uncheck()
                elif element["type"] == "radio":
                    for field in elements:
                        if field.value == value:
                            field.click()
                elif element._element.tag_name == "select":
                    element.select(value)
                else:
                    element.value = value
            except ElementDoesNotExist as e:
                if not ignore_missing:
                    raise ElementDoesNotExist(e)

    def type(self, name, value, slowly=False):  # NOQA: A003
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

    def screenshot(self, name="", suffix=".png", full=False, unique_file=True):
        filename = '{}{}'.format(name, suffix)

        if unique_file:
            (fd, filename) = tempfile.mkstemp(prefix=name, suffix=suffix)
            # Don't hold the file
            os.close(fd)

        if full:
            ori_window_size = self.driver.get_window_size()
            self.full_screen()

        self.driver.get_screenshot_as_file(filename)

        if full:
            self.recover_screen(ori_window_size)

        return filename

    def html_snapshot(self, name="", suffix=".html", encoding='utf-8', unique_file=True):
        filename = '{}{}'.format(name, suffix)

        if unique_file:
            (fd, filename) = tempfile.mkstemp(prefix=name, suffix=suffix)
            # Don't hold the file
            os.close(fd)

        with io.open(filename, 'w', encoding=encoding) as f:
            f.write(self.html)

        return filename

    def select(self, name, value):
        self.find_by_xpath(
            '//select[@name="%s"]//option[@value="%s"]' % (name, value)
        ).first._element.click()

    def select_by_text(self, name, text):
        self.find_by_xpath(
            '//select[@name="%s"]/option[text()="%s"]' % (name, text)
        ).first._element.click()

    def quit(self):  # NOQA: A003
        try:
            self.driver.quit()
        except WebDriverException:
            pass

    def full_screen(self):
        width = self.driver.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth);")
        height = self.driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight);")
        self.driver.set_window_size(width, height)

    def recover_screen(self, size):
        width = size.get('width')
        height = size.get('height')
        self.driver.set_window_size(width, height)

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


class ShadowRootElement(ElementAPI):
    find_by = find_by

    def __init__(self, element, parent):
        self._element = element
        self.parent = parent

        self.driver = self.parent.driver
        self.wait_time = self.parent.wait_time
        self.element_class = self.parent.element_class

    def _find(self, by: By, selector, wait_time=None):
        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': by, 'value': selector},
            wait_time=wait_time,
        )

    def find_by_css(self, selector, wait_time=None):
        return self._find(By.CSS_SELECTOR, selector, wait_time)

    def find_by_id(self, selector, wait_time=None):
        return self._find(By.ID, selector, wait_time)

    def find_by_name(self, selector, wait_time=None):
        return self._find(By.NAME, selector, wait_time)

    def find_by_tag(self, selector, wait_time=None):
        return self._find(By.TAG_NAME, selector, wait_time)


class WebDriverElement(ElementAPI):
    find_by = find_by

    def __init__(self, element, parent, finder_kwargs):
        self._element = element
        self.parent = parent

        self._find_elements = self._element.find_elements
        self._finder_kwargs = finder_kwargs

        self.driver = self.parent.driver
        self.wait_time = self.parent.wait_time
        self.element_class = self.parent.element_class

        self.links = FindLinks(self)

    def _get_value(self):
        return self["value"] or self._element.text

    def _set_value(self, value):
        if self._element.get_attribute("type") != "file":
            self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)

    def __getitem__(self, attr):
        return self._element.get_attribute(attr)

    @property
    def text(self):
        return self._element.text

    @property
    def tag_name(self):
        return self._element.tag_name

    def clear(self):
        if self._element.get_attribute("type") in [
            "email",
            "number",
            "password",
            "search",
            "tel",
            "text",
            "textarea",
            "url",
        ]:
            self._element.clear()

    def fill(self, value):
        self.value = value

    def select(self, value=None, text=None):
        finder = None
        search_value = None

        if text:
            finder = 'text()'
            search_value = text
        elif value:
            finder = '@value'
            search_value = value

        self.find_by_xpath(
            './/option[{}="{}"]'.format(finder, search_value)
        )._element.click()

    def select_by_text(self, text):
        self.select(text=text)

    def type(self, value, slowly=False):  # NOQA: A003
        if slowly:
            return TypeIterator(self._element, value)

        self._element.send_keys(value)
        return value

    def click(self):
        """Click an element.

        If the element is not interactive due to being covered by another
         element, the click will retry for self.parent.wait_time amount of
         time.
        """
        end_time = time.time() + self.parent.wait_time
        error = None
        while time.time() < end_time:
            try:
                return self._element.click()
            except (
                ElementClickInterceptedException,
                WebDriverException,
            ) as e:
                error = e

        raise error

    def check(self):
        if not self.checked:
            self.click()

    def uncheck(self):
        if self.checked:
            self.click()

    @property
    def checked(self):
        return self._element.is_selected()

    selected = checked

    @property
    def visible(self):
        return self._element.is_displayed()

    @property
    def html(self):
        return self["innerHTML"]

    @property
    def outer_html(self):
        return self["outerHTML"]

    def _refresh_element(self, wait_time: Optional[int] = None):
        """Search for the element and update the internal reference.

        Returns:
            WebDriverElement

        Raises:
            ElementDoesNotExist
        """
        element_list = self.find_by(
            self.parent._find_elements,
            finder_kwargs=self._finder_kwargs,
            original_find=self._finder_kwargs['by'],
            wait_time=wait_time,
        )

        # Ensure the correct element is picked and replace old element
        for elem in element_list:
            new_element = elem._element

            if new_element == self._element:
                self._element = new_element
                return self

        raise ElementDoesNotExist("Element was removed from DOM.")

    def is_visible(self, wait_time=None):
        wait_time = wait_time or self.wait_time

        def search() -> bool:
            # Element is refreshed to account for changes to the page.
            self._refresh_element(wait_time=0)

            try:
                result = self.visible
            # StaleElementReferenceException occurs if element is found
            # but changes before visible is checked
            except StaleElementReferenceException:
                return False

            if result:
                return True

            return False

        return _retry(search, timeout=wait_time)

    def is_not_visible(self, wait_time=None):
        wait_time = wait_time or self.wait_time

        def search() -> bool:
            # Element is refreshed to account for changes to the page.
            self._refresh_element(wait_time=0)

            try:
                result = self.visible
            # StaleElementReferenceException occurs if element is found
            # but changes before visible is checked
            except StaleElementReferenceException:
                return False

            if result:
                return False

            return True

        return _retry(search, timeout=wait_time)

    def find_by_css(self, selector, wait_time=None):
        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': By.CSS_SELECTOR, 'value': selector},
            original_find="css",
            wait_time=wait_time,
        )

    def find_by_xpath(self, selector, wait_time=None, original_find="xpath", original_query=None):
        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': By.XPATH, 'value': selector},
            original_find=original_find,
            original_query=original_query,
            wait_time=wait_time,
        )

    def find_by_name(self, selector, wait_time=None):
        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': By.NAME, 'value': selector},
            original_find="name",
            wait_time=wait_time,
        )

    def find_by_tag(self, selector, wait_time=None):
        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': By.TAG_NAME, 'value': selector},
            original_find="tag",
            wait_time=wait_time,
        )

    def find_by_value(self, value, wait_time=None):
        selector = '[value="{}"]'.format(value)

        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': By.CSS_SELECTOR, 'value': selector},
            original_find="value",
            original_query=value,
            wait_time=wait_time,
        )

    def find_by_text(self, text, wait_time=None):
        # Add a period to the xpath to search only inside the parent.
        xpath_str = '.{}'.format(_concat_xpath_from_str(text))

        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': By.XPATH, 'value': xpath_str},
            original_find="text",
            original_query=text,
            wait_time=wait_time,
        )

    def find_by_id(self, selector, wait_time=None):
        return self.find_by(
            self._element.find_elements,
            finder_kwargs={'by': By.ID, 'value': selector},
            original_find="id",
            wait_time=wait_time,
        )

    def has_class(self, class_name):
        return bool(
            re.search(r"(?:^|\s)" + re.escape(class_name) + r"(?:$|\s)", self["class"])
        )

    def scroll_to(self):
        """Scroll to the current element."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", self._element)

    def mouse_over(self):
        """Perform a mouse over the element."""
        self.scroll_to()
        ActionChains(self.driver).move_to_element(self._element).perform()

    def mouse_out(self):
        """Perform a mouse out the element."""
        self.scroll_to()
        size = self._element.size

        try:
            # Fails on left edge of viewport
            ActionChains(self.driver).move_to_element_with_offset(
                self._element, -10, -10).click().perform()
        except MoveTargetOutOfBoundsException:
            try:
                ActionChains(self.driver).move_to_element_with_offset(
                    self._element, size['width'] + 10, 10).click().perform()
            except MoveTargetOutOfBoundsException:
                ActionChains(self.driver).move_to_element_with_offset(
                    self._element, 10, size['height'] + 10).click().perform()

    def double_click(self):
        """Perform a double click in the element."""
        self.scroll_to()
        ActionChains(self.driver).double_click(self._element).perform()

    def right_click(self):
        """Perform a right click in the element."""
        self.scroll_to()
        ActionChains(self.driver).context_click(self._element).perform()

    def drag_and_drop(self, droppable):
        """Drag an element to another element."""
        self.scroll_to()
        ActionChains(self.driver).drag_and_drop(self._element, droppable._element).perform()

    def _full_screen(self):
        width = self.driver.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth);")
        height = self.driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight);")
        self.driver.set_window_size(width, height)

    def screenshot(self, name='', suffix='.png', full=False, unique_file=True):

        filename = '{}{}'.format(name, suffix)

        if unique_file:
            (fd, filename) = tempfile.mkstemp(prefix=name, suffix=suffix)
            # don't hold the file
            os.close(fd)

        if full:
            ori_window_size = self.driver.get_window_size()
            self._full_screen()

        self._element.screenshot(filename)

        if full:
            # Restore screen size
            width = ori_window_size.get('width')
            height = ori_window_size.get('height')
            self.driver.set_window_size(width, height)

        return filename

    @property
    def shadow_root(self) -> ShadowRootElement:
        shadow_root = self._element.shadow_root
        return ShadowRootElement(shadow_root, self)
