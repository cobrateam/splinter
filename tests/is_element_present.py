from nose.tools import assert_true, assert_false

class IsElementPresentTest(object):

    def test_is_element_present_by_css_selector(self):
        "should is element present by css selector verify if element is present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_css_selector('.async-element'))

    def test_is_element_present_by_css_selector_using_a_custom_wait_time(self):
        "should is element present by css selector verify if element is present using a custom wait time"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_css_selector('.async-element2', wait_time=3))

    def test_is_element_present_by_css_selector_returns_false_if_element_is_not_present(self):
        "should is element present by css selector returns False if element is not present"
        assert_false(self.browser.is_element_present_by_css_selector('.async-elementzz'))

    def test_is_element_not_present_by_css_selector(self):
        "should is element not present by css selector verify if element is not present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        self.browser.is_element_present_by_css_selector('.async-element')
        self.browser.find_by_css_selector('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_css_selector('.async-element'))

    def test_is_element_not_present_by_css_selector_returns_false_if_element_is_present(self):
        "should is element not present by css selector returns False if element is present"
        assert_false(self.browser.is_element_not_present_by_css_selector('h1'))

    def test_is_element_present_by_xpath(self):
        "should is element present by xpath verify if element is present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_xpath('//h4'))

    def test_is_element_present_by_xpath_using_a_custom_wait_time(self):
        "should is element present by xpath verify if element is present using a custom wait time"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_xpath('//h5', wait_time=3))

    def test_is_element_not_present_by_xpath(self):
        "should is element not present by xpath verify if element is not present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        self.browser.is_element_present_by_css_selector('.async-element')
        self.browser.find_by_css_selector('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_xpath('//h4'))

    def test_is_element_present_by_tag(self):
        "should is element present by tag verify if element is present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_tag('h4'))

    def test_is_element_present_by_tag_using_a_custom_wait_time(self):
        "should is element present by tag verify if element is present using a custom wait time"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_tag('h5', wait_time=3))

    def test_is_element_not_present_by_tag(self):
        "should is element not present by tag verify if element is not present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        self.browser.is_element_present_by_css_selector('.async-element')
        self.browser.find_by_css_selector('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_tag('h4'))

    def test_is_element_present_by_id(self):
        "should is element present by id verify if element is present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_id('async-header'))

    def test_is_element_present_by_id_using_a_custom_wait_time(self):
        "should is element present by id verify if element is present using a custom wait time"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_id('async-header2', wait_time=3))

    def test_is_element_present_by_id_returns_false_if_element_is_not_present(self):
        "should is element present by id returns False if element is not present"
        assert_false(self.browser.is_element_present_by_id('async-headerzz'))

    def test_is_element_not_present_by_id(self):
        "should is element not present by id verify if element is not present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        self.browser.is_element_present_by_css_selector('.async-element')
        self.browser.find_by_css_selector('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_id('async-header'))

    def test_is_element_not_present_by_id_returns_false_if_element_is_present(self):
        "should is element not present by id returns False if element is present"
        assert_false(self.browser.is_element_not_present_by_id('firstheader'))

    def test_is_element_present_by_name(self):
        "should is element present by name verify if element is present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_name('async-input'))

    def test_is_element_present_by_name_using_a_custom_wait_time(self):
        "should is element present by name verify if element is present using a custom wait time"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert_true(self.browser.is_element_present_by_name('async-input2', wait_time=3))

    def test_is_element_not_present_by_name(self):
        "should is element not present by name verify if element is not present"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        self.browser.is_element_present_by_css_selector('.async-element')
        self.browser.find_by_css_selector('.remove-async-element').first.click()
        assert_true(self.browser.is_element_not_present_by_name('async-input'))


