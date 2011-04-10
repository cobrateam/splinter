import warnings

from nose.tools import assert_equals

class FindElementsTest(object):

    def test_finding_by_css(self):
        "should finds by css"
        value = self.browser.find_by_css('h1').first.value
        assert_equals(value, 'Example Header')

    def test_existence_of_find_by_css_selector_alias_and_that_its_deprecated(self):
        "should check the existence of find_by_css_selector alias for backwards compatibility"
        found = self.browser.find_by_css('h1').first.value
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            found_deprecated = self.browser.find_by_css_selector('h1').first.value
            warn = w[-1]
            warn_message = str(warn.message)
            assert issubclass(warn.category, DeprecationWarning)
            assert "find_by_css" in warn_message
            assert "find_by_css_selector" in warn_message
        assert_equals(found, found_deprecated)

    def test_finding_by_xpath(self):
        "should find elements by xpath"
        value = self.browser.find_by_xpath('//h1').first.value
        assert_equals(value, 'Example Header')

    def test_finding_by_tag(self):
        "should find elements by tag"
        value = self.browser.find_by_tag('h1').first.value
        assert_equals(value, 'Example Header')

    def test_finding_by_id(self):
        "should find elements by id"
        value = self.browser.find_by_id("firstheader").first.value
        assert_equals(value, 'Example Header')

    def test_finding_by_name(self):
        "should find elements by name"
        value = self.browser.find_by_name('query').first.value
        assert_equals(value, 'default value')

    def test_finding_all_elements_by_css(self):
        "should find elements by css"
        value = self.browser.find_by_css('h1')[0].value
        assert_equals(value, 'Example Header')

    def test_finding_all_elements_by_xpath(self):
        "should find elements by xpath"
        value = self.browser.find_by_xpath('//h1')[0].value
        assert_equals(value, 'Example Header')

    def test_finding_all_elements_by_tag(self):
        "should find elements by tag"
        value = self.browser.find_by_tag('h1')[0].value
        assert_equals(value, 'Example Header')

    def test_finding_all_elements_by_id(self):
        "should find elements by id"
        value = self.browser.find_by_id("firstheader")[0].value
        assert_equals(value, 'Example Header')

    def test_finding_all_elements_by_name(self):
        "should find elements by name"
        value = self.browser.find_by_name('query')[0].value
        assert_equals(value, 'default value')

    def test_finding_all_links_by_text(self):
        "should find links by text"
        link = self.browser.find_link_by_text('Link for Example.com')[0]
        assert_equals(link['href'], 'http://example.com')

    def test_finding_all_links_by_href(self):
        "should find links by href"
        link = self.browser.find_link_by_href('http://example.com')[0]
        assert_equals(link['href'], 'http://example.com')

    def test_finding_last_element_by_css(self):
        "should find last element by css"
        value = self.browser.find_by_css('h1').last.value
        assert_equals(value, 'Example Last Header')

    def test_finding_last_element_by_xpath(self):
        "should find last element by xpath"
        value = self.browser.find_by_xpath('//h1').last.value
        assert_equals(value, 'Example Last Header')

    def test_finding_last_element_by_tag(self):
        "should find last element by tag"
        value = self.browser.find_by_tag('h1').last.value
        assert_equals(value, 'Example Last Header')

    def test_finding_last_element_by_id(self):
        "should find last element by id"
        value = self.browser.find_by_id("firstheader").last.value
        assert_equals(value, 'Example Header')

    def test_last_element_is_same_than_first_element_in_find_by_id(self):
        "should first element is same than last element in find by id"
        #a html page have contain one element by id
        first = self.browser.find_by_id("firstheader").first.value
        last = self.browser.find_by_id("firstheader").last.value
        assert_equals(first, last)

    def test_finding_last_element_by_name(self):
        "should find last element by name"
        value = self.browser.find_by_name('query').last.value
        assert_equals(value, 'default last value')

    def test_finding_last_link_by_text(self):
        "should find last link by text"
        link = self.browser.find_link_by_text('Link for Example.com').last
        assert_equals(link['href'], 'http://example.com/last')

    def test_finding_last_link_by_href(self):
        "should find last link by href"
        link = self.browser.find_link_by_href('http://example.com').last
        assert_equals(link.text, 'Link for last Example.com')

    def test_finding_element_by_css_using_slice(self):
        "should find element by css using slice"
        value = self.browser.find_by_css('h1')[-1].value
        assert_equals(value, 'Example Last Header')

    def test_finding_element_by_xpath_using_slice(self):
        "should find element by xpath using slice"
        value = self.browser.find_by_xpath('//h1')[-1].value
        assert_equals(value, 'Example Last Header')

    def test_finding_element_by_tag_using_slice(self):
        "should find element by tag using slice"
        value = self.browser.find_by_tag('h1')[-1].value
        assert_equals(value, 'Example Last Header')

    def test_finding_element_by_id_using_slice(self):
        "should find element by id using slice"
        value = self.browser.find_by_id("firstheader")[-1].value
        assert_equals(value, 'Example Header')

    def test_all_elements_is_same_than_first_element_in_find_by_id(self):
        "should all elements is same than first element in find by id"
        #a html page have contain one element by id
        first = self.browser.find_by_id("firstheader").first.value
        some = self.browser.find_by_id("firstheader")[-1].value
        assert_equals(first, some)

    def test_finding_element_by_name_using_slice(self):
        "should find element by name using slice"
        value = self.browser.find_by_name('query')[-1].value
        assert_equals(value, 'default last value')

    def test_finding_link_by_text_using_slice(self):
        "should find link by text using slice"
        link = self.browser.find_link_by_text('Link for Example.com')[-1]
        assert_equals(link['href'], 'http://example.com/last')

    def test_finding_link_by_href_using_slice(self):
        "should find link by href using slice"
        link = self.browser.find_link_by_href('http://example.com')[-1]
        assert_equals(link.text, 'Link for last Example.com')

    def test_finding_links_by_text(self):
        "should find links by text"
        link = self.browser.find_link_by_text('Link for Example.com').first
        assert_equals(link['href'], 'http://example.com')

    def test_finding_links_by_href(self):
        "should find links by href"
        link = self.browser.find_link_by_href('http://example.com').first
        assert_equals(link['href'], 'http://example.com')
