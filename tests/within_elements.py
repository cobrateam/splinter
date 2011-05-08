from splinter.element_list import ElementList

class WithinElementsTest(object):
    def test_element_should_be_a_elementList(self):
        "should be element list"
        element = self.browser.within('body')
        assert isinstance(element, ElementList)

    def test_find_element_within_should_be_a_elementList(self):
        "should return a elementList"
        element = self.browser.within('body').find_by_css('h2')
        assert isinstance(element, ElementList)

    def test_return_a_empty_list(self):
        "should return a empty list"
        elements = self.browser.within('body').find_by_css('h2')
        assert elements.is_empty()

    def test_return_a_list_with_elements(self):
        "should return a single element in list"
        elements = self.browser.within('body').find_by_css('h1')
        assert not elements.is_empty()
