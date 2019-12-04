import socket

try:
    from httplib import HTTPException
except ImportError:
    from http.client import HTTPException

import urllib3
from urllib3.exceptions import MaxRetryError

from selenium.webdriver.remote import remote_connection


# Get the original _request and store for future use in the monkey patched version as 'super'
old_request = remote_connection.RemoteConnection._request


def patch_request(self, *args, **kwargs):
    """Override _request to set socket timeout to some appropriate value."""
    exception = HTTPException('Unable to get response')
    for _ in range(3):
        try:
            return old_request(self, *args, **kwargs)
        except (socket.error, HTTPException, IOError, OSError, MaxRetryError) as exc:
            exception = exc
            self._conn = urllib3.PoolManager(timeout=self._timeout)
    raise exception
