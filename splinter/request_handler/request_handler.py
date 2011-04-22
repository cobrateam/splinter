import httplib
from urlparse import urlparse

class RequestHandler(object):
    def __init__(self, url):
        self.url = url
        self.connect()

    @property
    def status_code(self):
        return self.response.status

    def connect(self):
        self._parse_url()
        self.conn = httplib.HTTPConnection(self.host)
        self.conn.request('GET', self.url)
        self.store_response()

    def store_response(self):
        self.response = self.conn.getresponse()

    def _parse_url(self):
        parsed_url = urlparse(self.url)
        self.host = parsed_url.hostname
