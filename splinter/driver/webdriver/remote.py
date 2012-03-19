#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from selenium.webdriver import Remote
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement as BaseWebDriverElement
from splinter.cookie_manager import CookieManagerAPI


class WebDriver(BaseWebDriver):

    def __init__(self, server='localhost', port=4444):
        self.old_popen = subprocess.Popen

        self._patch_subprocess()
        dest = 'http://%s:%s/wd/hub' % (server, port)
        self.driver = Remote(dest, {})
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManagerAPI()

        super(WebDriver, self).__init__()


class WebDriverElement(BaseWebDriverElement):

    def mouse_over(self):
        """
        Remote Firefox doesn't support mouseover.
        """
        raise NotImplementedError("Remote Firefox doesn't support mouse over")

    def mouse_out(self):
        """
        Remote Firefox doesn't support mouseout.
        """
        raise NotImplementedError("Remote Firefox doesn't support mouseout")

    def double_click(self):
        """
        Remote Firefox doesn't support doubleclick.
        """
        raise NotImplementedError("Remote Firefox doesn't support doubleclick")

    def right_click(self):
        """
        Remote Firefox doesn't support right click'
        """
        raise NotImplementedError("Remote Firefox doesn't support right click")

    def drag_and_drop(self, droppable):
        """
        Remote Firefox doesn't support drag and drop
        """
        raise NotImplementedError("Remote Firefox doesn't support drag an drop")

    mouseover = mouse_over
    mouseout = mouse_out
