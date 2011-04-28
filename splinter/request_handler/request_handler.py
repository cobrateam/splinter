import httplib
from urlparse import urlparse

class HtppResponseError(Exception):
    pass

class RequestHandler(object):
    def __init__(self, url):
        self.url = url
        self.connect()

    @property
    def status_code(self):
        return self.response.status

    def connect(self):
        self._create_connection()
        self._store_response()
        self._ensures_success_response()

    def _ensures_success_response(self):
        if(self.status_code == 404):
            raise HtppResponseError("page not found")

    def _store_response(self):
        self.response = self.conn.getresponse()

    def _create_connection(self):
        self._parse_url()
        self.conn = httplib.HTTPConnection(self.host)
        self.conn.request('GET', self.url)

    def _parse_url(self):
        parsed_url = urlparse(self.url)
        self.host = parsed_url.hostname
