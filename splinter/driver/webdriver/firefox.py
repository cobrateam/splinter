#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import subprocess

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from tempfile import TemporaryFile

class WebDriver(BaseWebDriver):
    old_popen = subprocess.Popen

    def __init__(self):
        firefox_profile = FirefoxProfile()
        firefox_profile.set_preference('extensions.logging.enabled', 'false')

        self._patch_subprocess()
        self.driver = Firefox(firefox_profile)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        super(WebDriver, self).__init__()

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

    def _unpatch_subprocess(self):
        # cleaning up the house
        subprocess.Popen = self.old_popen

