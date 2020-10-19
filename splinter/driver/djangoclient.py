# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import six
from six.moves.urllib import parse

from splinter.cookie_manager import CookieManagerAPI
from splinter.request_handler.status_code import StatusCode

from .lxmldriver import LxmlDriver

import warnings


class CookieManager(CookieManagerAPI):
    def add(self, cookies):
        if isinstance(cookies, list):
            warnings.warn(
                'Using a list of cookies is deprecated.'
                ' Version 0.16.0 will only accept one cookie at a time.',
                FutureWarning,
            )
            for cookie in cookies:
                for key, value in cookie.items():
                    self.driver.cookies[key] = value
            return
        for key, value in cookies.items():
            self.driver.cookies[key] = value

    def delete(self, *cookies):
        if cookies:
            for cookie in cookies:
                try:
                    del self.driver.cookies[cookie]
                except KeyError:
                    pass
        else:
            self.delete_all()

    def delete_all(self):
        self.driver.cookies.clear()

    def all(self, verbose=False):
        cookies = {}
        for key, value in self.driver.cookies.items():
            cookies[key] = value
        return cookies

    def __getitem__(self, item):
        return self.driver.cookies[item].value

    def __contains__(self, key):
        return key in self.driver.cookies

    def __eq__(self, other_object):
        if isinstance(other_object, dict):
            cookies_dict = {
                key: morsel.value for key, morsel in self.driver.cookies.items()
            }
            return cookies_dict == other_object
        return False


class DjangoClient(LxmlDriver):

    driver_name = "django"

    def __init__(self, user_agent=None, wait_time=2, **kwargs):
        from django.test.client import Client

        self._custom_headers = kwargs.pop("custom_headers", {})

        client_kwargs = {}
        for key, value in six.iteritems(kwargs):
            if key.startswith("client_"):
                client_kwargs[key.replace("client_", "")] = value

        self._browser = Client(**client_kwargs)
        self._user_agent = user_agent
        self._cookie_manager = CookieManager(self._browser)
        super(DjangoClient, self).__init__(wait_time=wait_time)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def _post_load(self):
        self._forms = {}
        try:
            del self._html
        except AttributeError:
            pass
        self.status_code = StatusCode(self._response.status_code, "")

    def _handle_redirect_chain(self):
        if self._response.redirect_chain:
            for redirect_url, redirect_code in self._response.redirect_chain:
                self._last_urls.append(redirect_url)
            self._url = self._last_urls[-1]

    def _set_extra_params(self, url):
        extra = {}
        components = parse.urlparse(url)
        if components.hostname:
            extra.update({"SERVER_NAME": components.hostname})
        if components.port:
            extra.update({"SERVER_PORT": components.port})
        if self._user_agent:
            extra.update({"User-Agent": self._user_agent})
        if self._custom_headers:
            extra.update(self._custom_headers)
        return extra

    def _do_method(self, method, url, data=None):
        self._url = url
        extra = self._set_extra_params(url)
        func_method = getattr(self._browser, method.lower())
        self._response = func_method(url, data=data, follow=True, **extra)
        self._last_urls.append(url)
        self._handle_redirect_chain()
        self._post_load()

    def submit_data(self, form):
        return super(DjangoClient, self).submit(form).content

    @property
    def html(self):
        return self._response.content.decode(self._response._charset or "utf-8")
