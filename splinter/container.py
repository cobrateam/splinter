from lxml.cssselect import CSSSelector
from selenium.webdriver import Firefox
import time
from splinter.element_list import ElementList

class Container(object):
    def __init__(self, context):
        self.driver = Firefox()
        self.wait_time = 2
        self.context = context

    def find_by_css(self):
        selector = CSSSelector(self.context)
        return self.find_by(self.driver.find_elements_by_xpath, selector.path)

    def find_by(self, finder, selector):
        elements = None
        end_time = time.time() + self.wait_time

        while time.time() < end_time:
            try:
                elements = finder(selector)
                if not isinstance(elements, list):
                    elements = [elements]
            except NoSuchElementException:
                pass

            if elements:
                return ElementList([self.element_class(element, self) for element in elements])
        return ElementList([])

    def find_by_xpath(self, xpath):
        raise NotImplementedError
