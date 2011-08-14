# -*- coding: utf-8 -*-

import unittest

from nose.tools import assert_equals
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


class MetaTest(unittest.TestCase):

    def test_should_include_docs_from_superclass(self):
        "should include doc from superclass"
        assert_equals(SuperClass.say_hello.__doc__, SubClass.say_hello.__doc__)
