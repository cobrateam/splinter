from selenium.firefox.webdriver import WebDriver as firefox
from selenium.remote.errorhandler import InvalidElementStateException
from lxml.cssselect import CSSSelector
from splinter.driver import DriverAPI, ElementAPI

class WebDriver(DriverAPI):
    
    def __init__(self):
        self.driver = firefox()

    @property
    def title(self):
        return self.driver.get_title()

    @property
    def html(self):
        return self.driver.get_page_source()

    @property
    def url(self):
        return self.driver.get_current_url()

    def visit(self, url):
        self.driver.get(url)
 
    def find(self, css_selector=None,
                   xpath=None,
                   name=None,
                   id=None,
                   tag=None):
        if css_selector:
            return self._find_by_css_selector(css_selector)
        if xpath:
            return self._find_by_xpath(xpath)
        if name:
            return self._find_by_name(name)
        if id:
            return self._find_by_id(id)
        if tag:
            return self._find_by_tag(tag)

    def find_link(self, text=None, href=None):
        if text:
            return WebDriverElement(self.driver.find_element_by_link_text(text))
        if href:
            return self.find(xpath='//a[@href="%s" and (position() = 1)]' % href)

    def _find_by_css_selector(self, css_selector):
        selector = CSSSelector(css_selector)
        return WebDriverElement(self.driver.find_element_by_xpath(selector.path))

    def _find_by_xpath(self, xpath):
        return WebDriverElement(self.driver.find_element_by_xpath(xpath))

    def _find_by_name(self, name):
        return WebDriverElement(self.driver.find_element_by_name(name))

    def _find_by_id(self, id):
        return WebDriverElement(self.driver.find_element_by_id(id))

    def _find_by_tag(self, tag):
        return WebDriverElement(self.driver.find_element_by_tag_name(tag))

    def fill_in(self, name, value):
        field = self.find(name=name)
        field.value = value
    
    def choose(self, name):
        field = self.find(name=name)
        field.click()
    
    check = choose

    def quit(self):
        self.driver.quit()


class WebDriverElement(ElementAPI):

    def __init__(self, element):
        self._element = element

    def _get_value(self):
        try:
            return self._element.get_value()
        except InvalidElementStateException:
            return self._element.get_text()

    def _set_value(self, value):
        self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)

    def click(self):
        self._element.click()
        
    @property
    def checked(self):
        return self._element.is_selected()
        
    @property
    def visible(self):
        return self._element.is_displayed()

    def __getitem__(self, attr):
        return self._element.get_attribute(attr)
