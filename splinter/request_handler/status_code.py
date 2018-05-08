# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class StatusCode(object):

    def __init__(self, status_code, reason):
        #: A message for the response (example: Success)
        self.reason = reason
        #: Code of the response (example: 200)
        self.code = status_code

    def __eq__(self, other):
        return self.code == other

    def __str__(self):
        return "{} - {}".format(self.code, self.reason)

    def is_success(self):
        """
        Returns ``True`` if the response was succeed, otherwise, returns ``False``.
        """
        return self.code < 400
