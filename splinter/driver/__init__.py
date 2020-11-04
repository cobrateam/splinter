# -*- coding: utf-8 -*-:

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
This module contains the basic API for splinter drivers and elements.
"""

from splinter.meta import InheritedDocs


class DriverAPI(InheritedDocs("_DriverAPI", (object,), {})):
    """
    Basic driver API class.
    """

    driver_name = None

    @property
    def title(self):
        """
        Title of current page.
        """
        raise NotImplementedError(
            "%s doesn't support access to the title." % self.driver_name
        )

    def __enter__(self):
        """
        Context manager to use the browser safely.
        """
        raise NotImplementedError(
            "%s doesn't support use by 'with' statement." % self.driver_name
        )

    def __exit__(self):
        """
        Context manager to use the browser safely.
        """
        raise NotImplementedError(
            "%s doesn't support use by 'with' statement." % self.driver_name
        )

    @property
    def html(self):
        """
        Source of current page.
        """
        raise NotImplementedError(
            "%s doesn't support access to the html." % self.driver_name
        )

    @property
    def url(self):
        """
        URL of current page.
        """
        raise NotImplementedError(
            "%s doesn't support access to the url." % self.driver_name
        )

    def visit(self, url):
        """
        Visits a given URL.

        The ``url`` parameter is a string.
        """
        raise NotImplementedError("%s doesn't visit any url." % self.driver_name)

    def new_tab(self, url):
        """
        Visits a given URL in a new tab.

        The ``url`` parameter is a string.
        """
        raise NotImplementedError("%s doesn't open a new tab." % self.driver_name)

    def back(self):
        """
        Back to the last URL in the browsing history.

        If there is no URL to back, this method does nothing.
        """
        raise NotImplementedError(
            "%s doesn't support moving back in history." % self.driver_name
        )

    def forward(self):
        """
        Forward to the next URL in the browsing history.

        If there is no URL to forward, this method does nothing.
        """
        raise NotImplementedError(
            "%s doesn't support moving forward in history." % self.driver_name
        )

    def reload(self):
        """
        Revisits the current URL
        """
        raise NotImplementedError(
            "%s doesn't support reloading the page." % self.driver_name
        )

    def get_alert(self):
        """
        Changes the context for working with alerts and prompts.

        For more details, check the :doc:`docs about iframes, alerts and prompts </iframes-and-alerts>`
        """
        raise NotImplementedError("%s doesn't support alerts." % self.driver_name)

    def get_iframe(self, name):
        """
        Changes the context for working with iframes.

        For more details, check the :doc:`docs about iframes, alerts and prompts </iframes-and-alerts>`
        """
        raise NotImplementedError("%s doesn't support frames." % self.driver_name)

    def execute_script(self, script, *args):
        """
        Executes a given JavaScript in the browser.

        e.g.: ::
            >>> browser.execute_script('document.getElementById("body").innerHTML = "<p>Hello world!</p>"')
        """
        raise NotImplementedError(
            "%s doesn't support execution of arbitrary JavaScript." % self.driver_name
        )

    def evaluate_script(self, script, *args):
        """
        Similar to :meth:`execute_script <DriverAPI.execute_script>` method.

        Executes javascript in the browser and returns the value of the expression.

        e.g.: ::
            >>> assert 4 == browser.evaluate_script('2 + 2')
        """
        raise NotImplementedError(
            "%s doesn't support evaluation of arbitrary JavaScript." % self.driver_name
        )

    def find_by_css(self, css_selector):
        """
        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`,
        using a CSS selector to query the current page content.
        """
        raise NotImplementedError(
            "%s doesn't support finding elements by css selector." % self.driver_name
        )

    def find_by_xpath(self, xpath):
        """
        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`,
        using a xpath selector to query the current page content.
        """
        raise NotImplementedError(
            "%s doesn't support finding elements by xpath selector." % self.driver_name
        )

    def find_by_name(self, name):
        """
        Finds elements in current page by their name.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`.
        """
        raise NotImplementedError(
            "%s doesn't support finding elements by name." % self.driver_name
        )

    def find_by_id(self, id):
        """
        Finds an element in current page by its id.

        Even when only one element is find, this method returns an instance of
        :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding elements by id." % self.driver_name
        )

    def find_by_value(self, value):
        """
        Finds elements in current page by their value.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding elements by value." % self.driver_name
        )

    def find_by_text(self, text):
        """
        Finds elements in current page by their text.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding elements by text." % self.driver_name
        )

    def find_by_tag(self, tag):
        """
        Find all elements of a given tag in current page.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding elements by tag." % self.driver_name
        )

    def find_link_by_href(self, href):
        """
        Find all elements of a given tag in current page.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding links by href." % self.driver_name
        )

    def find_link_by_partial_href(self, partial_href):
        """
        Find links by looking for a partial ``str`` in their href attribute.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding links by partial href." % self.driver_name
        )

    def find_link_by_text(self, text):
        """
        Find links querying for their text.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding links by text." % self.driver_name
        )

    def find_link_by_partial_text(self, partial_text):
        """
        Find links by looking for a partial ``str`` in their text.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding links by partial text." % self.driver_name
        )

    def find_option_by_value(self, value):
        """
        Finds ``<option>`` elements by their value.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding options by value." % self.driver_name
        )

    def find_option_by_text(self, text):
        """
        Finds ``<option>`` elements by their text.

        Returns an instance of :class:`ElementList <splinter.element_list.ElementList>`
        """
        raise NotImplementedError(
            "%s doesn't support finding options by text." % self.driver_name
        )

    def is_text_present(self, text, wait_time=None):
        """
        Searchs for ``text`` in the browser and wait the seconds specified in ``wait_time``.

        Returns True if finds a match for the ``text`` and False if not.
        """
        raise NotImplementedError(
            "%s doesn't support checking if some text is present in the html. "
            % self.driver_name
        )

    def type(self, name, value, slowly=False):
        """
        Types the ``value`` in the field identified by ``name``.

        It's useful to test javascript events like keyPress, keyUp, keyDown, etc.

        If ``slowly`` is True, this function returns an iterator which will type one character per iteration.
        """
        raise NotImplementedError(
            "%s doesn't support typing on fields by name." % self.driver_name
        )

    def fill(self, name, value):
        """
        Fill the field identified by ``name`` with the content specified by ``value``.
        """
        raise NotImplementedError(
            "%s doesn't support filling fields by name." % self.driver_name
        )

    def fill_form(self, field_values, form_id=None, name=None):
        """
        Fill the fields identified by ``name`` with the content specified by ``value`` in a dict.

        Currently, fill_form supports the following fields: text, password, textarea, checkbox,
        radio and select.

        Checkboxes should be specified as a boolean in the dict.

        Arguments:
            field_values (dict): Values for all the fields in the form, in the pattern of {field name: field value}
            form_id (str): Id of the form to fill. Can be used instead of name.
            name (str): Name of the form to fill.
            ignore_missing (bool): Ignore missing keys in the dict.
        """
        raise NotImplementedError(
            "%s doesn't support filling forms with a dict." % self.driver_name
        )

    def choose(self, name, value):
        """
        Chooses a value in a radio buttons group.

        Suppose you have the two radio buttons in a page, with the name ``gender`` and values 'F' and 'M'.
        If you use the ``choose`` method the following way:

            >>> browser.choose('gender', 'F')

        Then you're choosing the female gender.
        """
        raise NotImplementedError(
            "%s doesn't support choosing options." % self.driver_name
        )

    def check(self, name):
        """
        Checks a checkbox by its name.

        Example:

            >>> browser.check("agree-with-terms")

        If you call ``browser.check`` n times, the checkbox keeps checked, it never get unchecked.

        To unckech a checkbox, take a look in the :meth:`uncheck <DriverAPI.uncheck>` method.
        """
        raise NotImplementedError(
            "%s doesn't support checking elements." % self.driver_name
        )

    def uncheck(self, name):
        """
        Unchecks a checkbox by its name.

        Example:

            >>> browser.uncheck("send-me-emails")

        If you call ``brower.uncheck`` n times, the checkbox keeps unchecked, it never get checked.

        To check a checkbox, take a look in the :meth:`check <DriverAPI.check>` method.
        """
        raise NotImplementedError(
            "%s doesn't support unchecking elements." % self.driver_name
        )

    def select(self, name, value):
        """
        Selects an ``<option>`` element in an ``<select>`` element using the ``name`` of the ``<select>`` and
        the ``value`` of the ``<option>``.

        Example:

            >>> browser.select("state", "NY")
        """
        raise NotImplementedError(
            "%s doesn't support selecting options in 'select' element."
            % self.driver_name
        )

    def click_link_by_href(self, href):
        """
        Clicks in a link by its ``href`` attribute.
        """
        return self.find_link_by_href(href).first.click()

    def click_link_by_partial_href(self, partial_href):
        """
        Clicks in a link by looking for partial content of ``href`` attribute.
        """
        return self.find_link_by_partial_href(partial_href).first.click()

    def click_link_by_text(self, text):
        """
        Clicks in a link by its ``text``.
        """
        return self.find_link_by_text(text).first.click()

    def click_link_by_partial_text(self, partial_text):
        """
        Clicks in a link by partial content of its text.
        """
        return self.find_link_by_partial_text(partial_text).first.click()

    def click_link_by_id(self, id):
        """
        Clicks in a link by id.
        """
        return self.find_by_id(id).first.click()

    def quit(self):
        """
        Quits the browser, closing its windows (if it has one).

        After quit the browser, you can't use it anymore.
        """
        raise NotImplementedError("%s doesn't support quit" % self.driver_name)

    def is_element_present_by_css(self, css_selector, wait_time=None):
        """
        Verify if the element is present in the current page by css, and wait the specified
        time in ``wait_time``.

        Returns True if the element is present and False if is not present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is present by css"
            % self.driver_name
        )

    def is_element_not_present_by_css(self, css_selector, wait_time=None):
        """
        Verify if the element is not present in the current page by css, and wait the specified time
        in ``wait_time``.

        Returns True if the element is not present and False if is present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is not present by css"
            % self.driver_name
        )

    def is_element_present_by_xpath(self, xpath, wait_time=None):
        """
        Verify if the element is present in the current page by xpath, and wait the specified
        time in ``wait_time``.

        Returns True if the element is present and False if is not present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is present by xpath"
            % self.driver_name
        )

    def is_element_not_present_by_xpath(self, xpath, wait_time=None):
        """
        Verify if the element is not present in the current page by xpath,
        and wait the specified time in ``wait_time``.

        Returns True if the element is not present and False if is present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is not present by xpath"
            % self.driver_name
        )

    def is_element_present_by_tag(self, tag, wait_time=None):
        """
        Verify if the element is present in the current page by tag,
        and wait the specified time in ``wait_time``.

        Returns True if the element is present and False if is not present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is present by tag"
            % self.driver_name
        )

    def is_element_not_present_by_tag(self, tag, wait_time=None):
        """
        Verify if the element is not present in the current page by tag,
        and wait the specified time in ``wait_time``.

        Returns True if the element is not present and False if is present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is not present by tag"
            % self.driver_name
        )

    def is_element_present_by_name(self, name, wait_time=None):
        """
        Verify if the element is present in the current page by name,
        and wait the specified time in ``wait_time``.

        Returns True if the element is present and False if is not present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is present by name"
            % self.driver_name
        )

    def is_element_not_present_by_name(self, name, wait_time=None):
        """
        Verify if the element is not present in the current page by name,
        and wait the specified time in ``wait_time``.

        Returns True if the element is not present and False if is present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is not present by name"
            % self.driver_name
        )

    def is_element_present_by_value(self, value, wait_time=None):
        """
        Verify if the element is present in the current page by value,
        and wait the specified time in ``wait_time``.

        Returns True if the element is present and False if is not present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is present by value"
            % self.driver_name
        )

    def is_element_not_present_by_value(self, value, wait_time=None):
        """
        Verify if the element is not present in the current page by value,
        and wait the specified time in ``wait_time``.

        Returns True if the element is not present and False if is present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is not present by value"
            % self.driver_name
        )

    def is_element_present_by_text(self, text, wait_time=None):
        """
        Verify if the element is present in the current page by text,
        and wait the specified time in ``wait_time``.

        Returns True if the element is present and False if is not present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is present by text"
            % self.driver_name
        )

    def is_element_not_present_by_text(self, text, wait_time=None):
        """
        Verify if the element is not present in the current page by text,
        and wait the specified time in ``wait_time``.

        Returns True if the element is not present and False if is present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is not present by text"
            % self.driver_name
        )

    def is_element_present_by_id(self, id, wait_time=None):
        """
        Verify if the element is present in the current page by id,
        and wait the specified time in ``wait_time``.

        Returns True if the element is present and False if is not present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is present by id"
            % self.driver_name
        )

    def is_element_not_present_by_id(self, id, wait_time=None):
        """
        Verify if the element is present in the current page by id,
        and wait the specified time in ``wait_time``.

        Returns True if the element is not present and False if is present.
        """
        raise NotImplementedError(
            "%s doesn't support verifying if element is not present by id"
            % self.driver_name
        )

    def screenshot(self, name=None, suffix=None):
        """
        Takes a screenshot of the current page and saves it locally.
        """
        raise NotImplementedError(
            "%s doesn't support taking screenshots." % self.driver_name
        )

    @property
    def cookies(self):
        """
        A :class:`CookieManager <splinter.cookie_manager.CookieManagerAPI>` instance.

        For more details, check the :doc:`cookies manipulation section </cookies>`.
        """
        raise NotImplementedError(
            "%s doesn't support cookies manipulation" % self.driver_name
        )


class ElementAPI(InheritedDocs("_ElementAPI", (object,), {})):
    """
    Basic element API class.

    Any element in the page can be represented as an instance of ``ElementAPI``.

    Once you have an instance, you can easily access attributes like a ``dict``:

        >>> element = browser.find_by_id("link-logo").first
        >>> assert element['href'] == 'https://splinter.readthedocs.io'

    You can also interact with the instance using the methods and properties listed below.
    """

    def _get_value(self):
        raise NotImplementedError

    def _set_value(self, value):
        raise NotImplementedError

    #: Value of the element, usually a form element
    value = property(_get_value, _set_value)

    @property
    def text(self):
        """
        String of all of the text within the element.  HTML tags are stripped.
        """
        raise NotImplementedError

    def click(self):
        """
        Clicks in the element.
        """
        raise NotImplementedError

    def check(self):
        """
        Checks the element, if it's "checkable" (e.g.: a checkbox).

        If the element is already checked, this method does nothing. For unchecking
        elements, take a loot in the :meth:`uncheck <ElementAPI.uncheck>` method.
        """
        raise NotImplementedError

    def uncheck(self):
        """
        Unchecks the element, if it's "checkable" (e.g.: a checkbox).

        If the element is already unchecked, this method does nothing. For checking
        elements, take a loot in the :meth:`check <ElementAPI.check>` method.
        """
        raise NotImplementedError

    @property
    def checked(self):
        """
        Boolean property that says if the element is checked or not.

        Example:

            >>> element.check()
            >>> assert element.checked
            >>> element.uncheck()
            >>> assert not element.checked
        """
        raise NotImplementedError

    @property
    def visible(self):
        """
        Boolean property that says if the element is visible or hidden in the current page.
        """
        raise NotImplementedError

    def has_class(self, class_name):
        """
        Indicates whether the element has the given class.
        """
        raise NotImplementedError

    def mouse_over(self):
        """
        Puts the mouse over the element.
        """
        raise NotImplementedError

    def mouse_out(self):
        """
        Moves the mouse away from the element.
        """
        raise NotImplementedError

    def clear(self):
        """
        Reset the field value.
        """
        raise NotImplementedError

    def fill(self, value):
        """
        Fill the field with the content specified by ``value``.
        """
        raise NotImplementedError

    def type(self, value, slowly=False):
        """
        Types the ``value`` in the field.

        It's useful to test javascript events like keyPress, keyUp, keyDown, etc.

        If ``slowly`` is True, this function returns an iterator which will type one character per iteration.

        Also supports selenium.

        Example:
            >>> from selenium.webdriver.common.keys import Keys
            >>> ElementAPI.type(Keys.RETURN)

        """
        raise NotImplementedError

    def select(self, value, slowly=False):
        """
        Selects an ``<option>`` element in the element using the ``value`` of the ``<option>``.

        Example:

            >>> element.select("NY")
        """
        raise NotImplementedError

    def screenshot(self):
        """
        Take screenshot of the element.
        """
        raise NotImplementedError

    def __getitem__(self, attribute):
        raise NotImplementedError
