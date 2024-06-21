# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
def test_is_text_present(browser, app_url):
    "should verify if text is present"
    browser.visit(app_url)
    assert browser.is_text_present("Example Header")


def test_is_text_present_and_should_return_false(browser, app_url):
    "should verify if text is present and return false"
    browser.visit(app_url)
    assert not browser.is_text_present("Text that not exist")


def test_is_text_present_and_should_wait_time(browser, app_url):
    "should verify if text is present and wait for five seconds"
    browser.visit(app_url)
    browser.links.find_by_text("FOO").click()
    assert browser.is_text_present("BAR!", wait_time=20)


def test_is_text_not_present(browser, app_url):
    "should verify if text is not present"
    browser.visit(app_url)
    assert browser.is_text_not_present("Text that not exist")


def test_is_text_not_present_and_should_return_false(browser, app_url):
    "should verify if text is not present and return false"
    browser.visit(app_url)
    assert not browser.is_text_not_present("Example Header")


def test_is_text_not_present_and_should_wait_time(browser, app_url):
    "should verify if text is not present and wait for five seconds"
    browser.visit(app_url)
    browser.links.find_by_text("FOO").click()
    assert browser.is_text_not_present("another text", wait_time=20)


def test_is_text_present_no_body(browser, app_url):
    "should work properly (return false) even if there's no body"
    browser.visit(app_url + "no-body")
    assert not browser.is_text_present("No such text")


def test_is_text_not_present_no_body(browser, app_url):
    "returns true if there's no body"
    browser.visit(app_url + "no-body")
    assert browser.is_text_not_present("No such text")
