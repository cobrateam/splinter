# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import sys

import base64
from .status_code import StatusCode

if sys.version_info[0] > 2:
    from http import client as http_client
    from urllib.parse import urlparse
else:
    import httplib as http_client  # NOQA
    from urlparse import urlparse  # NOQA


class RequestHandler(object):

    def connect(self, url):
        if not (url.startswith("file:") or url.startswith("about:")):
            self.request_url = url
            self._create_connection()
            status_code = self._store_response()
            self.conn.close()
        else:
            status_code = StatusCode(200, 'Ok')
        return status_code

    def _store_response(self):
        self.response = self.conn.getresponse()
        return StatusCode(self.response.status, self.response.reason)

    def _create_connection(self):
        self._parse_url()
        if self.scheme == 'https':
            self.conn = http_client.HTTPSConnection(self.host, self.port)
        else:
            self.conn = http_client.HTTPConnection(self.host, self.port)
        self.conn.putrequest('GET', self.path)
        self.conn.putheader('User-agent', 'python/splinter')
        if self.auth:
            self.conn.putheader("Authorization", "Basic %s" % self.auth)
        self.conn.endheaders()

    def _parse_url(self):
        parsed_url = urlparse(self.request_url)
        if parsed_url.username and parsed_url.password:
            login = '%s:%s' % (parsed_url.username, parsed_url.password)
            if sys.version_info[0] > 2:
                self.auth = base64.standard_b64encode(login.encode('utf-8')).decode("utf-8")
            else:
                self.auth = base64.standard_b64encode(login)
        else:
            self.auth = None
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.path = parsed_url.path
        self.scheme = parsed_url.scheme
        if parsed_url.query:
            self.path = parsed_url.path + "?" + parsed_url.query
