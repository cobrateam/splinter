# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class CookiesTest(object):

    def test_create_and_access_a_cookie(self):
        "should be able to create and access a cookie"
        self.browser.cookies.add({'sha': 'zam'})
        self.assertEqual(self.browser.cookies['sha'], 'zam')

    def test_create_some_cookies_and_delete_them_all(self):
        "should be able to delete all cookies"
        self.browser.cookies.add({'whatever': 'and ever'})
        self.browser.cookies.add({'anothercookie': 'im bored'})
        self.browser.cookies.delete()
        self.assertEqual(self.browser.cookies, {})

    def test_create_and_delete_a_cookie(self):
        "should be able to create and destroy a cookie"
        self.browser.cookies.delete()
        self.browser.cookies.add({'cookie': 'with milk'})
        self.browser.cookies.delete('cookie')
        self.assertEqual(self.browser.cookies, {})

    def test_create_and_delete_many_cookies(self):
        "should be able to create and destroy many cookies"
        self.browser.cookies.delete()
        self.browser.cookies.add({'cookie': 'cooked'})
        self.browser.cookies.add({'anothercookie': 'uncooked'})
        self.browser.cookies.add({'notacookie': 'halfcooked'})
        self.browser.cookies.delete('cookie', 'notacookie')
        self.assertEqual('uncooked', self.browser.cookies['anothercookie'])

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        self.browser.cookies.delete()
        self.browser.cookies.add({'foo': 'bar'})
        self.browser.cookies.delete('mwahahahaha')
        self.assertEqual(self.browser.cookies, {'foo': 'bar'})
