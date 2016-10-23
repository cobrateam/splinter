# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import time


class FormElementsTest(object):

    def test_fill(self):
        self.browser.fill('query', 'new query')
        value = self.browser.find_by_name('query').value
        self.assertEqual('new query', value)

    def test_fill_element(self):
        self.browser.find_by_name('q').fill('new query')
        time.sleep(1)
        value = self.browser.find_by_name('q').value
        self.assertEqual('new query', value)

    def test_submiting_a_form_and_verifying_page_content(self):
        self.browser.fill('query', 'my name')
        self.browser.find_by_name('send').click()
        self.assertIn('My name is: Master Splinter', self.browser.html)

    def test_can_choose_a_radio_button(self):
        "should provide a way to choose a radio button"
        self.assertFalse(self.browser.find_by_id("gender-m").checked)
        self.browser.choose("gender", "M")
        self.assertTrue(self.browser.find_by_id("gender-m").checked)

    def test_can_find_textarea_by_tag(self):
        "should provide a way to find a textarea by tag_name"
        tag = self.browser.find_by_tag("textarea").first
        self.assertEqual('', tag.value)

    def test_can_find_input_without_type(self):
        "should recognize an input element that doesn't have a `type` attribute"
        tag = self.browser.find_by_css('[name="typeless"]').first
        self.assertEqual('default value', tag.value)

    def test_can_find_button(self):
        "should recognize a button"
        tag = self.browser.find_by_css('.just-a-button').first
        self.assertTrue(hasattr(tag, 'click'))

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

    def test_can_select_an_option_in_an_optgroup(self):
        "should provide a way to select an option that is in an optgroup"
        self.assertEqual(self.browser.find_by_name("food").value, "apples")
        self.browser.select("food", "grapes")
        self.assertEqual(self.browser.find_by_name("food").value, "grapes")

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

    def test_can_fill_tel_text_field(self):
        "should provide a way to change a tel field value"
        new_telephone = '555-0042'
        self.browser.fill_form({'telephone': new_telephone})
        value = self.browser.find_by_name('telephone').value
        self.assertEqual(new_telephone, value)

    def test_can_fill_unknown_text_field(self):
        "should provide a way to change a unknown text field type that isn't specifically defined"
        new_search_keyword = 'foobar'
        self.browser.fill_form({'search_keyword': new_search_keyword})
        value = self.browser.find_by_name('search_keyword').value
        self.assertEqual(new_search_keyword, value)

    def test_can_clear_text_field_content(self):
        self.browser.fill('query', 'random query')
        value = self.browser.find_by_name('query').value
        self.assertEqual('random query', value)

        self.browser.find_by_name('query').clear()
        value = self.browser.find_by_name('query').value
        self.assertFalse(value)

    def test_can_clear_password_field_content(self):
        self.browser.fill('password', '1nF4m310')
        value = self.browser.find_by_name('password').value
        self.assertEqual('1nF4m310', value)

        self.browser.find_by_name('password').clear()
        value = self.browser.find_by_name('password').value
        self.assertFalse(value)

    def test_can_clear_tel_field_content(self):
        self.browser.fill('telephone', '5553743980')
        value = self.browser.find_by_name('telephone').value
        self.assertEqual('5553743980', value)

        self.browser.find_by_name('telephone').clear()
        value = self.browser.find_by_name('telephone').value
        self.assertFalse(value)
