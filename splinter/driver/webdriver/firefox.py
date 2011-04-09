#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.webdriver import Firefox
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement

class WebDriver(BaseWebDriver):

    def __init__(self):
        self._patch_subprocess()
        self.driver = Firefox()
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        super(WebDriver, self).__init__()
