from nose.tools import assert_true, assert_false


class IsTextPresentTest(object):

    def test_is_text_present(self):
        "should verify if text is present"
        assert_true(self.browser.is_text_present('Example Header'))

    def test_is_text_present_and_should_return_false(self):
        "should verify if text is present and return false"
        assert_false(self.browser.is_text_present('Text that not exist'))

    def test_is_text_present_and_should_wait_time(self):
        "should verify if text is present and wait for five seconds"
        self.browser.find_link_by_text('FOO').first.click()
        assert_true(self.browser.is_text_present('BAR!', wait_time=5))

    def test_is_text_not_present(self):
        "should verify if text is not present"
        assert_true(self.browser.is_text_not_present('Text that not exist'))

    def test_is_text_not_present_and_should_return_false(self):
        "should verify if text is not prasent and return false"
        assert_false(self.browser.is_text_not_present('Example Header'))

    def test_is_text_not_present_and_should_wait_time(self):
        "should verify if text is not present and wait for five seconds"
        self.browser.find_link_by_text('FOO').first.click()
        assert_true(self.browser.is_text_not_present('another text', wait_time=5))
