# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import httplib
import base64
from urlparse import urlparse
from status_code import StatusCode


class RequestHandler(object):

    def connect(self, url):
        if not (url.startswith("file:") or url.startswith("about:")):
            self.request_url = url
            self._create_connection()
            self._store_response()
            self.conn.close()
        else:
            self.status_code = StatusCode(200, 'Ok')

    def ensure_success_response(self):
        """
        Guarantee the success on response.

        If response is not success, raises an
        :class:`HttpResponseError <splinter.request_handler.status_code.HttpResponseError>`
        exception.
        """
        self.status_code.is_valid_response()

    def _store_response(self):
        self.response = self.conn.getresponse()
        self.status_code = StatusCode(self.response.status, self.response.reason)

    def _create_connection(self):
        self._parse_url()
        if self.scheme == 'https':
            self.conn = httplib.HTTPSConnection(self.host, self.port)
        else:
            self.conn = httplib.HTTPConnection(self.host, self.port)
        self.conn.putrequest('GET', self.path)
        self.conn.putheader('User-agent', 'python/splinter')
        if self.auth:
            self.conn.putheader("Authorization", "Basic %s" % self.auth)
        self.conn.endheaders()

    def _parse_url(self):
        parsed_url = urlparse(self.request_url)
        if parsed_url.username and parsed_url.password:
            login = '%s:%s' % (parsed_url.username, parsed_url.password)
            self.auth = base64.standard_b64encode(login)
        else:
            self.auth = None
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.path = parsed_url.path
        self.scheme = parsed_url.scheme
        if parsed_url.query:
            self.path = parsed_url.path + "?" + parsed_url.query
