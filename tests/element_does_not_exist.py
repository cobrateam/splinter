# -*- coding: utf-8 -*-

from splinter.exceptions import ElementDoesNotExist


class ElementDoestNotExistTest(object):

    def test_element_query_should_raises_when_element_first_doest_exists(self):
        with self.assertRaises(ElementDoesNotExist):
            self.browser.find_by_css('.element-that-dont-exists').first

    def test_element_list_raises_when_element_last_does_not_exists(self):
        with self.assertRaises(ElementDoesNotExist):
            self.browser.find_by_css('.element-that-dont-exists').last

    def test_element_list_raises_when_element_does_not_exists(self):
        with self.assertRaises(ElementDoesNotExist):
            self.browser.find_by_css('.element-that-dont-exists')[2]

    def test_element_list_contains_right_information_and_raises_right_exception(self):
        "element list contains right information about query and raises nice exception message"
        with self.assertRaises(ElementDoesNotExist) as cm:
            element_list = self.browser.find_by_css('.element-that-dont-exists')
            self.assertEquals('css', element_list.find_by)
            self.assertEquals('.element-that-dont-exists', element_list.query)
            element_list.first

        expected_message = 'no elements could be find with css ".element-that-dont-exists"'

        e = cm.exception
        self.assertEquals(expected_message, e.args[0])

    def test_element_list_raises_when_element_first_doesnt_exists_in_element_context(self):
        "element list raises exception with right information in element context"
        with self.assertRaises(ElementDoesNotExist) as cm:
            element_list = self.browser.find_by_css("#inside").first.find_by_css('.inner-element-that-dont-exists')
            self.assertEquals('css', element_list.find_by)
            self.assertEquals('.inner-element-that-dont-exists', element_list.query)
            element_list.first

        expected_message = 'no elements could be find with css ".inner-element-that-dont-exists"'

        e = cm.exception
        self.assertEquals(expected_message, e.args[0])
