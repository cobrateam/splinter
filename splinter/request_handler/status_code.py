class HttpResponseError(Exception):

    def __init__(self, code, reason):
        self.status_code = code
        self.reason = reason.title()
        self.msg = "%s - %s" % (self.status_code, self.reason)

    def __str__(self):
        return self.msg


class StatusCode(object):

    http_errors = (400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411,
                   412, 413, 414, 415, 416, 417, 500, 501, 502, 503, 504, 505)

    def __init__(self, status_code, reason):
        self.reason = reason
        self.code = status_code

    def __cmp__(self, other):
        if self.code == other:
            return 0
        return 1

    def is_valid_response(self):
        if self.code in self.http_errors:
            raise HttpResponseError(self.code, self.reason)
        return True

    def is_success(self):
        if self.code not in self.http_errors:
            return True
        return False
