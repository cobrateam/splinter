from http.client import HTTPException

import urllib3
from selenium.webdriver.remote import remote_connection
from urllib3.exceptions import MaxRetryError


# Get the original _request and store for future use in the monkey patched version as 'super'
old_request = remote_connection.RemoteConnection._request


def patch_request(self, *args, **kwargs):
    """Override _request to set socket timeout to some appropriate value."""
    exception = HTTPException("Unable to get response")
    for _ in range(3):
        try:
            return old_request(self, *args, **kwargs)
        except (OSError, HTTPException, MaxRetryError) as exc:
            exception = exc
            self._conn = urllib3.PoolManager(timeout=self._timeout)
    raise exception
