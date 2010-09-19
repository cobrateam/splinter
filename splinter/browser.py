from splinter.page import Page
from splinter.driver import WebDriver

class Browser(object):
    
    def __init__(self):
        self.driver = WebDriver()
        
    def visit(self, url):
        self.driver.visit(url)
        return Page(url, self)
        
    def quit(self):
        self.driver.quit()