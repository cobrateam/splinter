# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import warnings
from urllib.parse import urlparse

from splinter.cookie_manager import CookieManagerAPI


class CookieManager(CookieManagerAPI):
    def add(self, cookie, **kwargs):
        for key, value in cookie.items():
            kwargs['name'] = key
            kwargs['value'] = value
            self.driver.add_cookie(kwargs)

    def delete(self, *cookies):
        if cookies:
            for cookie in cookies:
                self.driver.delete_cookie(cookie)
        else:
            warnings.warn(
                'Deleting all cookies via CookieManager.delete() with no arguments '
                'has been deprecated. use CookieManager.delete_all().',
                FutureWarning,
            )
            self.delete_all()

    def delete_all(self):
        self.driver.delete_all_cookies()

    def all(self, verbose=False):  # NOQA: A003
        if not verbose:
            cleaned_cookies = {}
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if not cookie["domain"].startswith("."):
                    cookie_domain = cookie["domain"]
                else:
                    cookie_domain = cookie["domain"][1:]

                if cookie_domain in urlparse(self.driver.current_url).netloc:
                    cleaned_cookies[cookie["name"]] = cookie["value"]

            return cleaned_cookies
        return self.driver.get_cookies()

    def __getitem__(self, item):
        return self.driver.get_cookie(item)["value"]

    def __contains__(self, key):
        return self.driver.get_cookie(key) is not None

    def __eq__(self, other_object):
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie["name"]] = cookie["value"]

        if isinstance(other_object, dict):
            return dict(cookies) == other_object

        return False
