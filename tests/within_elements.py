class WithinElementsTest(object):

    def test_return_a_empty_list(self):
        "should return an empty list"
        elements = self.browser.within('body').find_by_css('h3')
        assert elements.is_empty()

    def test_return_a_list_with_elements(self):
        "should return a single element in list"
        elements = self.browser.within('body').find_by_css('h1')
        assert not elements.is_empty()

    def test_return_nothing_if_context_is_not_valid(self):
        "should return nothing if context is not valid"
        elements = self.browser.within('h1').find_by_css('body')
        assert elements.is_empty()
