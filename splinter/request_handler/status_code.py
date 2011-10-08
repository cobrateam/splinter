# -*- coding: utf-8 -*-

class HttpResponseError(Exception):
    """
    Represents an HTTP response error.
    """

    def __init__(self, code, reason):
        #: Number representing the error (example: 404)
        self.status_code = code

        #: Reason of the fail (example: "Not found")
        self.reason = reason.title()

        #: A message for the error (example: "404 - Not found")
        self.msg = "%s - %s" % (self.status_code, self.reason)

    def __str__(self):
        return self.msg


class StatusCode(object):

    http_errors = (400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411,
                   412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505)

    def __init__(self, status_code, reason):
        #: A message for the response (example: Success)
        self.reason = reason
        #: Code of the response (example: 200)
        self.code = status_code

    def __cmp__(self, other):
        if self.code == other:
            return 0
        return 1

    def is_valid_response(self):
        """
        Returns ``True`` if the response is valid (:attr:`code` < 400).

        Otherwise, raises an :class:`HttpResponseError <splinter.request_handler.status_code.HttpResponseError>`
        exception.
        """
        if self.code in self.http_errors:
            raise HttpResponseError(self.code, self.reason)
        return True

    def is_success(self):
        """
        Returns ``True`` if the response was succed, otherwise, returns ``False``.
        """
        if self.code not in self.http_errors:
            return True
        return False
