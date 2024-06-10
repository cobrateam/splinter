# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from .fake_webapp import EXAMPLE_APP


class SlowlyTypeTest:
    def test_simple_type(self):
        """should provide a away to change field value using type method"""
        self.browser.visit(EXAMPLE_APP)
        elem = self.browser.find_by_name("query")
        elem.type(" with type method")
        assert "default value with type method" == elem.value

        self.browser.find_by_name("description").type("type into textarea")
        value = self.browser.find_by_name("description").value
        assert "type into textarea" == value

    def test_simple_type_on_element(self):
        self.browser.visit(EXAMPLE_APP)
        elem = self.browser.find_by_name("query")
        elem.type(" with type method")
        assert "default value with type method" == elem.value

        self.browser.find_by_name("description").type("type into textarea")
        value = self.browser.find_by_name("description").value
        assert "type into textarea" == value

    def test_slowly_typing(self):
        """should be able to slowly type some text in a field"""
        for name in ["type-input", "type-textarea"]:
            self.browser.visit(EXAMPLE_APP + "type")
            num = 0
            num_max = 6
            for key in self.browser.find_by_name(name).type("typing", slowly=True):
                assert self.browser.is_text_present("#%d" % num)
                num += 1
            assert num == num_max

            element = self.browser.find_by_name(name)
            assert element.value == "typing"

    def test_slowly_typing_on_element(self):
        for name in ["type-input", "type-textarea"]:
            self.browser.visit(EXAMPLE_APP + "type")
            num = 0
            num_max = 6
            text_input = self.browser.find_by_name(name)
            typing = text_input.type("typing", slowly=True)
            for key in typing:
                assert self.browser.is_text_present("#%d" % num)
                num += 1
            assert num == num_max

            element = self.browser.find_by_name(name)
            assert element.value == "typing"
