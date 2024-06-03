# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from .fake_webapp import EXAMPLE_APP


class IsTextPresentTest:
    def test_is_text_present(self):
        "should verify if text is present"
        assert self.browser.is_text_present("Example Header")

    def test_is_text_present_and_should_return_false(self):
        "should verify if text is present and return false"
        assert not self.browser.is_text_present("Text that not exist")

    def test_is_text_present_and_should_wait_time(self):
        "should verify if text is present and wait for five seconds"
        self.browser.links.find_by_text("FOO").click()
        assert self.browser.is_text_present("BAR!", wait_time=20)

    def test_is_text_not_present(self):
        "should verify if text is not present"
        assert self.browser.is_text_not_present("Text that not exist")

    def test_is_text_not_present_and_should_return_false(self):
        "should verify if text is not present and return false"
        assert not self.browser.is_text_not_present("Example Header")

    def test_is_text_not_present_and_should_wait_time(self):
        "should verify if text is not present and wait for five seconds"
        self.browser.links.find_by_text("FOO").click()
        assert self.browser.is_text_not_present("another text", wait_time=20)

    def test_is_text_present_no_body(self):
        "should work properly (return false) even if there's no body"
        self.browser.visit(EXAMPLE_APP + "no-body")
        assert not self.browser.is_text_present("No such text")

    def test_is_text_not_present_no_body(self):
        "returns true if there's no body"
        self.browser.visit(EXAMPLE_APP + "no-body")
        assert self.browser.is_text_not_present("No such text")
