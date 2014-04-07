# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

from splinter.meta import InheritedDocs


class SuperClass(InheritedDocs('_SuperClass', (object,), {})):

    def say_hello(self):
        """
        Says hello
        """
        pass


class SubClass(SuperClass):

    def say_hello(self):
        print("hello")

    @property
    def name(self):
        """
        Stores the name
        """
        pass


class SubSubClass(SubClass):

    def say_hello(self):
        print("I can't say hello")

    say_hi = say_hello

    @property
    def name(self):
        pass


class MetaTest(unittest.TestCase):

    def test_should_include_docs_from_superclass(self):
        "should include doc from superclass"
        self.assertEqual(
            SuperClass.say_hello.__doc__,
            SubClass.say_hello.__doc__
        )

    def test_should_include_docs_from_any_class_in_hierarchy(self):
        "should include doc from any class in hierarchy"
        self.assertEqual(
            SuperClass.say_hello.__doc__,
            SubSubClass.say_hello.__doc__
        )

    def test_change_docs_for_readonly_properties(self):
        "should also change docs for readonly properties"
        self.assertEqual(SubClass.name.__doc__, SubSubClass.name.__doc__)

    def test_should_not_touch_the_class_type(self):
        "shouldn't touch the type of the object"
        self.assertEqual('SubSubClass', SubSubClass.__name__)
