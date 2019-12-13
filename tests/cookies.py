# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import time


class CookiesTest(object):
    def test_create_and_access_a_cookie(self):
        """should be able to create and access a cookie"""
        self.browser.cookies.add("sha", "zam")
        assert 'zam' == self.browser.cookies["sha"]["value"]

    def test_create_some_cookies_and_delete_them_all(self):
        """should be able to delete all cookies"""
        self.browser.cookies.add("whatever", "and ever")
        self.browser.cookies.add("anothercookie", "im bored")
        self.browser.cookies.delete()
        self.assertEqual(self.browser.cookies, {})

    def test_create_and_delete_a_cookie(self):
        """should be able to create and destroy a cookie"""
        self.browser.cookies.delete()
        self.browser.cookies.add("cookie", "with milk")
        self.browser.cookies.delete("cookie")
        self.assertEqual(self.browser.cookies, {})

    def test_create_and_delete_many_cookies(self):
        """should be able to create and destroy many cookies"""
        self.browser.cookies.delete()
        self.browser.cookies.add("acookie", "cooked")
        self.browser.cookies.add("anothercookie", "uncooked")
        self.browser.cookies.add("notacookie", "halfcooked")
        self.browser.cookies.delete("acookie", "notacookie")
        assert 'uncooked' == self.browser.cookies["anothercookie"]["value"]

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        self.browser.cookies.delete()
        self.browser.cookies.add("foo", "bar")
        self.browser.cookies.delete("mwahahahaha")
        self.assertEqual(self.browser.cookies, {"foo": "bar"})

    def test_create_and_get_all_cookies(self):
        """should be able to create some cookies and retrieve them all"""
        self.browser.cookies.delete()
        self.browser.cookies.add("taco", "shrimp")
        self.browser.cookies.add("lavar", "burton")
        self.assertEqual(len(self.browser.cookies.all()), 2)
        self.browser.cookies.delete()
        self.assertEqual(self.browser.cookies.all(), {})

    def test_create_and_use_contains(self):
        """should be able to create many cookies at once as dict"""
        self.browser.cookies.add('sha', 'zam')
        self.assertIn("sha", self.browser.cookies)
        self.assertNotIn("foo", self.browser.cookies)

    def test_cookies_extra_parameters(self):
        """Cookie can be created with extra parameters."""
        timestamp = int(time.time() + 120)
        self.browser.cookies.add('sha', 'zam', expiry=timestamp)
        cookie = self.browser.cookies["sha"]
        assert timestamp == cookie["expiry"]
