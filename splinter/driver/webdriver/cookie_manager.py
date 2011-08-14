from splinter.cookie_manager import CookieManagerAPI


class CookieManager(CookieManagerAPI):

    def __init__(self, driver):
        self.driver = driver

    def add(self, cookies):
        for key, value in cookies.items():
            self.driver.add_cookie({'name': key, 'value': value})

    def delete(self, *cookies):
        if cookies:
            for cookie in cookies:
                self.driver.delete_cookie(cookie)
        else:
            self.driver.delete_all_cookies()

    def __getitem__(self, item):
        return self.driver.get_cookie(item)['value']

    def __eq__(self, other_object):
        cookies = {}
        for cookie in self.driver.get_cookies():
            cookies[cookie['name']] = cookie['value']

        if isinstance(other_object, dict):
            return dict(cookies) == other_object


class ChromeCookieManager(CookieManager):
    """
    This class exists because of a bug on Chrome webdriver.

    When you call ``driver.delete_cookie(<cookie-identifier>)`` in ChromeDriver, all cookies are deleted.

    We've filled the issue #2262 on Selenium project and we should delete this class when the issue is solved.

    Link to issue: http://code.google.com/p/selenium/issues/detail?id=2262
    """

    def __init__(self, driver):
        super(ChromeCookieManager, self).__init__(driver)
        self._cookies = {}

    def add(self, cookies):
        super(ChromeCookieManager, self).add(cookies)
        self._cookies.update(cookies)

    def delete(self, *cookies):
        for cookie in cookies:
            try:
                del self._cookies[cookie]
            except KeyError:
                pass

        self.driver.delete_all_cookies()

        # Just delete all cookies
        if not cookies:
            self._cookies = {}

        self.add(self._cookies)
