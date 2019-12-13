# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import sys

from splinter.cookie_manager import CookieManagerAPI

if sys.version_info[0] > 2:
    from urllib.parse import urlparse
else:
    from urlparse import urlparse  # NOQA


class CookieManager(CookieManagerAPI):
    def add(self, key, value='', **kwargs):
        cookie = {
            'name': key,
            'value': value,
        }
        cookie.update(kwargs)

        self.driver.add_cookie(cookie)

    def delete(self, *cookies):
        if cookies:
            for cookie in cookies:
                self.driver.delete_cookie(cookie)
        else:
            self.delete_all()

    def delete_all(self):
        self.driver.delete_all_cookies()

    def all(self, verbose=False):
        cookies = self.driver.get_cookies()
        if not verbose:
            cleaned_cookies = {}
            for cookie in cookies:
                if not cookie["domain"].startswith("."):
                    cookie_domain = cookie["domain"]
                else:
                    cookie_domain = cookie["domain"][1:]

                if cookie_domain in urlparse(self.driver.current_url).netloc:
                    cleaned_cookies[cookie["name"]] = cookie

            return cleaned_cookies

        return cookies

    def __getitem__(self, item):
        return self.driver.get_cookie(item)

    def __contains__(self, key):
        return self.driver.get_cookie(key) is not None

    def __eq__(self, other_object):
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie["name"]] = cookie["value"]

        if isinstance(other_object, dict):
            return dict(cookies) == other_object

        return False
