# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class StatusCode(object):

    http_errors = (400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411,
                   412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505)

    def __init__(self, status_code, reason):
        #: A message for the response (example: Success)
        self.reason = reason
        #: Code of the response (example: 200)
        self.code = status_code

    def __eq__(self, other):
        return self.code == other

    def __str__(self):
        return "%s - %s" % (self.code, self.reason)

    def is_success(self):
        """
        Returns ``True`` if the response was succeed, otherwise, returns ``False``.
        """
        if self.code not in self.http_errors:
            return True
        return False
