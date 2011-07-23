# -*- coding: utf-8 -*-
from nose.tools import assert_equals, assert_false, assert_true, raises
from splinter.element_list import ElementList
from splinter.exceptions import ElementDoesNotExist

import unittest


class Person(object):
    """Very simple class, just for tests"""

    def __init__(self):
        self.current_action = None

    def walk(self):
        self.current_action = "walking"


class ElementListTest(unittest.TestCase):

    def test_method_that_verifies_if_the_list_is_empty(self):
        "should verify if the list is empty"
        the_list = ElementList([1, 2, 3])
        assert_false(the_list.is_empty())
        assert_true(ElementList([]).is_empty())

    def test_property_first_and_last(self):
        "should provide a \"first\" and a \"last\" properties which returns the first and last element"
        the_list = ElementList([1, 2, 3])
        assert_equals(the_list[0], the_list.first)
        assert_equals(the_list[2], the_list.last)

    def test_call_method_on_first_element(self):
        "when some method is missing on ElementList and is present in element, it should be passed"
        the_list = ElementList([Person(), Person(), Person()])
        the_list.walk()
        the_person = the_list.first
        assert_equals("walking", the_person.current_action)

    @raises(ElementDoesNotExist)
    def test_raise_exception_on_indexerror(self):
        "should raise ElementDoesNotExist exception on IndexError"
        ElementList([]).first

    @raises(AttributeError)
    def test_raise_attribute_error(self):
        "should raise AttributeError when trying to access a non-existent method on list and element"
        the_list = ElementList([Person(), Person()])
        the_list.talk()

    @raises(AttributeError)
    def test_attribute_error_for_empty(self):
        "should raise AttributeError when the list is empty and someone tries to access a method or property on it"
        the_list = ElementList([])
        the_list.unknown_method()

    def test_attribute_error_content(self):
        "should raise AttributeError with right content"
        expected_message = "'ElementList' object has no attribute 'talk'"
        try:
            the_list = ElementList([Person(), Person()])
            the_list.talk()
        except AttributeError, e:
            assert_equals(expected_message, e.message)
