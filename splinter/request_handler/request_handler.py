import httplib
from urlparse import urlparse

class HttpResponseError(Exception):
    pass

class RequestHandler():
    @property
    def status_code(self):
        return self.response.status

    def connect(self, url):
        self.request_url = url
        self._create_connection()
        self._store_response()

    #TODO how to get an internal server error?
    def ensures_success_response(self):
        if self.status_code == 404:
            raise HttpResponseError("page not found")
        elif self.status_code == 500:
            raise HttpResponseError("internal server error")

    def _store_response(self):
        self.response = self.conn.getresponse()

    def _create_connection(self):
        self._parse_url()
        self.conn = httplib.HTTPConnection(self.host)
        self.conn.request('GET', self.request_url)

    def _parse_url(self):
        parsed_url = urlparse(self.request_url)
        self.host = parsed_url.hostname
