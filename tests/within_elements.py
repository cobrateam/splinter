from splinter.container import Container
from splinter.element_list import ElementList

class WithinElementsTest(object):
    def test_element_should_be_a_container(self):
        "should be container"
        element = self.browser.within('body')
        assert isinstance(element, ElementList)

    def test_find_element_within(self):
        "should return a elementList"
        element = self.browser.within('body').find_by_css('h2')
        assert isinstance(element, ElementList)
