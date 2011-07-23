from splinter.cookie_manager import CookieManagerAPI


class CookieManager(CookieManagerAPI):

    def __init__(self, driver):
        self.driver = driver

    def add(self, cookies):
        for key, value in cookies.items():
            self.driver.add_cookie({'name': key, 'value': value})

    def delete(self, cookie=None):
        if cookie:
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
