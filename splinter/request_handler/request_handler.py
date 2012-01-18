import httplib
from urlparse import urlparse
from status_code import StatusCode


class RequestHandler(object):

    def connect(self, url):
        if url.startswith("http://"):
            self.request_url = url
            self._create_connection()
            self._store_response()
            self.conn.close()
        else:
            self.status_code = StatusCode(200, 'Ok')

    def ensure_success_response(self):
        """
        Guarantee the success on response.

        If the response is not successed, raises an
        :class:`HttpResponseError <splinter.request_handler.status_code.HttpResponseError>`
        exception.
        """
        self.status_code.is_valid_response()

    def _store_response(self):
        self.response = self.conn.getresponse()
        self.status_code = StatusCode(self.response.status, self.response.reason)

    def _create_connection(self):
        self._parse_url()
        self.conn = httplib.HTTPConnection(self.host, self.port)
        self.conn.request('GET', self.path)

    def _parse_url(self):
        parsed_url = urlparse(self.request_url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.path = parsed_url.path
        if parsed_url.query:
            self.path = parsed_url.path + "?" + parsed_url.query
