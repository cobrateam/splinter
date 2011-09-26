# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from splinter.meta import InheritedDocs


class SuperClass(object):
    __metaclass__ = InheritedDocs

    def say_hello(self):
        """
        Says hello
        """
        pass


class SubClass(SuperClass):

    def say_hello(self):
        print "hello"

    @property
    def name(self):
        """
        Stores the name
        """
        pass


class SubSubClass(SubClass):

    def say_hello(self):
        print "I can't say hello"

    say_hi = say_hello

    @property
    def name(self):
        pass


class MetaTest(unittest.TestCase):

    def test_should_include_docs_from_superclass(self):
        "should include doc from superclass"
        self.assertEquals(SuperClass.say_hello.__doc__, SubClass.say_hello.__doc__)

    def test_should_include_docs_from_any_class_in_hierarchy(self):
        "should include doc from any class in hierarchy"
        self.assertEquals(SuperClass.say_hello.__doc__, SubSubClass.say_hello.__doc__)

    def test_change_docs_for_readonly_properties(self):
        "should also change docs for readonly properties"
        self.assertEquals(SubClass.name.__doc__, SubSubClass.name.__doc__)

    def test_should_not_touch_the_class_type(self):
        "shouldn't touch the type of the object"
        self.assertEquals('SubSubClass', SubSubClass.__name__)
