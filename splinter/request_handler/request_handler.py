import httplib
from urlparse import urlparse

class RequestHandler(object):
    def __init__(self, url):
        self.url = url
        self.connect()

    @property
    def status_code(self):
        """
        Return the HTTP status code of a request
        """
        self.response = self.conn.getresponse()
        return self.response.status

    def connect(self):
        self._parse_url()
        self.conn = httplib.HTTPConnection(self.host)
        self.conn.request('get', self.url)

    def _parse_url(self):
        parsed_url = urlparse(self.url)
        self.host = parsed_url.hostname
