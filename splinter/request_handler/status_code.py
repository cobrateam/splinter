class HttpResponseError(Exception):
    def __init__(self, msg, code, reason):
        self.msg = msg
        self.status_code = code
        self.reason = reason.title()

class StatusCode():
    http_errors = [400, 401, 403, 404, 405, 406, 500, 502, 503]

    def __init__(self, status_code, reason):
        self.reason = reason
        self.code = status_code

    def __cmp__(self, other):
        if self.code == other:
            return 0
        return 1

    def is_valid_response(self):
        if self.code in self.http_errors:
            msg = "%s - %s" % (str(self.code), self.reason)
            raise HttpResponseError(msg, self.code, self.reason)
        return True

    def is_success(self):
        if self.code not in self.http_errors:
            return True
        return False
