from splinter.page import Page
from selenium.firefox.webdriver import WebDriver as firefox

class WebDriver(object):
    
    def __init__(self):
        self.driver = firefox()

    def visit(self, url):
        self.driver.get(url)
        return Page(url, self)

    @property
    def title(self):
        return self.driver.get_title()
        
    def find(self, name):
        return self.driver.find_element_by_name(name)
        
    @property
    def source(self):
        return self.driver.get_page_source()

    def quit(self):
        self.driver.quit()

