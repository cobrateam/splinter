class HttpResponseError(Exception):
    pass

class StatusCode():
    http_errors = [400, 401, 403, 404, 405, 406, 500, 502, 503]

    def __init__(self, response):
        self.response = response
        self.code = self.response.status

    def __cmp__(self, other):
        if self.code == other:
            return 0
        return 1

    def is_valid_response(self):
        if self.code in self.http_errors:
            raise HttpResponseError(self.response.reason)
        return True

    def is_success(self):
        if self.code not in self.http_errors:
            return True
        return False
