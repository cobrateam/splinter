# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
def test_create_and_access_a_cookie(browser, app_url):
    """Should be able to create and access a cookie"""
    browser.visit(app_url)

    browser.cookies.add({"sha": "zam"})

    assert "zam" == browser.cookies["sha"]


def test_create_many_cookies_at_once_as_dict(browser, app_url):
    """Should be able to create many cookies at once as dict"""
    browser.visit(app_url)

    cookies = {"sha": "zam", "foo": "bar"}
    browser.cookies.add(cookies)

    assert "zam" == browser.cookies["sha"]
    assert "bar" == browser.cookies["foo"]


def test_create_some_cookies_and_delete_them_all(browser, app_url):
    """Should be able to delete all cookies"""
    browser.visit(app_url)

    browser.cookies.add({"whatever": "and ever"})
    browser.cookies.add({"anothercookie": "im bored"})
    browser.cookies.delete_all()

    assert {} == browser.cookies


def test_create_and_delete_a_cookie(browser, app_url):
    """Should be able to create and destroy a cookie"""
    browser.visit(app_url)

    browser.cookies.delete_all()
    browser.cookies.add({"cookie": "with milk"})
    browser.cookies.delete("cookie")

    assert {} == browser.cookies


def test_create_and_delete_many_cookies(browser, app_url):
    """Should be able to create and destroy many cookies"""
    browser.visit(app_url)

    browser.cookies.delete_all()
    browser.cookies.add({"acookie": "cooked"})
    browser.cookies.add({"anothercookie": "uncooked"})
    browser.cookies.add({"notacookie": "halfcooked"})
    browser.cookies.delete("acookie", "notacookie")

    assert "uncooked" == browser.cookies["anothercookie"]


def test_try_to_destroy_an_absent_cookie_and_nothing_happens(browser, app_url):
    browser.visit(app_url)

    browser.cookies.delete_all()
    browser.cookies.add({"foo": "bar"})
    browser.cookies.delete("mwahahahaha")

    assert {"foo": "bar"} == browser.cookies


def test_create_and_get_all_cookies(browser, app_url):
    """Should be able to create some cookies and retrieve them all"""
    browser.visit(app_url)

    browser.cookies.delete_all()
    browser.cookies.add({"taco": "shrimp"})
    browser.cookies.add({"lavar": "burton"})

    assert 2 == len(browser.cookies.all())

    browser.cookies.delete_all()

    assert {} == browser.cookies.all()


def test_create_and_use_contains(browser, app_url):
    """Should be able to create many cookies at once as dict"""
    browser.visit(app_url)

    cookies = {"sha": "zam"}
    browser.cookies.add(cookies)

    assert "sha" in browser.cookies
    assert "foo" not in browser.cookies
