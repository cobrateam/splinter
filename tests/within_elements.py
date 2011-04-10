from splinter.container import Container
from splinter.element_list import ElementList

class WithinElementsTest(object):
    def test_element_should_be_a_container(self):
        "should be container"
        element = self.browser.within('h1')
        assert isinstance(element, Container)

    def test_find_element_within(self):
        "should return a elementList"
        element = self.browser.within('h2').find_by_css()
        assert isinstance(element, ElementList)

    def test_element_list_empty(self):
        element_list = self.browser.within('h2').find_by_css()
        assert not element_list

