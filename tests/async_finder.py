class AsyncFinderTests(object):

    def test_find_by_css_selector_should_found_an_async_element(self):
        "should find element by css selector found an async element"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_css_selector('.async-element'))

    def test_find_by_xpath_should_found_an_async_element(self):
        "should find by xpath found an async element"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_xpath('//h4'))

    def test_find_by_tag_should_found_an_async_element(self):
        "should find by tag found an async element"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_tag('h4'))

    def test_find_by_id_should_found_an_async_element(self):
        "should find by id found an async element"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_id('async-header'))

    def test_find_by_name_should_found_an_async_element(self):
        "should find by name found an async element"
        self.browser.find_by_css_selector('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_name('async-input'))


