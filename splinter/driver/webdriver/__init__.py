from selenium.remote.errorhandler import InvalidElementStateException
from lxml.cssselect import CSSSelector
from splinter.driver import DriverAPI, ElementAPI
from splinter.element_list import ElementList

class BaseWebDriver(DriverAPI):

    def __init__(self):
        raise NotImplementedError

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

    def execute_script(self, script):
        self.driver.execute_script(script)

    def evaluate_script(self, script):
        return self.driver.execute_script("return %s" % script)
    
    def find_option_by_value(self, value):
        return self.find_by_xpath('//option[@value="%s"]' % value)

    def find_option_by_text(self, text):
        return self.find_by_xpath('//option[normalize-space(text())="%s"]' % text)

    def find_link_by_href(self, href):
        return self.find_by_xpath('//a[@href="%s"]' % href)

    def find_link_by_text(self, text):
        return ElementList([self.element_class(element) for element in self.driver.find_elements_by_link_text(text)])
        
    def find_by_css_selector(self, css_selector):
        selector = CSSSelector(css_selector)
        return self.find_by_xpath(selector.path)

    def find_by_xpath(self, xpath):
        return ElementList([self.element_class(element) for element in self.driver.find_elements_by_xpath(xpath)])

    def find_by_name(self, name):
        return ElementList([self.element_class(element) for element in self.driver.find_elements_by_name(name)])

    def find_by_id(self, id):
        return ElementList([self.element_class(self.driver.find_element_by_id(id))])

    def find_by_tag(self, tag):
        return ElementList([self.element_class(element) for element in self.driver.find_elements_by_tag_name(tag)])

    def fill_in(self, name, value):
        field = self.find_by_name(name).first
        field.value = value

    fill = fill_in
    attach_file = fill

    def choose(self, name):
        field = self.find_by_name(name).first
        field.click()

    def check(self, name):
        field = self.find_by_name(name).first
        field.check()

    def uncheck(self, name):
        field = self.find_by_name(name).first
        field.uncheck()
    
    def select(self, name, value):
        self.find_by_xpath('//select[@name="%s"]/option[@value="%s"]' % (name, value)).first._element.set_selected()

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
    
    @property
    def text(self):
        return self._element.get_text()
                
    def click(self):
        self._element.click()

    def check(self):
        if not self.checked:
            self._element.toggle()

    def uncheck(self):
        if self.checked:
            self._element.toggle()

    @property
    def checked(self):
        return self._element.is_selected()
    
    selected = checked

    @property
    def visible(self):
        return self._element.is_displayed()

    def __getitem__(self, attr):
        return self._element.get_attribute(attr)
