import unittest
import lxml.html
from should_dsl import should
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP, EXAMPLE_HTML
from time import sleep

class BrowserTest(unittest.TestCase):

    def setUp(self):
        self.browser = Browser()
        self.browser.visit(EXAMPLE_APP)

    def tearDown(self):
        self.browser.quit()

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

    def test_finding_elements(self):
        "should find elements by css_selector, xpath, tag and id"
        values = [self.browser.find(css_selector='h1').value,
                  self.browser.find(xpath='//h1').value,
                  self.browser.find(tag='h1').value,
                  self.browser.find(id='firstheader').value]
        set(values) |should| equal_to(set([values[0]]))

    def test_can_find_by_name(self):
        "should find elements by name"
        field = self.browser.find(name='query')
        field.value |should| equal_to('default value')

    def test_finding_links(self):
        "should find links by text"
        link1 = self.browser.find_link(text='Link for Example.com')
        link2 = self.browser.find_link(href='http://example.com')
        link1['href'] |should| equal_to('http://example.com')
        link2['href'] |should| equal_to('http://example.com')

    def test_can_change_field_value(self):
        "should provide a away to change field value"
        self.browser.fill_in('query', 'new query')
        value = self.browser.find(name='query').value
        value |should| equal_to('new query')

    def test_submiting_a_form_and_verifying_page_content(self):
        "should be able search a term in google and verifying if content expected exists"
        self.browser.fill_in('query', 'my name')
        self.browser.find(name='send').click()
        self.browser.html |should| include('My name is: Master Splinter')
        
    def test_can_choose_a_radio_button(self):
        "should provide a way to choose a radio button"
        assert not self.browser.find(name="some-radio").checked
        self.browser.choose("some-radio")
        assert self.browser.find(name="some-radio").checked
        
    def test_can_check_a_checkbox(self):
        "should provide a way to check a radio checkbox"
        assert not self.browser.find(name="some-check").checked
        self.browser.check("some-check")
        assert self.browser.find(name="some-check").checked

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        assert self.browser.find(id="visible").visible
        assert not self.browser.find(id="invisible").visible