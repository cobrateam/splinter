from splinter.driver import WebDriver

class Browser(object):
    
    def __init__(self):
        self.driver = WebDriver()
        
    def visit(self, url):
        return self.driver.visit(url)
        
    def quit(self):
        self.driver.quit()
