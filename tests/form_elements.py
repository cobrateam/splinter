from should_dsl import should, should_not

class FormElementsTest(object):

    def test_can_change_field_value(self):
        "should provide a away to change field value"
        self.browser.fill('query', 'new query')
        value = self.browser.find_by_name('query').first.value
        value |should| equal_to('new query')

    def test_submiting_a_form_and_verifying_page_content(self):
        "should be able search a term in google and verifying if content expected exists"
        self.browser.fill('query', 'my name')
        self.browser.find_by_name('send').first.click()
        self.browser.html |should| include('My name is: Master Splinter')

    def test_can_choose_a_radio_button(self):
        "should provide a way to choose a radio button"
        self.browser.find_by_name("some-radio").first |should_not| be_checked
        self.browser.choose("some-radio")
        self.browser.find_by_name("some-radio").first |should| be_checked

    def test_can_find_option_by_value(self):
        "should provide a way to find select option by value"
        self.browser.find_option_by_value("rj").first.text |should| equal_to("Rio de Janeiro")

    def test_can_get_value_attribute_for_a_option(self):
        "should option have a value attribute"
        self.browser.find_option_by_value("rj").first["value"] |should| equal_to("rj")

    def test_can_find_option_by_text(self):
        "should provide a way to find select option by text"
        self.browser.find_option_by_text("Rio de Janeiro").first.value |should| equal_to("rj")

    def test_can_select_a_option(self):
        "should provide a way to select a option"
        self.browser.find_option_by_value("rj").first |should_not| be_selected
        self.browser.select("uf", "rj")
        self.browser.find_option_by_value("rj").first |should| be_selected

    def test_can_check_a_checkbox(self):
        "should provide a way to check a radio checkbox"
        self.browser.find_by_name("some-check").first |should_not| be_checked
        self.browser.check("some-check")
        self.browser.find_by_name("some-check").first |should| be_checked

    def test_check_keeps_checked_if_called_multiple_times(self):
        "should keep a checkbox checked if check() is called multiple times"
        self.browser.find_by_name("some-check").first |should_not| be_checked
        self.browser.check("some-check")
        self.browser.check("some-check")
        self.browser.find_by_name("some-check").first |should| be_checked

    def test_can_uncheck_a_checkbox(self):
        "should provide a way to uncheck a radio checkbox"
        self.browser.find_by_name("checked-checkbox").first |should| be_checked
        self.browser.uncheck("checked-checkbox")
        self.browser.find_by_name("checked-checkbox").first |should_not| be_checked

    def test_uncheck_should_keep_unchecked_if_called_multiple_times(self):
        "should keep a checkbox unchecked if uncheck() is called multiple times"
        self.browser.find_by_name("checked-checkbox").first |should| be_checked
        self.browser.uncheck("checked-checkbox")
        self.browser.uncheck("checked-checkbox")
        self.browser.find_by_name("checked-checkbox").first |should_not| be_checked


