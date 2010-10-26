import lxml.html
from should_dsl import should, should_not
from fake_webapp import EXAMPLE_APP, EXAMPLE_HTML

import shutil
import os

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
    
    def test_save_and_open_page(self):
        self.browser.save_and_open_page()
        
    def test_save_and_open_page_when_temp_directory_does_not_exist(self):
        shutil.rmtree('/tmp/splinter')
        self.browser.save_and_open_page()
        
    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').click()
    
        html = self.browser.html
        html |should| include('text/plain')
        html |should| include(open(file_path).read())
    
    def test_click_links(self):
        "should allow to click links"
        self.browser.find_link_by_text('FOO').click()
        self.browser.html |should| include('BAR!')
