from nose.tools import assert_equals, assert_true, assert_false
from fake_webapp import EXAMPLE_APP
from find_elements import FindElementsTest
from form_elements import FormElementsTest
from click_elements import ClickElementsTest
from element_does_not_exist import ElementDoestNotExistTest
from is_element_present import IsElementPresentTest
from iframes import IFrameElementsTest
from status_code import StatusCodeTest
from async_finder import AsyncFinderTests
from is_text_present import IsTextPresentTest
from within_elements import WithinElementsTest
from cookies import CookiesTest


class BaseBrowserTests(FindElementsTest, FormElementsTest, ClickElementsTest, WithinElementsTest, CookiesTest):

    def setUp(self):
        self.fail("You should set up your browser in the setUp() method")

    def test_can_open_page(self):
        "should be able to visit, get title and quit"
        title = self.browser.title
        assert_equals('Example Title', title)

    def test_can_back_on_history(self):
        "should be able to back on history"
        self.browser.visit("%s/iframe" % EXAMPLE_APP.rstrip('/'))
        self.browser.back()
        assert_equals(EXAMPLE_APP, self.browser.url)

    def test_can_forward_on_history(self):
        "should be able to forward history"
        url = "%s/iframe" % EXAMPLE_APP.rstrip('/')
        self.browser.visit(url)
        self.browser.back()
        self.browser.forward()
        assert_equals(url, self.browser.url)

    def test_should_have_html(self):
        "should have access to the html"
        html = self.browser.html
        assert '<title>Example Title</title>' in html
        assert '<h1 id="firstheader">Example Header</h1>' in html

    def test_should_reload_a_page(self):
        "should reload a page"
        title = self.browser.title
        self.browser.reload()
        assert_equals('Example Title', title)

    def test_should_have_url(self):
        "should have access to the url"
        assert_equals(EXAMPLE_APP, self.browser.url)

    def test_accessing_attributes_of_links(self):
        "should allow link's attributes retrieval"
        foo = self.browser.find_link_by_text('FOO').first
        assert_equals('http://localhost:5000/foo', foo['href'])

    def test_accessing_attributes_of_inputs(self):
        "should allow input's attributes retrieval"
        button = self.browser.find_by_css('input[name="send"]').first
        assert_equals('send', button['name'])

    def test_accessing_attributes_of_simple_elements(self):
        "should allow simple element's attributes retrieval"
        header = self.browser.find_by_css('h1').first
        assert_equals('firstheader', header['id'])

    def test_links_should_have_value_attribute(self):
        foo = self.browser.find_link_by_href('http://localhost:5000/foo').first
        assert_equals('FOO', foo.value)

    def test_should_receive_browser_on_parent(self):
        "element should contains the browser on \"parent\" attribute"
        element = self.browser.find_by_id("firstheader").first
        assert_equals(self.browser, element.parent)


class WebDriverTests(BaseBrowserTests, IFrameElementsTest, ElementDoestNotExistTest, IsElementPresentTest, AsyncFinderTests, IsTextPresentTest, StatusCodeTest):

    def test_can_execute_javascript(self):
        "should be able to execute javascript"
        self.browser.execute_script("$('body').empty()")
        assert_equals("", self.browser.find_by_tag("body").first.value)

    def test_can_evaluate_script(self):
        "should evaluate script"
        assert_equals(8, self.browser.evaluate_script("4+4"))

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        assert_true(self.browser.find_by_id("visible").first.visible)

    def test_can_verify_if_a_element_is_invisible(self):
        "should provide verify if element is invisible"
        assert_false(self.browser.find_by_id("invisible").first.visible)

    def test_default_wait_time_should_be_2(self):
        "should driver default wait time 2"
        assert_equals(2, self.browser.wait_time)
