import warnings

from nose.tools import assert_equals, assert_true, assert_false

class FormElementsTest(object):

    def test_can_change_field_value(self):
        "should provide a away to change field value"
        self.browser.fill('query', 'new query')
        value = self.browser.find_by_name('query').first.value
        assert_equals('new query', value)

    def test_existence_of_the_fill_in_alias_and_that_its_deprecated(self):
        "should check the existence of the fill_in alias for backwards compatibility"
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self.browser.fill_in('query', 'new query')
            warn = w[-1]
            warn_message = str(warn.message)
            assert issubclass(warn.category, DeprecationWarning)
            assert "fill" in warn_message
            assert "fill_in" in warn_message
        value = self.browser.find_by_name('query').first.value
        assert_equals('new query', value)

    def test_submiting_a_form_and_verifying_page_content(self):
        "should be able search a term in google and verifying if content expected exists"
        self.browser.fill('query', 'my name')
        self.browser.find_by_name('send').first.click()
        assert 'My name is: Master Splinter' in self.browser.html

    def test_can_choose_a_radio_button(self):
        "should provide a way to choose a radio button"
        assert_false(self.browser.find_by_id("gender-m").first.checked)
        self.browser.choose("gender", "M")
        assert_true(self.browser.find_by_id("gender-m").first.checked)

    def test_can_find_option_by_value(self):
        "should provide a way to find select option by value"
        assert_equals("Rio de Janeiro", self.browser.find_option_by_value("rj").first.text)

    def test_can_get_value_attribute_for_a_option(self):
        "should option have a value attribute"
        assert_equals("rj", self.browser.find_option_by_value("rj").first["value"])

    def test_can_find_option_by_text(self):
        "should provide a way to find select option by text"
        assert_equals("rj", self.browser.find_option_by_text("Rio de Janeiro").first.value)

    def test_can_select_a_option(self):
        "should provide a way to select a option"
        assert_false(self.browser.find_option_by_value("rj").first.selected)
        self.browser.select("uf", "rj")
        assert_true(self.browser.find_option_by_value("rj").first.selected)

    def test_can_check_a_checkbox(self):
        "should provide a way to check a radio checkbox"
        assert_false(self.browser.find_by_name("some-check").first.checked)
        self.browser.check("some-check")
        assert_true(self.browser.find_by_name("some-check").first.checked)

    def test_check_keeps_checked_if_called_multiple_times(self):
        "should keep a checkbox checked if check() is called multiple times"
        assert_false(self.browser.find_by_name("some-check").first.checked)
        self.browser.check("some-check")
        self.browser.check("some-check")
        assert_true(self.browser.find_by_name("some-check").first.checked)

    def test_can_uncheck_a_checkbox(self):
        "should provide a way to uncheck a radio checkbox"
        assert_true(self.browser.find_by_name("checked-checkbox").first.checked)
        self.browser.uncheck("checked-checkbox")
        assert_false(self.browser.find_by_name("checked-checkbox").first.checked)

    def test_uncheck_should_keep_unchecked_if_called_multiple_times(self):
        "should keep a checkbox unchecked if uncheck() is called multiple times"
        assert_true(self.browser.find_by_name("checked-checkbox").first.checked)
        self.browser.uncheck("checked-checkbox")
        self.browser.uncheck("checked-checkbox")
        assert_false(self.browser.find_by_name("checked-checkbox").first.checked)
