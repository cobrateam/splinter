# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

"""
This snippet show how to "test" a Facebook feature: the creation of an event.

It creates an event by going to http://www.facebook.com, login and navigate to "Create an event" page.
"""

import os
import unittest
import time
from splinter import Browser


class FacebookEventsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("firefox")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def do_login_if_need(self, username, password):
        if self.browser.is_element_present_by_css("div.menu_login_container"):
            self.browser.fill("email", username)
            self.browser.fill("pass", password)
            self.browser.find_by_css(
                'div.menu_login_container input[type="submit"]'
            ).first.click()
            assert self.browser.is_element_present_by_css("li#navAccount")

    def test_create_event(self):
        "Should be able to create an event"
        # Open home and login
        self.browser.visit("http://www.facebook.com")
        self.do_login_if_need(username="user", password="pass")

        # Go to events page
        self.browser.find_by_css("li#navItem_events a").first.click()

        # Click on "Create an event button"
        self.browser.find_by_css("div.uiHeaderTop a.uiButton").first.click()
        time.sleep(1)

        # Uploading the picture
        picture_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "img", "turtles.jpg"
        )
        self.browser.find_by_css("div.eventEditUpload a.uiButton").first.click()

        if not self.browser.is_element_present_by_css(
            "iframe#upload_pic_frame", wait_time=10
        ):
            self.fail("The upload pic iframe didn't appear :(")

        with self.browser.get_iframe("upload_pic_frame") as frame:
            frame.attach_file("pic", picture_path)
            time.sleep(10)

        # Filling the form
        self.browser.fill("event_startIntlDisplay", "5/21/2011")
        self.browser.select("start_time_min", "480")
        self.browser.fill("name", "Splinter sprint")
        self.browser.fill("location", "Rio de Janeiro, Brazil")
        self.browser.fill(
            "desc", "For more info, check out the #cobratem channel on freenode!"
        )

        self.browser.find_by_css('label.uiButton input[type="submit"]').first.click()
        time.sleep(1)

        # Checking if the event was created and we were redirect to its page
        title = self.browser.find_by_css("h1 span").first.text
        assert title == "Splinter sprint", title
