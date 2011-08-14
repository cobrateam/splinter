# -*- coding: utf-8 -*-

import unittest

from nose.tools import assert_equals
from splinter.meta import InheritedDocs

class MetaTest(unittest.TestCase):

    def test_should_include_docs_from_superclass(self):
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

        assert_equals("Says hello", SubClass.say_hello.__doc__)
