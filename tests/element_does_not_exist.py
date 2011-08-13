# -*- coding: utf-8 -*-

from nose.tools import assert_equals, raises
from splinter.exceptions import ElementDoesNotExist


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

    def test_element_list_contains_right_information_and_raises_right_exception(self):
        "element list contains right information about query and raises nice exception message"
        expected_message = 'no elements could be find with css ".element-that-dont-exists"'
        element_list = self.browser.find_by_css('.element-that-dont-exists')
        assert_equals('css', element_list.find_by)
        assert_equals('.element-that-dont-exists', element_list.query)

        try:
            element_list.first
        except ElementDoesNotExist, e:
            assert_equals(expected_message, e.args[0])

    def test_element_list_raises_when_element_first_doesnt_exists_in_element_context(self):
        "element list raises exception with right information in element context"
        expected_message = 'no elements could be find with css ".inner-element-that-dont-exists"'
        element_list = self.browser.find_by_css("#inside").first.find_by_css('.inner-element-that-dont-exists')
        assert_equals('css', element_list.find_by)
        assert_equals('.inner-element-that-dont-exists', element_list.query)

        try:
            element_list.first
        except ElementDoesNotExist, e:
            assert_equals(expected_message, e.args[0])
