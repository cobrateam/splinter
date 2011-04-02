from should_dsl import should, should_not
from fake_webapp import EXAMPLE_APP

from find_elements import FindElementsTest
from form_elements import FormElementsTest
from click_elements import ClickElementsTest
from element_does_not_exist import ElementDoestNotExistTest
from is_element_present import IsElementPresentTest
from async_finder import AsyncFinderTests

class BaseBrowserTests(FindElementsTest, FormElementsTest, ClickElementsTest):

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

    def test_accessing_attributes_of_links(self):
        "should allow link's attributes retrieval"
        foo = self.browser.find_link_by_text('FOO').first
        foo['href'] |should| equal_to('/foo')

    def test_accessing_attributes_of_inputs(self):
        "should allow input's attributes retrieval"
        button = self.browser.find_by_css_selector('input[name="send"]').first
        button['name'] |should| equal_to('send')

    def test_accessing_attributes_of_simple_elements(self):
        "should allow simple element's attributes retrieval"
        header = self.browser.find_by_css_selector('h1').first
        header['id'] |should| equal_to('firstheader')

    def test_links_should_have_value_attribute(self):
        foo = self.browser.find_link_by_href('/foo').first
        foo.value |should| equal_to('FOO')


class WebDriverTests(BaseBrowserTests, ElementDoestNotExistTest, IsElementPresentTest, AsyncFinderTests):

    def test_can_execute_javascript(self):
        "should execute javascript"
        self.browser.execute_script("$('body').empty()")
        self.browser.find_by_tag("body") == ""

    def test_can_evaluate_script(self):
        "should evaluate script"
        assert self.browser.evaluate_script("4+4") == 8

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        self.browser.find_by_id("visible").first |should| be_visible

    def test_can_verify_if_a_element_is_invisible(self):
        "should provide verify if element is invisible"
        self.browser.find_by_id("invisible").first |should_not| be_visible

    def test_default_wait_time_should_be_2(self):
        "should driver default wait time 2"
        self.browser.wait_time |should| be(2)
