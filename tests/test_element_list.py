# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from splinter.element_list import ElementList
from splinter.exceptions import ElementDoesNotExist


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
        self.assertFalse(the_list.is_empty())
        self.assertTrue(ElementList([]).is_empty())

    def test_property_first_and_last(self):
        """
        should provide a \"first\" and a \"last\" properties
        which returns the first and last element
        """
        the_list = ElementList([1, 2, 3])
        self.assertEqual(the_list[0], the_list.first)
        self.assertEqual(the_list[2], the_list.last)

    def test_call_method_on_first_element(self):
        """
        when some method is missing on ElementList and
        is present in element, it should be passed
        """
        the_list = ElementList([Person(), Person(), Person()])
        the_list.walk()
        the_person = the_list.first
        self.assertEqual("walking", the_person.current_action)

    def test_raise_exception_on_indexerror(self):
        "should raise ElementDoesNotExist exception on IndexError"
        with self.assertRaises(ElementDoesNotExist):
            ElementList([]).first

    def test_raise_exception_on_indexerror_with_unicode_query(self):
        "should raise ElementDoesNotExist exception on IndexError"
        with self.assertRaises(ElementDoesNotExist):
            ElementList([], query=u'.element[title=título]').first

    def test_raise_attribute_error(self):
        """
        should raise AttributeError when trying to access
        a non-existent method on list and element
        """
        with self.assertRaises(AttributeError):
            the_list = ElementList([Person(), Person()])
            the_list.talk()

    def test_attribute_error_for_empty(self):
        """
        should raise AttributeError when the list is empty
        and someone tries to access a method or property on it
        """
        with self.assertRaises(AttributeError):
            the_list = ElementList([])
            the_list.unknown_method()

    def test_attribute_error_content(self):
        "should raise AttributeError with right content"
        with self.assertRaises(AttributeError) as cm:
            the_list = ElementList([Person(), Person()])
            the_list.talk()

        expected_message = "'ElementList' object has no attribute 'talk'"
        e = cm.exception
        self.assertEqual(expected_message, e.args[0])

    def test_not_found_exception_with_query_and_method(self):
        """
        should receive the find method
        and the query and use them in exception
        """
        with self.assertRaises(ElementDoesNotExist) as cm:
            the_list = ElementList([], find_by="id", query="menu")
            the_list.first

        expected_message = 'no elements could be found with id "menu"'
        e = cm.exception
        self.assertEqual(expected_message, e.args[0])
