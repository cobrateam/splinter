class CookieManager(object):

    def __init__(self, browser_cookies):
        self._cookies = browser_cookies

    def add(self, cookies):
        for key, value in cookies.items():
            self._cookies[key] = value

    def delete(self, cookie=None):
        if cookie:
            try:
                del self._cookies[cookie]
            except KeyError:
                pass
        else:
            self._cookies.clearAll()

    def __getitem__(self, item):
        return self._cookies[item]

    def __eq__(self, other_object):
        if isinstance(other_object, dict):
            return dict(self._cookies) == other_object
