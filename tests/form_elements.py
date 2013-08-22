# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

class FormElementsTest(object):

    def test_can_change_field_value(self):
        "should provide a away to change field value"
        self.browser.fill('query', 'new query')
        value = self.browser.find_by_name('query').value
        self.assertEqual('new query', value)

    def test_should_provide_a_method_on_element_to_change_its_value(self):
        self.browser.find_by_name('query').fill('new query')
        value = self.browser.find_by_name('query').value
        self.assertEqual('new query', value)

    def test_submiting_a_form_and_verifying_page_content(self):
        self.browser.fill('query', 'my name')
        self.browser.find_by_name('send').click()
        assert 'My name is: Master Splinter' in self.browser.html

    def test_can_choose_a_radio_button(self):
        "should provide a way to choose a radio button"
        self.assertFalse(self.browser.find_by_id("gender-m").checked)
        self.browser.choose("gender", "M")
        self.assertTrue(self.browser.find_by_id("gender-m").checked)

    def test_can_find_option_by_value(self):
        "should provide a way to find select option by value"
        self.assertEqual("Rio de Janeiro", self.browser.find_option_by_value("rj").text)

    def test_can_get_value_attribute_for_a_option(self):
        "should option have a value attribute"
        self.assertEqual("rj", self.browser.find_option_by_value("rj")["value"])

    def test_can_find_option_by_text(self):
        "should provide a way to find select option by text"
        self.assertEqual("rj", self.browser.find_option_by_text("Rio de Janeiro").value)

    def test_can_select_a_option(self):
        "should provide a way to select a option"
        self.assertFalse(self.browser.find_option_by_value("rj").selected)
        self.browser.select("uf", "rj")
        self.assertTrue(self.browser.find_option_by_value("rj").selected)

    def test_can_select_a_option_via_element(self):
        "should provide a way to select a option via element"
        self.assertFalse(self.browser.find_option_by_value("rj").selected)
        self.browser.find_by_name("uf").select("rj")
        self.assertTrue(self.browser.find_option_by_value("rj").selected)

    def test_can_check_a_checkbox(self):
        "should provide a way to check a radio checkbox"
        self.assertFalse(self.browser.find_by_name("some-check").checked)
        self.browser.check("some-check")
        self.assertTrue(self.browser.find_by_name("some-check").checked)

    def test_check_keeps_checked_if_called_multiple_times(self):
        "should keep a checkbox checked if check() is called multiple times"
        self.assertFalse(self.browser.find_by_name("some-check").checked)
        self.browser.check("some-check")
        self.browser.check("some-check")
        self.assertTrue(self.browser.find_by_name("some-check").checked)

    def test_can_uncheck_a_checkbox(self):
        "should provide a way to uncheck a radio checkbox"
        self.assertTrue(self.browser.find_by_name("checked-checkbox").checked)
        self.browser.uncheck("checked-checkbox")
        self.assertFalse(self.browser.find_by_name("checked-checkbox").checked)

    def test_uncheck_should_keep_unchecked_if_called_multiple_times(self):
        "should keep a checkbox unchecked if uncheck() is called multiple times"
        self.assertTrue(self.browser.find_by_name("checked-checkbox").checked)
        self.browser.uncheck("checked-checkbox")
        self.browser.uncheck("checked-checkbox")
        self.assertFalse(self.browser.find_by_name("checked-checkbox").checked)

    def test_can_fill_text_field_in_form(self):
        "should provide a away to change field value"
        self.browser.fill_form({'query': 'new query'})
        value = self.browser.find_by_name('query').value
        self.assertEqual('new query', value)

    def test_can_fill_password_field_in_form(self):
        "should provide a way to change password value"
        new_password = 'new password'
        self.browser.fill_form({'password': new_password})
        value = self.browser.find_by_name('password').value
        self.assertEqual(new_password, value)

    def test_can_fill_more_than_one_field_in_form(self):
        "should provide a away to change field value"
        self.browser.fill('query', 'my name')
        self.assertFalse(self.browser.find_by_id("gender-m").checked)
        self.assertFalse(self.browser.find_option_by_value("rj").selected)
        self.assertFalse(self.browser.find_by_name("some-check").checked)
        self.assertTrue(self.browser.find_by_name("checked-checkbox").checked)
        self.browser.fill_form({
            'query': 'another new query',
            'description': 'Just another description value in the textarea',
            'gender': 'M',
            'uf': 'rj',
            'some-check': True,
            'checked-checkbox': False
        })
        query_value = self.browser.find_by_name('query').value
        self.assertEqual('another new query', query_value)
        desc_value = self.browser.find_by_name('description').value
        self.assertEqual('Just another description value in the textarea', desc_value)
        self.assertTrue(self.browser.find_by_id("gender-m").checked)
        self.assertTrue(self.browser.find_option_by_value("rj").selected)
        self.assertTrue(self.browser.find_by_name("some-check").checked)
        self.assertFalse(self.browser.find_by_name("checked-checkbox").checked)
