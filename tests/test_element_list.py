# -*- coding: utf-8 -*-
import unittest
from nose.tools import assert_equals
from splinter.element_list import ElementList

class Person(object):
    """Very simple class, just for tests"""

    def __init__(self):
        self.current_action = None

    def walk(self):
        self.current_action = "walking"

class ElementListTest(unittest.TestCase):

    def test_call_method_on_first_element(self):
        "when some method is missing on ElementList and is present in element, it should be passed"
        the_list = ElementList([Person(), Person(), Person()])
        the_list.walk()
        the_person = the_list.first
        assert_equals("walking", the_person.current_action)
