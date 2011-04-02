from should_dsl import should

class ClickElementsTest(object):

    def test_click_links(self):
        "should allow to click links"
        self.browser.find_link_by_text('FOO').first.click()
        self.browser.html |should| include('BAR!')

    def test_click_element_by_css_selector(self):
        "should allow to click at elements by css selector"
        self.browser.find_by_css_selector('a[href="/foo"]').first.click()
        self.browser.html |should| include('BAR!')

    def test_click_input_by_css_selector(self):
        "should allow to click at inputs by css selector"
        self.browser.find_by_css_selector('input[name="send"]').first.click()
        self.browser.html |should| include('My name is: Master Splinter')


