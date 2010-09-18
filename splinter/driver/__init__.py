from selenium.firefox.webdriver import WebDriver as firefox

class WebDriver(object):
    
    def __init__(self):
        self.driver = firefox()
    
    def visit(self, url):
        self.driver.get('http://google.com')
    
    def get_title(self):
        return self.driver.get_title()
        
    def quit(self):
        self.driver.quit()