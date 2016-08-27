# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import httplib
from urlparse import urlparse


class StatusCode(object):

    def __init__(self, url):
        #: so we can grab the header return from the url
        self.url = url

        # need to parse the host and path from the url
        parsed_url = urlparse(self.url)
        con_url = parsed_url.netloc
        # we may also need to think about including the query string
        path = parsed_url.path

        try:
            conn = httplib.HTTPConnection(con_url)
            conn.request("HEAD", path)
            resp = conn.getresponse()
            self.code = resp.status
            self.reason = resp.reason
        except StandardError:
            self.code = None
            self.reason = None

    def __eq__(self, other):
        return self.code == other

    def __str__(self):
        return "{} - {}".format(self.code, self.reason)

    def is_success(self):
        """
        Returns ``True`` if the response was succeed, otherwise, returns ``False``.
        """
        return self.code < 400
