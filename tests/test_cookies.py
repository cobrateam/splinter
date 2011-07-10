from nose.tools import assert_equals


class CookiesTest(object):

    def test_create_and_access_a_cookie(self):
        "should be able to create and access a cookie"
        self.browser.add_cookie({'sha': 'zam'})
        assert_equals(self.browser.cookie('sha'), 'zam')

    def test_create_some_cookies_and_delete_them_all(self):
        "should be able to delete all cookies"
        self.browser.add_cookie({'whatever': 'and ever'})
        self.browser.add_cookie({'anothercookie': 'im bored'})
        self.browser.delete_cookies()
        assert_equals(self.browser.cookies, {})

    def test_create_and_delete_a_cookie(self):
        "should be able to create and destroy a cookie"
        self.browser.delete_cookies()
        self.browser.add_cookie({'cookie': 'with milk'})
        self.browser.delete_cookie('cookie')
        assert_equals(self.browser.cookies, {})

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        self.browser.delete_cookies()
        self.browser.add_cookie({'foo': 'bar'})
        self.browser.delete_cookie('mwahahahaha')
        assert_equals(self.browser.cookies, {'foo': 'bar'})
