# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class CookiesTest(object):
    def test_create_and_access_a_cookie(self):
        """Should be able to create and access a cookie"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        browser.cookies.add({"sha": "zam"})

        assert "zam" == browser.cookies["sha"]

        browser.quit()

    def test_create_many_cookies_at_once_as_dict(self):
        """Should be able to create many cookies at once as dict"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        cookies = {"sha": "zam", "foo": "bar"}
        browser.cookies.add(cookies)

        assert "zam" == browser.cookies["sha"]
        assert "bar" == browser.cookies["foo"]

        browser.quit()

    def test_create_many_cookies_at_once_as_list(self):
        """Should be able to create many cookies at once as list"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        cookies = [{"sha": "zam"}, {"foo": "bar"}]
        browser.cookies.add(cookies)

        assert "zam" == browser.cookies["sha"]
        assert "bar" == browser.cookies["foo"]

        browser.quit()

    def test_create_some_cookies_and_delete_them_all(self):
        """Should be able to delete all cookies"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        browser.cookies.add({"whatever": "and ever"})
        browser.cookies.add({"anothercookie": "im bored"})
        browser.cookies.delete()

        assert {} == browser.cookies

        browser.quit()

    def test_create_and_delete_a_cookie(self):
        """Should be able to create and destroy a cookie"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        browser.cookies.delete()
        browser.cookies.add({"cookie": "with milk"})
        browser.cookies.delete("cookie")

        assert {} == browser.cookies

        browser.quit()

    def test_create_and_delete_many_cookies(self):
        """Should be able to create and destroy many cookies"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        browser.cookies.delete()
        browser.cookies.add({"acookie": "cooked"})
        browser.cookies.add({"anothercookie": "uncooked"})
        browser.cookies.add({"notacookie": "halfcooked"})
        browser.cookies.delete("acookie", "notacookie")

        assert "uncooked" == browser.cookies["anothercookie"]

        browser.quit()

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        browser.cookies.delete()
        browser.cookies.add({"foo": "bar"})
        browser.cookies.delete("mwahahahaha")

        {"foo": "bar"} == browser.cookies

        browser.quit()

    def test_create_and_get_all_cookies(self):
        """Should be able to create some cookies and retrieve them all"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        browser.cookies.delete()
        browser.cookies.add({"taco": "shrimp"})
        browser.cookies.add({"lavar": "burton"})

        assert 2 == len(browser.cookies.all())

        browser.cookies.delete()

        assert {} == browser.cookies.all()

        browser.quit()

    def test_create_and_use_contains(self):
        """Should be able to create many cookies at once as dict"""
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)

        cookies = {"sha": "zam"}
        browser.cookies.add(cookies)

        assert "sha" in browser.cookies
        assert "foo" not in browser.cookies

        browser.quit()
