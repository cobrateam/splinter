import warnings

from nose.tools import assert_true, assert_false, assert_equals

class IsElementPresentTest(object):

    def test_is_element_present_by_css(self):
        "should is element present by css verify if element is present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_css('.async-element'))

    def test_is_element_present_by_css_using_a_custom_wait_time(self):
        "should is element present by css verify if element is present using a custom wait time"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_css('.async-element2', wait_time=3))

    def test_is_element_present_by_css_returns_false_if_element_is_not_present(self):
        "should is element present by css returns False if element is not present"
        self.browser.reload()
        assert_false(self.browser.is_element_present_by_css('.async-elementzz'))

    def test_is_element_not_present_by_css(self):
        "should is element not present by css verify if element is not present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        self.browser.is_element_present_by_css('.async-element')
        self.browser.find_by_css('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_css('.async-element'))

    def test_is_element_not_present_by_css_returns_false_if_element_is_present(self):
        "should is element not present by css returns False if element is present"
        self.browser.reload()
        assert_false(self.browser.is_element_not_present_by_css('h1'))

    def test_existence_of_is_element_present_by_css_selector_alias_and_that_its_deprecated(self):
        "should check the existence of the is_element_present_by_css_selector alias for backwards compatibility"
        self.browser.reload()
        is_present = self.browser.is_element_present_by_css('h1')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            is_present_deprecated = self.browser.is_element_present_by_css_selector('h1')
            warn = w[-1]
            warn_message = str(warn.message)
            assert issubclass(warn.category, DeprecationWarning)
            assert "is_element_present_by_css" in warn_message
            assert "is_element_present_by_css_selector" in warn_message
        assert_equals(is_present, is_present_deprecated)

    def test_existence_of_is_element_not_present_by_css_selector_alias_and_that_its_deprecated(self):
        "should check the existence of the is_element_not_present_by_css_selector alias for backwards compatibility"
        self.browser.reload()
        is_not_present = self.browser.is_element_not_present_by_css('h1')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            is_not_present_deprecated = self.browser.is_element_not_present_by_css_selector('h1')
            warn = w[-1]
            warn_message = str(warn.message)
            assert issubclass(warn.category, DeprecationWarning)
            assert "is_element_not_present_by_css" in warn_message
            assert "is_element_not_present_by_css_selector" in warn_message
        assert_equals(is_not_present, is_not_present_deprecated)

    def test_is_element_present_by_xpath(self):
        "should is element present by xpath verify if element is present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_xpath('//h4'))

    def test_is_element_present_by_xpath_using_a_custom_wait_time(self):
        "should is element present by xpath verify if element is present using a custom wait time"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_xpath('//h5', wait_time=3))

    def test_is_element_not_present_by_xpath(self):
        "should is element not present by xpath verify if element is not present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        self.browser.is_element_present_by_css('.async-element')
        self.browser.find_by_css('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_xpath('//h4'))

    def test_is_element_present_by_tag(self):
        "should is element present by tag verify if element is present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_tag('h4'))

    def test_is_element_present_by_tag_using_a_custom_wait_time(self):
        "should is element present by tag verify if element is present using a custom wait time"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_tag('h5', wait_time=3))

    def test_is_element_not_present_by_tag(self):
        "should is element not present by tag verify if element is not present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        self.browser.is_element_present_by_css('.async-element')
        self.browser.find_by_css('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_tag('h4'))

    def test_is_element_present_by_id(self):
        "should is element present by id verify if element is present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_id('async-header'))

    def test_is_element_present_by_id_using_a_custom_wait_time(self):
        "should is element present by id verify if element is present using a custom wait time"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_id('async-header2', wait_time=3))

    def test_is_element_present_by_id_returns_false_if_element_is_not_present(self):
        "should is element present by id returns False if element is not present"
        self.browser.reload()
        assert_false(self.browser.is_element_present_by_id('async-headerzz'))

    def test_is_element_not_present_by_id(self):
        "should is element not present by id verify if element is not present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        self.browser.is_element_present_by_css('.async-element')
        self.browser.find_by_css('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_id('async-header'))

    def test_is_element_not_present_by_id_returns_false_if_element_is_present(self):
        "should is element not present by id returns False if element is present"
        self.browser.reload()
        assert_false(self.browser.is_element_not_present_by_id('firstheader'))

    def test_is_element_present_by_name(self):
        "should is element present by name verify if element is present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_name('async-input'))

    def test_is_element_present_by_name_using_a_custom_wait_time(self):
        "should is element present by name verify if element is present using a custom wait time"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_name('async-input2', wait_time=3))

    def test_is_element_not_present_by_name(self):
        "should is element not present by name verify if element is not present"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        self.browser.is_element_present_by_css('.async-element')
        self.browser.find_by_css('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_name('async-input'))

    def test_is_element_not_present_by_name_using_a_custom_wait_time(self):
        "should is element not present by name verify if element is not present using a custom wait time"
        self.browser.reload()
        self.browser.find_by_css('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_name('async-input2', wait_time=3))
        self.browser.find_by_css('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_name('async-input2', wait_time=3))
