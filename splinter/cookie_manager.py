class CookieManager(object):

    def __init__(self, browser_cookies, *args, **kwargs):
        self._cookies = browser_cookies

    def add(self, cookies):
        for key in cookies.keys():
            self._cookies[key] = cookies[key]

    def delete(self, cookie=None):
        if not cookie:
            self._cookies.clearAll()
        else:
            try:
                del(self._cookies[cookie])
            except KeyError:
                pass

    def __getitem__(self, item):
        return self._cookies.__getitem__(item)

    def __eq__(self, other_object):
        if isinstance(other_object, dict):
            return dict(self._cookies) == other_object
