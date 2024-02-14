# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from splinter.element_list import ElementList
from splinter.exceptions import ElementDoesNotExist


class Person:
    """Very simple class, just for tests"""

    def __init__(self):
        self.current_action = None

    def walk(self):
        self.current_action = "walking"


def test_slice():
    """ElementList should work with slice operations."""
    elem_list = ElementList([1, 2, 3, 4, 5])
    new_elem_list = elem_list[2:5]
    assert len(new_elem_list) == 3


def test_method_that_verifies_if_the_list_is_empty():
    "should verify if the list is empty"
    the_list = ElementList([1, 2, 3])
    assert not the_list.is_empty()
    assert ElementList([]).is_empty()


def test_property_first_and_last():
    """
    should provide a \"first\" and a \"last\" properties
    which returns the first and last element
    """
    the_list = ElementList([1, 2, 3])
    assert the_list[0] == the_list.first
    assert the_list[2] == the_list.last


def test_call_method_on_first_element():
    """
    when some method is missing on ElementList and
    is present in element, it should be passed
    """
    the_list = ElementList([Person(), Person(), Person()])
    the_list.walk()
    the_person = the_list.first
    assert "walking" == the_person.current_action


def test_raise_exception_on_indexerror():
    "should raise ElementDoesNotExist exception on IndexError"
    with pytest.raises(ElementDoesNotExist):
        ElementList([]).first


def test_raise_exception_on_indexerror_with_unicode_query():
    "should raise ElementDoesNotExist exception on IndexError"
    with pytest.raises(ElementDoesNotExist):
        ElementList([], query=".element[title=título]").first


def test_raise_attribute_error():
    """
    should raise AttributeError when trying to access
    a non-existent method on list and element
    """
    with pytest.raises(AttributeError):
        the_list = ElementList([Person(), Person()])
        the_list.talk()


def test_attribute_error_method_for_empty():
    """
    should raise ElementDoesNotExist when the list is empty
    and someone tries to access a method or property on the child element.
    """
    with pytest.raises(ElementDoesNotExist):
        the_list = ElementList([])
        the_list.unknown_method()


def test_attribute_error_content():
    "should raise AttributeError with right content"
    with pytest.raises(AttributeError) as e:
        the_list = ElementList([Person(), Person()])
        the_list.talk()

    expected_message = "'ElementList' object has no attribute 'talk'"
    assert expected_message == str(e.value)


def test_not_found_exception_with_query_and_method():
    """
    should receive the find method
    and the query and use them in exception
    """
    with pytest.raises(ElementDoesNotExist) as e:
        the_list = ElementList([], find_by="id", query="menu")
        the_list.first

    expected_message = 'No elements were found with id "menu"'
    assert expected_message == str(e.value)


def test_elementlist_repr():
    """repr() of ElementList is identical to repr() of the internal container."""
    the_list = [Person(), Person()]
    elementlist = ElementList(the_list)

    assert repr(elementlist) == repr(the_list)
