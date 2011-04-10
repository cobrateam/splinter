from splinter.element_list import ElementDoesNotExist
from nose.tools import raises

class ElementDoestNotExistTest(object):

    @raises(ElementDoesNotExist)
    def test_element_query_should_raises_when_element_first_doest_exists(self):
        self.browser.find_by_css('.element-that-dont-exists').first

    @raises(ElementDoesNotExist)
    def test_element_list_raises_when_element_last_does_not_exists(self):
        self.browser.find_by_css('.element-that-dont-exists').last

    @raises(ElementDoesNotExist)
    def test_element_list_raises_when_element_does_not_exists(self):
        self.browser.find_by_css('.element-that-dont-exists')[2]


