from should_dsl import should, should_not
from fake_webapp import EXAMPLE_APP

class BaseBrowserTests(object):

    def setUp(self):
        self.fail("You should set up your browser in the setUp() method")

    def test_can_open_page(self):
        "should be able to visit, get title and quit"
        title = self.browser.title
        title |should| equal_to('Example Title')

    def test_should_have_html(self):
        "should have access to the html"
        html = self.browser.html
        html |should| include('<title>Example Title</title>')
        html |should| include('<h1 id="firstheader">Example Header</h1>')

    def test_should_have_url(self):
        "should have access to the url"
        url = self.browser.url
        url |should| equal_to(EXAMPLE_APP)

    def test_finding_by_css_selector(self):
        "should find elements by css_selector"
        value = self.browser.find_by_css_selector('h1').value
        value |should| equal_to('Example Header')

    def test_finding_by_xpath(self):
        "should find elements by xpath"
        value = self.browser.find_by_xpath('//h1').value
        value |should| equal_to('Example Header')

    def test_finding_by_tag(self):
        "should find elements by tag"
        value = self.browser.find_by_tag('h1').value
        value |should| equal_to('Example Header')

    def test_finding_by_id(self):
        "should find elements by id"
        value = self.browser.find_by_id("firstheader").value
        value |should| equal_to('Example Header')

    def test_finding_by_name(self):
        "should find elements by name"
        value = self.browser.find_by_name('query').value
        value |should| equal_to('default value')

    def test_finding_links_by_text(self):
        "should find links by text"
        link = self.browser.find_link_by_text('Link for Example.com')
        link['href'] |should| equal_to('http://example.com')

    def test_finding_links_by_href(self):
        "should find links by href"
        link = self.browser.find_link_by_href('http://example.com')
        link['href'] |should| equal_to('http://example.com')

    def test_can_change_field_value(self):
        "should provide a away to change field value"
        self.browser.fill_in('query', 'new query')
        value = self.browser.find_by_name('query').value
        value |should| equal_to('new query')

    def test_submiting_a_form_and_verifying_page_content(self):
        "should be able search a term in google and verifying if content expected exists"
        self.browser.fill_in('query', 'my name')
        self.browser.find_by_name('send').click()
        self.browser.html |should| include('My name is: Master Splinter')

    def test_can_choose_a_radio_button(self):
        "should provide a way to choose a radio button"
        self.browser.find_by_name("some-radio") |should_not| be_checked
        self.browser.choose("some-radio")
        self.browser.find_by_name("some-radio") |should| be_checked

    def test_can_check_a_checkbox(self):
        "should provide a way to check a radio checkbox"
        self.browser.find_by_name("some-check") |should_not| be_checked
        self.browser.check("some-check")
        self.browser.find_by_name("some-check") |should| be_checked

    def test_check_keeps_checked_if_called_multiple_times(self):
        "should keep a checkbox checked if check() is called multiple times"
        self.browser.find_by_name("some-check") |should_not| be_checked
        self.browser.check("some-check")
        self.browser.check("some-check")
        self.browser.find_by_name("some-check") |should| be_checked

    def test_can_uncheck_a_checkbox(self):
        "should provide a way to uncheck a radio checkbox"
        self.browser.find_by_name("checked-checkbox") |should| be_checked
        self.browser.uncheck("checked-checkbox")
        self.browser.find_by_name("checked-checkbox") |should_not| be_checked

    def test_uncheck_should_keep_unchecked_if_called_multiple_times(self):
        "should keep a checkbox unchecked if uncheck() is called multiple times"
        self.browser.find_by_name("checked-checkbox") |should| be_checked
        self.browser.uncheck("checked-checkbox")
        self.browser.uncheck("checked-checkbox")
        self.browser.find_by_name("checked-checkbox") |should_not| be_checked

    def test_click_links(self):
        "should allow to click links"
        self.browser.find_link_by_text('FOO').click()
        self.browser.html |should| include('BAR!')

    def test_click_element_by_css_selector(self):
        "should allow to click at elements by css selector"
        self.browser.find_by_css_selector('a[href="/foo"]').click()
        self.browser.html |should| include('BAR!')

    def test_click_input_by_css_selector(self):
        "should allow to click at inputs by css selector"
        self.browser.find_by_css_selector('input[name="send"]').click()
        self.browser.html |should| include('My name is: Master Splinter')

    def test_accessing_attributes_of_links(self):
        "should allow link's attributes retrieval"
        foo = self.browser.find_link_by_text('FOO')
        foo['href'] |should| equal_to('/foo')

    def test_accessing_attributes_of_inputs(self):
        "should allow input's attributes retrieval"
        button = self.browser.find_by_css_selector('input[name="send"]')
        button['name'] |should| equal_to('send')

    def test_accessing_attributes_of_simple_elements(self):
        "should allow simple element's attributes retrieval"
        header = self.browser.find_by_css_selector('h1')
        header['id'] |should| equal_to('firstheader')

    def test_links_should_have_value_attribute(self):
        foo = self.browser.find_link_by_href('/foo')
        foo.value |should| equal_to('FOO')

class WebDriverTests(BaseBrowserTests):

    def test_can_execute_javascript(self):
        "should execute javascript"
        self.browser.execute_script("$('body').empty()")
        self.browser.find_by_tag("body") == ""

    def test_can_evaluate_script(self):
        "should evaluate script"
        assert self.browser.evaluate_script("4+4") == 8

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        self.browser.find_by_id("visible") |should| be_visible

    def test_can_verify_if_a_element_is_invisible(self):
        "should provide verify if element is invisible"
        self.browser.find_by_id("invisible") |should_not| be_visible
